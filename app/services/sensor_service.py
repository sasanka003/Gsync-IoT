from app.database import supabase
from app.models.sensor_data import SensorData

def save_sensor_data(sensor_data: SensorData):
    data = sensor_data.dict()
    response = supabase.table("sensors").insert(data).execute()
    return response
