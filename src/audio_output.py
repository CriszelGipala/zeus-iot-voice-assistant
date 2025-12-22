import subprocess

def speak(text):
    subprocess.run(['espeak', text])