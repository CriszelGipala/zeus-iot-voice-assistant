import BlynkLib, os, subprocess
import requests
from config import BLYNK_TOKEN
from time import time, sleep
from sense_hat import SenseHat

sense = SenseHat()
sense.clear()

BLYNK_TOKEN = os.getenv("BLYNK_TOKEN")
blynk = BlynkLib.Blynk(BLYNK_TOKEN)

INACTIVITY_TIMEOUT = 30
blynk.last_activity = time()

@blynk.on("V1")
def handle_v1_write(value):
    button_value = int(value[0])
    blynk.last_activity = time()
    print(f'Current button value: {button_value}')

    if button_value == 1:
        sense.clear(255,255,255)
    else:
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

# Main loop to keep the Blynk connection alive and process events
if __name__ == "__main__":
    print("Blynk application started. Listening for events...")
    try:
        while True:
            blynk.run()  # Process Blynk events
            blynk.virtual_write(0, sense.get_temperature())
            now = time()
            # If there's been no activity, break out of loop
            if now - blynk.last_activity > INACTIVITY_TIMEOUT:
                print(f"No activity for {INACTIVITY_TIMEOUT} seconds. Exiting.")
                break
            sleep(2)  # Add a short delay to avoid high CPU usage
    except KeyboardInterrupt:
        print("Blynk application stopped.")