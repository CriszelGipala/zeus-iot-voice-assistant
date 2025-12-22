import requests
from config import THINGSPEAK_WRITE_KEY

def send_temp_humidity(temp: float, humidity: float) -> None:
    if not THINGSPEAK_WRITE_KEY:
        return  # Not configured yet

    url = "https://api.thingspeak.com/update"
    params = {
        "api_key": THINGSPEAK_WRITE_KEY,
        "field1": round(temp, 2),
        "field2": round(humidity, 2),
    }
    try:
        requests.get(url, params=params, timeout=5)
    except Exception:
        pass
