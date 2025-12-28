import json
import queue
import time
import sounddevice as sd
from vosk import Model, KaldiRecognizer

from config import VOSK_MODEL_DIR, AUDIO_DEVICE_INDEX

audio_q = queue.Queue()

def callback(indata, frames, time_info, status):
    audio_q.put(indata.copy())

def listen_for_command(seconds: int = 4) -> str:
    model = Model(VOSK_MODEL_DIR)

    device_info = sd.query_devices(AUDIO_DEVICE_INDEX, "input")
    samplerate = int(device_info["default_samplerate"])
    recognizer = KaldiRecognizer(model, samplerate)

    end_time = time.time() + seconds

    with sd.InputStream(
        device=AUDIO_DEVICE_INDEX,
        channels=1,
        samplerate=samplerate,
        callback=callback,
    ):
        while time.time() < end_time:
            data = audio_q.get()
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                text = result.get("text", "").lower().strip()
                if text:
                    return text

    # If nothing finalised, try partial:
    partial = json.loads(recognizer.PartialResult()).get("partial", "").lower().strip()
    return partial
