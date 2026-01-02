import BlynkLib, os, subprocess
import requests
from config import BLYNK_TOKEN
from time import time, sleep
from sense_hat import SenseHat
from threading import Thread, Event

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
    else:
        assistant_enabled = False
        sense.clear()

@blynk.on("V2")
def handle_shutdown(value):
    """
    V2 button: when pressed (value '1'), shutdown the Raspberry Pi.
    Requires passwordless sudo for /sbin/shutdown.
    """
    try:
        pressed = str(value[0]).strip() in ("1", "on", "true")
    except Exception:
        pressed = False
    if pressed:
        print("[Blynk] Shutdown requested via V2")
        # Non-blocking to allow print to flush
        subprocess.Popen(["sudo", "shutdown", "-h", "now"])

@blynk.on("V3")
def handle_reboot(value):
    """
    V3 button: when pressed (value '1'), reboot the Raspberry Pi.
    Requires passwordless sudo for /sbin/reboot.
    """
    try:
        pressed = str(value[0]).strip() in ("1", "on", "true")
    except Exception:
        pressed = False
    if pressed:
        print("[Blynk] Reboot requested via V3")
        subprocess.Popen(["sudo", "reboot"])

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