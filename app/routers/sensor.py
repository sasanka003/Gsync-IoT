from fastapi import APIRouter, HTTPException
from app.models.sensor_data import SensorData
from app.services.sensors_service import save_sensor_data

router = APIRouter(
    prefix="/api",
    tags=["sensors"]
)

@router.post("/sensors")
async def add_sensor_data(sensor_data: SensorData):
    try:
        response = save_sensor_data(sensor_data)
        if response.get("status_code") == 201:
            return {"message": "Sensor data added successfully"}
        else:
            raise HTTPException(status_code=400, detail=response.get("message"))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
