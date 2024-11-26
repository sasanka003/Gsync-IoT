from sensors import read_dht22, read_mq135
from mqtt_client import publish_data
from database import insert_data_to_supabase
import time

def main():
    while True:
        try:
            # Read sensor data
            humidity, temperature = read_dht22()
            co2_level = read_mq135()
            
            # Prepare data payload
            data = {
                "temperature": temperature,
                "humidity": humidity,
                "co2_level": co2_level,
                "timestamp": time.strftime('%Y-%m-%d %H:%M:%S')
            }

            # Publish to MQTT broker
            publish_data(data)

            # Insert into Supabase
            insert_data_to_supabase(data)

            print(f"Data: {data}")

            # Wait before next read
            time.sleep(10)

        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
