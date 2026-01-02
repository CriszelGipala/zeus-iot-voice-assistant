import json, queue, time
import sounddevice as sd
from vosk import Model, KaldiRecognizer
from datetime import datetime
import difflib

from audio_output import speak
from config import WAKE_PHRASE, AUDIO_DEVICE_INDEX, VOSK_MODEL_DIR

q = queue.Queue()

def callback(indata, *_):
    q.put(bytes(indata))

def main():
    print(f"[Wake] '{WAKE_PHRASE}' | mic={AUDIO_DEVICE_INDEX}")

    model = Model(VOSK_MODEL_DIR)
    sr = int(sd.query_devices(AUDIO_DEVICE_INDEX, "input")["default_samplerate"])

    wake = KaldiRecognizer(model, sr, json.dumps([WAKE_PHRASE]))
    cmd  = KaldiRecognizer(model, sr)

    mode = "wake"
    last = suppress = 0
    deadline = 0

    def say(text, delay=0.6):
        nonlocal suppress
        speak(text)
        suppress = time.time() + delay

    def wake_mode():
        nonlocal mode
        mode = "wake"
        cmd.Reset()

    def cmd_mode():
        nonlocal mode, deadline
        mode = "cmd"
        deadline = time.time() + 20
        wake.Reset()

    with sd.RawInputStream(
        device=AUDIO_DEVICE_INDEX,
        samplerate=sr,
        blocksize=8000,
        dtype="int16",
        channels=1,
        callback=callback
    ):
        print("Listening for wake word...")
        while True:
            data = q.get()
            now = time.time()
            if now < suppress:
                continue

            rec = wake if mode == "wake" else cmd

            if rec.AcceptWaveform(data):
                text = json.loads(rec.Result()).get("text", "").lower().strip()
                if not text:
                    continue
                print(f"FINAL({mode}):", text)

                if mode == "wake":
                    if WAKE_PHRASE in text and now - last > 3:
                        last = now
                        say("How can I help you?", 1.0)
                        cmd_mode()

                else:
                    if WAKE_PHRASE in text:
                        say("How can I help you?")
                        deadline = time.time() + 20
                    elif is_end(text):
                        say("No problem.")
                        wake_mode()
                    else:
                        handle_command(text)
                        deadline = time.time() + 20
                        suppress = time.time() + 0.6
                        cmd.Reset()

            else:
                partial = json.loads(rec.PartialResult()).get("partial", "")
                if partial:
                    print(f"PARTIAL({mode}):", partial)
                    if mode == "cmd":
                        deadline = time.time() + 20
                        if WAKE_PHRASE in partial:
                            say("How can I help you?")
                if mode == "cmd" and time.time() > deadline:
                    say("Okay.")
                    wake_mode()

# ---------------- helpers ----------------

def handle_command(text):
    try:
        from sensors import get_temperature, get_humidity
    except Exception:
        get_temperature = get_humidity = None

    try:
        from ai_client import ask_ai, ai_fallback_response
    except Exception:
        ask_ai = ai_fallback_response = None

    if "time" in text:
        speak(datetime.now().strftime("The time is %I:%M %p").lstrip("0"))
        return

    if wants_humidity(text) and "temp" in text:
        if get_temperature and get_humidity:
            speak(f"The temperature is {get_temperature():.1f} degrees Celsius and humidity {get_humidity():.0f} percent.")
        else:
            speak("Sensors are unavailable.")
        return

    if "temp" in text:
        speak(f"The temperature is {get_temperature():.1f} degrees Celsius." if get_temperature else "Temperature unavailable.")
        return

    if wants_humidity(text):
        speak(f"The humidity is {get_humidity():.0f} percent." if get_humidity else "Humidity unavailable.")
        return

    if ask_ai:
        try:
            reply = ask_ai(text)
            if reply:
                speak(reply)
                return
        except Exception:
            pass

    speak(ai_fallback_response() if ai_fallback_response else "I'm not available right now.")

def is_end(t):
    return any(w in t for w in (
        "stop","cancel","thanks","thank you","goodbye","exit","quit","that's all"
    ))

def wants_humidity(t):
    if any(w in t for w in ("humid","humidity","moisture","rh")):
        return True
    return difflib.SequenceMatcher(None, t, "humidity").ratio() > 0.75

if __name__ == "__main__":
    main()
