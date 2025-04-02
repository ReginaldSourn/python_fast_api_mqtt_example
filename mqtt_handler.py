# mqtt_handler.py
import paho.mqtt.client as mqtt
from database import SessionLocal, SensorData
import threading
import ENV
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
        # Subscribe to all sensor topics
        client.subscribe("sensors/#")
    else:
        print("Connection failed with rc:", rc)

def on_message(client, userdata, msg):
    session = SessionLocal()
    try:
        # Decode message and store in the database
        data = SensorData(topic=msg.topic, data=msg.payload.decode())
        print("data received", data)
        session.add(data)
        session.commit()
        print(f"Saved data: {msg.topic} -> {msg.payload.decode()}")
    except Exception as e:
        session.rollback()
        print("Error saving data:", e)
    finally:
        session.close()

def start_mqtt():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    broker = ENV.host
    # Connect to a public broker or your own
    client.connect(broker, 1883, 60)
    client.loop_forever()

def run_mqtt_in_background():
    thread = threading.Thread(target=start_mqtt)
    thread.daemon = True  # Daemonize thread so it exits when the main program exits
    thread.start()
