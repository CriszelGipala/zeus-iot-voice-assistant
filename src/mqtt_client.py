import json
import time
import paho.mqtt.client as mqtt
from config import MQTT_BROKER, MQTT_PORT, MQTT_BASE

def publish(topic: str, payload: dict) -> None:
    client = mqtt.Client()
    client.connect(MQTT_BROKER, MQTT_PORT, 60)

    payload = dict(payload)
    payload["ts"] = time.time()

    client.publish(f"{MQTT_BASE}/{topic}", json.dumps(payload))
    client.disconnect()