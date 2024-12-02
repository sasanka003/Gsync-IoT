from fastapi import APIRouter, HTTPException
from models.sensor_data import SensorData
from services.sensor_service import save_sensor_data

router = APIRouter(
    prefix="/api",
    tags=["sensors"]
)

@router.post("/sensors")
async def add_sensor_data(sensor_data: SensorData):
    try:
        return save_sensor_data(sensor_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
