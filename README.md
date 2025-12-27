# zeus-iot-voice-assistant

Zeus is a voice-activated IoT assistant built using a Raspberry Pi. It listens for a wake phrase ("hey zeus") and responds to a basic commands such as reading sensor data and triggering IoT events.

The system uses offline wake-word detection to recognise the phrase "hey zeus". Once activated, the assistant relies on network connectivity to process commands, publish MQTT events, send mobile notifications via Blynk, and upload sensor data provides appropriate fallback responses.

# Hardware Used
- Raspberry Pi 4B
- USB Microphone
- External Speaker (3.5mm jack)
- Sense HAT

## Hardware Verification
The folowing hardware tests have been completed successfully:
- USB microphone tested using 'arecord'
- Audio playback tested using 'aplay'
- Microphone recording verified by recording and replaying a WAV file
- Speaker output verified using ALSA test sounds

Audio input and output are confirmed working correctly.

## Mobile Notifications
Mobile notifications are implemented using the Blynk platform. A notification is sent to the user's mobile device whenever the wake phrase "hey zeus" is detected. This provides real-time feedback that the system has been activated and demonstrates event-driven IoT communication.

## Project Status
- Repository created
- Python virtual environment set up
- Audio input/output configured and tested
- Ready to integrate speech recognition and wake-word detection
