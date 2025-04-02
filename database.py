# database.py
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

DATABASE_URL = "sqlite:///./db.sqlite3"  # SQLite database file

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}  # required for SQLite
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class SensorData(Base):
    __tablename__ = "sensor_data"
    id = Column(Integer, primary_key=True, index=True)
    topic = Column(String, index=True)
    payload = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)
