import os
from dotenv import load_dotenv

load_dotenv()

WAKE_PHRASE = os.getenv("WAKE_PHRASE", "hey laika").strip().lower()
VOSK_MODEL_DIR = os.getenv("VOSK_MODEL_DIR", "models/vosk-model-small-en-us-0.15").strip()

AUDIO_DEVICE_INDEX = int(os.getenv("AUDIO_DEVICE_INDEX", "1"))

MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost").strip()
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
MQTT_BASE = os.getenv("MQTT_BASE", "laika").strip()

THINGSPEAK_WRITE_KEY = os.getenv("THINGSPEAK_WRITE_KEY", "").strip()

BLYNK_TOKEN = os.getenv("BLYNK_TOKEN", "").strip()
BLYNK_EVENT_WAKE = os.getenv("BLYNK_EVENT_WAKE", "wake_detected").strip()

AI_API_URL = os.getenv("AI_API_URL", "").strip()
AI_API_KEY = os.getenv("AI_API_KEY", "").strip()
