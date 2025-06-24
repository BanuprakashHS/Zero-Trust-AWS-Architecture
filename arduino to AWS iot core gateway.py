import time
import serial
import paho.mqtt.client as mqtt
import ssl
import json

# Serial port configuration
arduino_port = "COM3"  # Update to match your system
baud_rate = 9600
try:
    arduino = serial.Serial(arduino_port, baud_rate)
    print("✅ Successfully connected to Arduino.")
except Exception as e:
    print(f"❌ Failed to connect to Arduino: {e}")
    exit()

# AWS IoT Core configuration
aws_endpoint = "my aws iot core end point "
port = 8883
ca_path = r"C:\Users\banuprakash\Desktop\ZTA\Zero Trust\AmazonRootCA.pem"
cert_path = r"C:\Users\banuprakash\Desktop\ZTA\Zero Trust\ ####### certificate.pem.crt"
key_path = r"C:\Users\banuprakash\Desktop\ZTA\Zero Trust\ #### -private.pem.key"
mqtt_topic = "SensorData"

# MQTT client setup
client = mqtt.Client()
client.enable_logger()

try:
    client.tls_set(
        ca_certs=ca_path,
        certfile=cert_path,
        keyfile=key_path,
        cert_reqs=ssl.CERT_REQUIRED,
        tls_version=ssl.PROTOCOL_TLSv1_2,
    )
    print("✅ TLS configuration set successfully.")
except Exception as e:
    print(f"❌ Failed to configure TLS: {e}")
    exit()

# Connection status
connected = False
def on_connect(client, userdata, flags, rc):
    global connected
    if rc == 0:
        print("✅ Connected to AWS IoT Core")
        connected = True
    else:
        print(f"❌ Failed to connect, return code {rc}")

client.on_connect = on_connect

try:
    client.connect(aws_endpoint, port, keepalive=60)
except Exception as e:
    print(f"❌ Failed to connect to AWS IoT Core: {e}")
    exit()

client.loop_start()

# Wait until connected
print("⏳ Waiting for MQTT connection...")
while not connected:
    time.sleep(1)

# Main loop to read and publish sensor data
try:
    while True:
        if arduino.in_waiting > 0:
            raw_data = arduino.readline().decode("utf-8").strip()
            print(f"📥 Raw data from Arduino: {raw_data}")
            try:
                sensor_type, reading, units = raw_data.split(",")

                payload = {
                    "SensorID": sensor_type,
                    "TS": int(time.time()),
                    "Reading": float(reading),
                    "Units": units
                }

                payload_json = json.dumps(payload)

                result = client.publish(mqtt_topic, payload_json)
                status = result.rc

                if status == 0:
                    print(f"✅ Published: {payload_json}")
                else:
                    print(f"❌ Failed to publish message, error code: {status}")
            except ValueError:
                print(f"⚠️ Invalid data format: {raw_data}")
        time.sleep(1)
except KeyboardInterrupt:
    print("🔚 Exiting gracefully...")
finally:
    client.loop_stop()
    arduino.close()
    print("🛑 Closed connections.")
