from sense_hat import SenseHat

sense = SenseHat()

def get_temperature() -> float:
    return sense.get_temperature()

def get_humidity() -> float:
    return sense.get_humidity()
