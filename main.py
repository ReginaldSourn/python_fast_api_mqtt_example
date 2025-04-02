# main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, SensorData
from mqtt_handler import run_mqtt_in_background
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="IoT Simple Data API", version="1.0")

# Allow Cross-Origin Resource Sharing if needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Start the MQTT client when the FastAPI app starts
@app.on_event("startup")
def startup_event():
    run_mqtt_in_background()
    print("MQTT handler started.")

@app.get("/")
async def root():
    return {"message": "IoT Data API is running"}

@app.get("/data")
def read_sensor_data(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    data = db.query(SensorData).offset(skip).limit(limit).all()
    if not data:
        raise HTTPException(status_code=404, detail="No sensor data available")
    return data
