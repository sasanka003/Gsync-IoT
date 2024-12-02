from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from database.sensor_data import SensorData, SensorResponse, ImageResponse
from services.sensor_service import save_sensor_data, upload_image
from database.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/api",
    tags=["sensors"]
)

@router.post("/sensors", description="add sensor data", response_model=SensorResponse)
async def add_sensor_data(sensor_data: SensorData):
    try:
        return save_sensor_data(sensor_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post('/save_image', description="save camera image from sensor kit", response_model=ImageResponse)
async def upload_sensor_image(
    file: UploadFile = File(...),
    sensor_id: int = Form(...),
    db: Session = Depends(get_db)
):
    return await upload_image(db, file, sensor_id)
