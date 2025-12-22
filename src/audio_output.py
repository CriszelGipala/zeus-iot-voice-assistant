import subprocess

def speak(text: str) -> None:
    # espeak is simple and reliable on Pi
    subprocess.run(["espeak", text], check=False)
