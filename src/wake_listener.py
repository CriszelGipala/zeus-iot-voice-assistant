import json
import queue
import time
import sounddevice as sd
from vosk import Model, KaldiRecognizer
from datetime import datetime

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

    # Build two recognizers:
    # 1) Wake recognizer biased to the wake phrase only
    wake_grammar = json.dumps([WAKE_PHRASE])
    wake_recognizer = KaldiRecognizer(model, samplerate, wake_grammar)
    # 2) Command recognizer with full vocabulary
    cmd_recognizer = KaldiRecognizer(model, samplerate)

    cooldown_seconds = 3.0
    last_trigger_time = 0.0
    suppress_until = 0.0
    mode = "wake"  # "wake" or "command"
    command_timeout_seconds = 8.0
    command_deadline = 0.0

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

            now = time.time()
            if now < suppress_until:
                # Ignore mic while we're speaking or shortly after
                continue

            if mode == "wake":
                if wake_recognizer.AcceptWaveform(data):
                    text = json.loads(wake_recognizer.Result()).get("text", "").lower().strip()
                    if text:
                        print("FINAL(wake):", text)
                    if text and WAKE_PHRASE in text and (now - last_trigger_time) >= cooldown_seconds:
                        print("Wake phrase detected!")
                        speak("How can I help you?")
                        last_trigger_time = now
                        # Suppress mic pickup of our own TTS
                        suppress_until = now + 1.0
                        # Switch to command mode
                        mode = "command"
                        command_deadline = now + command_timeout_seconds
                        wake_recognizer.Reset()
                else:
                    # Reduce noise by not spamming partials in wake mode
                    partial = json.loads(wake_recognizer.PartialResult()).get("partial", "")
                    if partial and partial != WAKE_PHRASE:
                        print("PARTIAL(wake):", partial)

            else:
                # Command mode: listen for a short utterance
                if cmd_recognizer.AcceptWaveform(data):
                    text = json.loads(cmd_recognizer.Result()).get("text", "").lower().strip()
                    print("FINAL(command):", text)
                    if text:
                        # Exit phrases end the conversation and return to wake mode
                        if _is_end_of_conversation(text):
                            speak("Okay.")
                            mode = "wake"
                            cmd_recognizer.Reset()
                            suppress_until = time.time() + 0.6
                        else:
                            _handle_command(text)
                            # Stay in conversation; extend deadline for next question
                            command_deadline = time.time() + command_timeout_seconds
                            cmd_recognizer.Reset()
                            suppress_until = time.time() + 0.6
                    else:
                        # Nothing recognized; keep listening briefly
                        speak("Sorry, I didn't catch that.")
                        command_deadline = time.time() + command_timeout_seconds
                        cmd_recognizer.Reset()
                        suppress_until = time.time() + 0.4
                else:
                    # Time out if user stays silent
                    if time.time() >= command_deadline:
                        speak("Okay.")
                        mode = "wake"
                        cmd_recognizer.Reset()
                        suppress_until = time.time() + 0.6
                    else:
                        partial = json.loads(cmd_recognizer.PartialResult()).get("partial", "")
                        if partial:
                            print("PARTIAL(command):", partial)


def _handle_command(text: str) -> None:
    """
    Very simple intent handling:
    - Local: time, temperature, humidity
    - Otherwise: try AI API, fall back to canned message
    """
    # Import optional modules lazily to avoid breaking wake mode
    try:
        from sensors import get_temperature, get_humidity  # type: ignore
    except Exception:
        get_temperature = None  # type: ignore
        get_humidity = None  # type: ignore
    try:
        from ai_client import ask_ai, ai_fallback_response  # type: ignore
    except Exception:
        ask_ai = None  # type: ignore
        ai_fallback_response = None  # type: ignore
    if "time" in text:
        now = datetime.now().strftime("%I:%M %p").lstrip("0")
        speak(f"The time is {now}.")
        return

    if "temperature" in text:
        try:
            if get_temperature is None:
                raise RuntimeError("Sensors not available")
            temp_c = get_temperature()
            speak(f"The temperature is {temp_c:.1f} degrees Celsius.")
        except Exception:
            speak("Sorry, I can't read the temperature right now.")
        return

    if "humidity" in text:
        try:
            if get_humidity is None:
                raise RuntimeError("Sensors not available")
            hum = get_humidity()
            speak(f"The humidity is {hum:.0f} percent.")
        except Exception:
            speak("Sorry, I can't read the humidity right now.")
        return

    # Try AI extension if configured
    ai_reply = None
    if ask_ai is not None:
        try:
            ai_reply = ask_ai(text)  # type: ignore
        except Exception:
            ai_reply = None
    if ai_reply:
        speak(ai_reply)
    else:
        if ai_fallback_response is not None:
            speak(ai_fallback_response())  # type: ignore
        else:
            speak("I'm not available right now.")


def _is_end_of_conversation(text: str) -> bool:
    words = (
        "stop",
        "cancel",
        "nevermind",
        "never mind",
        "thank you",
        "thanks",
        "goodbye",
        "go to sleep",
        "that's all",
        "that is all",
        "exit",
        "quit",
    )
    return any(w in text for w in words)


if __name__ == "__main__":
    main()
