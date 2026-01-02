from blynk_client import trigger_event
from config import BLYNK_EVENT_WAKE

trigger_event(BLYNK_EVENT_WAKE, "Manual test from Raspberry Pi")
print("Blynk event sent")
