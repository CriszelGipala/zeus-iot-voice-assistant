# src/mic_test.py
import sounddevice as sd
import numpy as np
from config import AUDIO_DEVICE_INDEX

duration = 3
samplerate = int(sd.query_devices(AUDIO_DEVICE_INDEX, "input")["default_samplerate"])

print("Recording...")
audio = sd.rec(
    int(duration * samplerate),
    samplerate=samplerate,
    channels=1,
    device=AUDIO_DEVICE_INDEX,
    dtype="int16"
)
sd.wait()
print("Finished recording")

print("Playing back...")
sd.play(audio, samplerate)
sd.wait()
