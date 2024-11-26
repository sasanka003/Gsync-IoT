import paho.mqtt.client as mqtt
import json

# MQTT Configuration
BROKER = "broker.emqx.io"
PORT = 1883
TOPIC = "sensors/data"

def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT Broker with result code {rc}")

def on_publish(client, userdata, mid):
    print(f"Message {mid} published successfully.")

def publish_data(data):
    """Publishes sensor data to the MQTT broker."""
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_publish = on_publish

    client.connect(BROKER, PORT, 60)
    client.loop_start()
    message = json.dumps(data)
    client.publish(TOPIC, message)
    client.loop_stop()
    client.disconnect()
