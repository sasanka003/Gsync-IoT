from database import supabase
from models.sensor_data import SensorData

def save_sensor_data(sensor_data: SensorData):
    data = sensor_data.dict()
    response = supabase.table("sensor_data").insert(data).execute()
    return response
