import json
import queue
import sounddevice as sd
from vosk import Model, KaldiRecognizer

from config import WAKE_PHRASE, VOSK_MODEL_DIR, AUDIO_DEVICE_INDEX
from audio_output import speak


audio_q = queue.Queue()

def callback(indata, frames, time, status):
    volume = abs(indata).mean()
    print(f"Mic level: {volume:.4f}")
    audio_q.put(bytes(indata))


def listen_for_wake():
    device_info = sd.query_devices(AUDIO_DEVICE_INDEX, "input")
    samplerate = int(device_info["default_samplerate"])

    recognizer = KaldiRecognizer(model, samplerate)


    with sd.InputStream(
    device=AUDIO_DEVICE_INDEX,
    channels=1,
    samplerate=samplerate,
    callback=callback,
):

        print("Listening for wake phrase:", WAKE_PHRASE)

        while True:
            data = audio_q.get()
            if recognizer.AcceptWaveform(data):
                text = json.loads(recognizer.Result()).get("text", "").lower()
                if WAKE_PHRASE in text:
                    print("Wake phrase detected!")
                    speak("How can I help you?")
                    return

if __name__ == "__main__":
    listen_for_wake()