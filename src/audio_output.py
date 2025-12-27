# src/audio_output.py
import subprocess
import tempfile
import os

def speak(text):
    print(f"[SPEAKING] {text}")

    # Create a temporary wav file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
        wav_path = f.name

    # Use espeak to generate speech (ALSA-friendly)
    try:
        subprocess.run([
            "espeak",
            "-w", wav_path,
            text
        ], check=True)
    except Exception as e:
        print(f"[Audio] espeak failed: {e}")
        # Ensure temp file is removed if created but empty
        try:
            if os.path.exists(wav_path):
                os.remove(wav_path)
        except Exception:
            pass
        return

    # Play via ALSA (this is the IMPORTANT part)
    try:
        subprocess.run([
            "aplay",
            wav_path
        ], check=True)
    except Exception as e:
        print(f"[Audio] aplay failed: {e}")
    finally:
        try:
            os.remove(wav_path)
        except Exception:
            pass
