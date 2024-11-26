import Adafruit_DHT

# Define GPIO pins
DHT_PIN = 4  # Pin connected to DHT22
MQ135_PIN = 17  # ADC pin for MQ-135 (use an ADC if required)

def read_dht22():
    """Read temperature and humidity from DHT22."""
    sensor = Adafruit_DHT.DHT22
    humidity, temperature = Adafruit_DHT.read_retry(sensor, DHT_PIN)
    if humidity is not None and temperature is not None:
        return round(humidity, 2), round(temperature, 2)
    else:
        raise ValueError("Failed to read from DHT22 sensor.")
