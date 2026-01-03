import requests
from config import THINGSPEAK_WRITE_KEY

def send_switch(state: int) -> None:
    if not THINGSPEAK_WRITE_KEY:
        print("[TS] Missing THINGSPEAK_WRITE_KEY")
        return
    try:
        r = requests.get(
            "https://api.thingspeak.com/update",
            params={"api_key": THINGSPEAK_WRITE_KEY, "field3": int(bool(state))},
            timeout=5,
        )
        print("[TS] update status:", r.status_code, r.text)
    except Exception as e:
        print("[TS] error:", e)