import BlynkLib, os
import requests
from config import BLYNK_TOKEN
from time import time, sleep

blynk = BlynkLib.Blynk(BLYNK_TOKEN)

INACTIVITY_TIMEOUT = 30
blynk.last_activity = time()

@blynk.on("V1")
def handle_v1_write(value):
    button_value = value[0]
    blynk.last_activity = time.time()
    print(f'Current button value: {button_value}')


def trigger_event(event_code: str, description: str = "") -> None:
    if not BLYNK_TOKEN:
        return  # Not configured yet

    # Blynk new platform: Events -> logEvent
    url = "https://blynk.cloud/dashboard/160133/templates/311759/events"
    params = {
        "token": BLYNK_TOKEN,
        "event": event_code,
        "description": description
    }
    try:
        requests.get(url, params=params, timeout=5)
    except Exception:
        pass
