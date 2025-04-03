import time
import paho.mqtt.client as mqtt
import ENV
# MQTT configuration
MQTT_BROKER = ENV.host  # Replace with your MQTT broker address
MQTT_PORT = 1883
MQTT_TOPIC_TEMPERATURE = "raspi/temperature"
MQTT_TOPIC_CPU_TEMPERATURE = "raspi/cpu_temperature"

# Initialize MQTT client
mqtt_client = mqtt.Client()

def read_cpu_temperature():
    """Reads the CPU temperature of the Raspberry Pi."""
    try:
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as file:
            temp_raw = file.read().strip()
            # Convert millidegree Celsius to Celsius
            return float(temp_raw) / 1000.0
    except FileNotFoundError:
        print("Could not read CPU temperature. Ensure this is running on a Raspberry Pi.")
        return None

def publish_cpu_temperature():
    """Reads CPU temperature and publishes it to the MQTT broker."""
    cpu_temp = read_cpu_temperature()
    if cpu_temp is not None:
        payload = {
            "cpu_temperature": round(cpu_temp, 2),
            "unit": "Celsius"
        }
        mqtt_client.publish(MQTT_TOPIC_CPU_TEMPERATURE, str(payload))
        print(f"Published: {payload} to topic {MQTT_TOPIC_CPU_TEMPERATURE}")
    else:
        print("No data to publish")

def main():
    # Connect to the MQTT broker
    mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
    mqtt_client.loop_start()

    try:
        while True:
            publish_cpu_temperature()
            time.sleep(5)  # Publish every 5 seconds
    except KeyboardInterrupt:
        print("Exiting...")
        mqtt_client.loop_stop()
        mqtt_client.disconnect()

if __name__ == "__main__":
    main()