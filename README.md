# Zeus IoT Voice Assistant

Zeus is a small, offline-capable voice assistant built for **Raspberry Pi**, designed as a learning and portfolio project for IoT, embedded systems, and voice interfaces.

It combines **offline speech recognition**, **sensor readings**, and **cloud notifications**, while remaining functional even without an internet connection.

---

## 🎥 Demo Video
▶️ **YouTube:**  
https://www.youtube.com/shorts/L1Sjp0GxqyI
> The demo shows:
> - Wake phrase detection (`hey zeus`)
> - Speech-to-text processing (offline)
> - Spoken responses via speaker
> - Temperature & humidity queries
> - Blynk and ThingSpeak integrations

---

## Overview

- **Wake phrase:** `hey zeus`
- **Speech-to-Text (STT):** Vosk (offline)
- **Text-to-Speech (TTS):** eSpeak (with pico2wave fallback)
- **Audio playback:** ALSA (`aplay`)
- **Sensors:** Sense HAT (temperature & humidity)
- **Notifications:** Blynk Cloud (Events)
- **Email alerts:** ThingSpeak React
- **Platform:** Raspberry Pi OS

---

## Features

- Offline wake-word and command recognition  
- Cooldown logic to prevent repeated wake triggers  
- Spoken responses using on-device TTS  
- Temperature and humidity readings via Sense HAT  
- Email alerts using ThingSpeak React rules  
- Push notifications using Blynk Events  
- Graceful fallback when sensors or cloud services are unavailable  

## Project Structure (simplified)
src/
- main.py                       # Entry point
- wake_listener.py              # Wake word + command logic
- audio_output.py               # Text-to-speech playback
- sensors.py                    # Sense HAT readings
- blynk_client.py               # Blynk event notifications
- thingspeak_client.py          # ThingSpeak updates
- config.py                     # Environment-based configuration

## Quick Start

### 1. System Dependencies (Raspberry Pi OS)
``` bash
sudo apt update
sudo apt install -y python3-env espeak libttspico-utils alsa-utils
```
---

### 2. Python Environment
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install sounddevice vosk sense-hat python-dotenv requests paho-mqtt 


### 3. Download Vosk Model
Download a Vosk English model and place in the models/ directory (Default used below: vosk-model-small-en-us-0.15)

### 4. Configuration (.env)
Create a .env file in the project root:
WAKE_PHRASE=hey zeus
VOSK_MODEL_DIR=models/vosk-model-small-en-us-0.15
AUDIO_DEVICE_INDEX=1

BLYNK_TOKEN=DvXFD1-kRcdtF2HZh4pWVEj8BkvBYmAR
THINGSPEAK_WRITE_KEY=ALZMOXQ5S5ULTMM

To list audio devices and find the correct microphone index:
python -c "import sounddevice as sd; print(sd.query_devices())

### 5. Run the assistant
pythhon src/main.py


## Contact
For questions, feedback, or collaborations:
- Preferred contact: Github
- Please open an Issue or Pull Request in this repository

