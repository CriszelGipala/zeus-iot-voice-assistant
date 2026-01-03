import BlynkLib, subprocess
from config import BLYNK_TOKEN
from time import time, sleep
from sense_hat import SenseHat
from threading import Thread, Event
from thingspeak_client import send_switch


sense = SenseHat()
sense.clear()

blynk = BlynkLib.Blynk(BLYNK_TOKEN)

_stop_event = Event()
assistant_enabled = True

def is_assistant_enabled() -> bool:
    return assistant_enabled

@blynk.on("V1")
def handle_v1_write(value):
    global assistant_enabled
    button_value = int(value[0])
    print(f'Current button value: {button_value}')

    if button_value == 1:
        assistant_enabled = True
        sense.clear(255,255,255)
        send_switch(1)
    else:
        assistant_enabled = False
        sense.clear()
        send_switch(0)

def _blynk_loop():
    print("Blynk thread started. Listening for events...")
    try:
        while not _stop_event.is_set():
            blynk.run()  # Process Blynk events
            # Example telemetry: Sense HAT temperature on virtual pin V0
            try:
                blynk.virtual_write(0, sense.get_temperature())
            except Exception:
                pass
            sleep(2)  # Add a short delay to avoid high CPU usage
    except KeyboardInterrupt:
        print("Blynk thread interrupted.")

def start_blynk() -> Thread:
    """Start Blynk processing in a background thread."""
    t = Thread(target=_blynk_loop, daemon=True)
    t.start()
    return t

def stop_blynk() -> None:
    """Signal the background Blynk thread to stop."""
    _stop_event.set()

# Main loop to keep the Blynk connection alive and process events standalone
if __name__ == "__main__":
    t = start_blynk()
    try:
        # Keep the main thread alive while the background thread runs
        while t.is_alive():
            t.join(timeout=1.0)
    except KeyboardInterrupt:
        stop_blynk()
        print("Blynk application stopped.")
