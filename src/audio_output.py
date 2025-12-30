import os
import shutil
import subprocess
import tempfile
from typing import Optional, List


def _run(command: List[str], timeout_sec: int) -> None:
    subprocess.run(command, check=True, timeout=timeout_sec)


def _generate_with_espeak(
    text: str,
    wav_path: str,
    speed_wpm: int,
    pitch: int,
    voice: Optional[str],
    timeout_sec: int,
) -> bool:
    if shutil.which("espeak") is None:
        return False

    command: List[str] = ["espeak", "-w", wav_path, "-s", str(speed_wpm), "-p", str(pitch)]
    if voice:
        command.extend(["-v", voice])
    command.append(text)
    try:
        _run(command, timeout_sec)
        return True
    except Exception as exc:
        print(f"[Audio] espeak failed: {exc}")
        return False


def _generate_with_pico2wave(
    text: str,
    wav_path: str,
    language: str,
    timeout_sec: int,
) -> bool:
    if shutil.which("pico2wave") is None:
        return False

    command: List[str] = ["pico2wave", "-l", language, "-w", wav_path, text]
    try:
        _run(command, timeout_sec)
        return True
    except Exception as exc:
        print(f"[Audio] pico2wave failed: {exc}")
        return False


def speak(text):
    return speak_extended(text)

def speak_extended(
    text: str,
    *,
    speed_wpm: int = 160,                # espeak words per minute
    pitch: int = 50,                     # espeak pitch (0-99)
    voice: Optional[str] = None,         # espeak voice, e.g., "en-us+m3"
    language: str = "en-US",             # pico2wave language, e.g., "en-US"
    play_device: Optional[str] = None,   # ALSA device, e.g., "default" or "plughw:1,0"
    tts_timeout_sec: int = 10,
    play_timeout_sec: int = 10,
) -> bool:
    print(f"[SPEAKING] {text}")

    if shutil.which("aplay") is None:
        print("[Audio] aplay not found on system PATH")
        return False

    wav_path: str = ""
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            wav_path = tmp.name

        generated: bool = _generate_with_espeak(
            text=text,
            wav_path=wav_path,
            speed_wpm=speed_wpm,
            pitch=pitch,
            voice=voice,
            timeout_sec=tts_timeout_sec,
        )
        if not generated:
            generated = _generate_with_pico2wave(
                text=text,
                wav_path=wav_path,
                language=language,
                timeout_sec=tts_timeout_sec,
            )
        if not generated:
            print("[Audio] No available TTS engine (espeak/pico2wave).")
            return False

        play_cmd: List[str] = ["aplay"]
        if play_device:
            play_cmd.extend(["-D", play_device])
        play_cmd.append(wav_path)

        try:
            _run(play_cmd, play_timeout_sec)
            return True
        except Exception as exc:
            print(f"[Audio] aplay failed: {exc}")
            return False
    finally:
        try:
            if wav_path and os.path.exists(wav_path):
                os.remove(wav_path)
        except Exception:
            pass
