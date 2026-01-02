import BlynkLib, os
import requests
from config import BLYNK_TOKEN
from time import time, sleep

BLYNK_TOKEN = os.getenv("BLYNK_TOKEN")
blynk = BlynkLib.Blynk(BLYNK_TOKEN)

INACTIVITY_TIMEOUT = 30
blynk.last_activity = time()

@blynk.on("V1")
def handle_v1_write(value):
    button_value = value[0]
    blynk.last_activity = time()
    print(f'Current button value: {button_value}')


# Main loop to keep the Blynk connection alive and process events
if __name__ == "__main__":
    print("Blynk application started. Listening for events...")
    try:
        while True:
            blynk.run()  # Process Blynk events
            now = time()
            # If there's been no activity, break out of loop
            if now - blynk.last_activity > INACTIVITY_TIMEOUT:
                print(f"No activity for {INACTIVITY_TIMEOUT} seconds. Exiting.")
                break
            sleep(2)  # Add a short delay to avoid high CPU usage
    except KeyboardInterrupt:
        print("Blynk application stopped.")