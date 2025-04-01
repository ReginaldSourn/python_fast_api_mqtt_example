import threading
import paho.mqtt.client as mqtt
from fastapi import FastAPI, HTTPException

app = FastAPI(title="FastAPI & MQTT Integration Example")

# Create a global MQTT client instance
mqtt_client = mqtt.Client()

# Callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully to MQTT broker")
        # Subscribe to a topic after connecting
        client.subscribe("test/topic")
    else:
        print("Failed to connect, return code %d\n", rc)

# Callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(f"Received message on {msg.topic}: {msg.payload.decode()}")

mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

def mqtt_loop():
    # Connect to an MQTT broker (e.g., a public broker or your own)
    mqtt_client.connect("localhost", 1883, 60)
    # Run the loop forever in this thread
    mqtt_client.loop_forever()

# FastAPI startup event: start the MQTT loop in a separate background thread.
@app.on_event("startup")
def startup_event():
    thread = threading.Thread(target=mqtt_loop)
    thread.daemon = True
    thread.start()
    print("MQTT client loop started in a background thread.")

# A basic HTTP endpoint to check service health.
@app.get("/")
async def read_root():
    return {"message": "FastAPI & MQTT are running"}

# Endpoint to publish messages to an MQTT topic.
@app.post("/publish")
async def publish_message(topic: str, payload: str):
    result = mqtt_client.publish(topic, payload)
    # Check if the message was published successfully (result[0] == 0 means success)
    if result.rc != 0:
        raise HTTPException(status_code=500, detail="Failed to publish message")
    return {"message": f"Message published to {topic}"}
