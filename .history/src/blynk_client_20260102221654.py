import BlynkLib, os
import requests
from config import BLYNK_TOKEN

blynk = BlynkLib.Blynk(BLYNK_TOKEN)

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
