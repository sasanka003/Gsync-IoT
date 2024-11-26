import Adafruit_DHT
import spidev
import time

# Define GPIO pins
DHT_PIN = 4  # Pin connected to DHT22
MQ135_PIN = 17  # ADC pin for MQ-135 (use an ADC if required)

# Define SPI parameters
SPI_CHANNEL = 0  # MCP3008 CH0 is used for MQ-135 sensor
SPI_SPEED_HZ = 1000000  # SPI communication speed

def read_dht22():
    """Read temperature and humidity from DHT22."""
    sensor = Adafruit_DHT.DHT22
    humidity, temperature = Adafruit_DHT.read_retry(sensor, DHT_PIN)
    if humidity is not None and temperature is not None:
        return round(humidity, 2), round(temperature, 2)
    else:
        raise ValueError("Failed to read from DHT22 sensor.")

def read_adc(channel, spi):
    """
    Reads data from the specified ADC channel (0-7).
    """
    if channel < 0 or channel > 7:
        raise ValueError("Invalid ADC channel. Must be between 0 and 7.")

    # Send start bit, single/diff bit, and channel bits (5 bits total)
    adc = spi.xfer2([1, (8 + channel) << 4, 0])

    # Combine the returned bits into a single 10-bit result
    data = ((adc[1] & 3) << 8) + adc[2]
    return data

def convert_to_ppm(adc_value):
    """
    Convert the raw ADC value to CO₂ levels in ppm.
    This is a placeholder function. Calibrate it for accurate readings.
    """
    # Example calibration: Scale raw ADC value to a PPM range
    # Replace with your own calibration logic
    max_adc = 1023  # MCP3008 is a 10-bit ADC
    max_ppm = 1000  # Adjust based on your sensor calibration
    ppm = (adc_value / max_adc) * max_ppm
    return round(ppm, 2)

def read_mq135():
    """
    Reads CO₂ levels from the MQ-135 sensor via MCP3008.
    """
    # Initialize SPI
    spi = spidev.SpiDev()
    spi.open(0, 0)  # Open SPI bus 0, device 0 (CE0)
    spi.max_speed_hz = SPI_SPEED_HZ

    try:
        # Read raw ADC value from CH0
        adc_value = read_adc(SPI_CHANNEL, spi)
        # Convert to CO₂ levels (ppm)
        co2_level = convert_to_ppm(adc_value)
        return co2_level
    finally:
        # Close SPI connection
        spi.close()

