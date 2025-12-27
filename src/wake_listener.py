# src/wake_listener.py
import json
import queue
import sounddevice as sd
from vosk import Model, KaldiRecognizer

from audio_output import speak
from config import WAKE_PHRASE, AUDIO_DEVICE_INDEX, VOSK_MODEL_DIR

q = queue.Queue()

def callback(indata, frames, time, status):
    q.put(bytes(indata))

def main():
    print(f"[Wake] Using wake phrase: '{WAKE_PHRASE}'")
    print(f"[Wake] Using mic device index: {AUDIO_DEVICE_INDEX}")
    print(f"[Wake] Using Vosk model dir: {VOSK_MODEL_DIR}")

    model = Model(VOSK_MODEL_DIR)
    device = sd.query_devices(AUDIO_DEVICE_INDEX, "input")
    samplerate = int(device["default_samplerate"])

    # Bias recognition strongly toward the wake phrase
    wake_grammar = json.dumps([WAKE_PHRASE])
    recognizer = KaldiRecognizer(model, samplerate, wake_grammar)

    with sd.RawInputStream(
        device=AUDIO_DEVICE_INDEX,
        samplerate=samplerate,
        blocksize=8000,
        dtype="int16",
        channels=1,
        callback=callback
    ):
        while True:
            data = q.get()

            if recognizer.AcceptWaveform(data):
                text = json.loads(recognizer.Result()).get("text", "").lower()
                print("FINAL:", text)

                if WAKE_PHRASE in text:
                    print("Wake phrase detected!")
                    speak("How can I help you?")
                    return

            else:
                partial = json.loads(recognizer.PartialResult()).get("partial", "")
                if partial:
                    print("PARTIAL:", partial)


if __name__ == "__main__":
    main()
