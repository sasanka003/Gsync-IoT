from pydantic import BaseModel, Field
from pydantic.types import UUID
from datetime import datetime

class SensorData(BaseModel):
    sensor_id: int
    temperature: float
    humidity: float
    nh3_level: float
    co2_level: float

class SensorResponse(BaseModel):
    id: int
    sensor_id: int
    temperature: float
    humidity: float
    nh3_level: float
    co2_level: float

# Response Model for Retrieving Image Data
class ImageResponse(BaseModel):
    image_id: int = Field(..., description="Unique identifier of the image record")
    image_url: str = Field(..., description="URL of the image media")
    sensor_id: int = Field(..., description="ID of the sensor")
    plantation_id: int = Field(..., description="ID of the plantation")
    created_at: datetime = Field(..., description="Timestamp of the image capture")