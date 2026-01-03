from wake_listener import main as wake_main
try:
    # Start Blynk in background so device is online while assistant runs
    from blynk_client import start_blynk  # type: ignore
except Exception:
    start_blynk = None  # type: ignore

if __name__ == "__main__":
    if start_blynk:
        start_blynk()
    wake_main()