try:
    from sense_hat import SenseHat  # type: ignore
    _sense = SenseHat()
except Exception:
    _sense = None

def get_temperature() -> float:
    if _sense is None:
        raise RuntimeError("Sense HAT not available")
    return _sense.get_temperature()

def get_humidity() -> float:
    if _sense is None:
        raise RuntimeError("Sense HAT not available")
    return _sense.get_humidity()
