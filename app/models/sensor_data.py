from pydantic import BaseModel
from datetime import datetime

class SensorData(BaseModel):
    temperature: float
    humidity: float
    nh3_level: float
    co2_level: float
    created_at: datetime
