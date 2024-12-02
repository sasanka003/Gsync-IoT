from fastapi import UploadFile
from database.sensor_data import SensorData
from sqlalchemy.orm import Session
import uuid
from datetime import datetime
import time
from database.database import supabase
from database.models import DbSensor, DbSensorImage, DbSensorData

def save_sensor_data(sensor_data: SensorData):
    data = sensor_data.dict()
    response = supabase.table("sensor_data").insert(data).execute()
    return response

async def upload_image(db: Session, file: UploadFile, sensor_id: uuid):
    # Check if the sensor exists
    sensor = db.query(DbSensor).filter(DbSensor.sensor_id == sensor_id).first()
    if not sensor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sensor not found")

    image_content = await file.read()

    file_name = f"{sensor_id}_{int(time.time())}.jpg"

    response = supabase.storage.from_('prediction_imgs').upload(file_name, image_content)
    print(response)

    # if response.status_code != 200:
    #     raise HTTPException(status_code=response.status_code, detail=response.json())
    

    # Extract the file URL from the response
    # file_url = supabase.storage.from_('prediction_imgs').get_public_url(file_name)
    full_path = response.full_path

    if not full_path:
        raise HTTPException(status_code=500, detail="Failed to retrieve file URL from the response")

    # Save the image to the database
    new_image = DbSensorImage(
        image_url=full_path,
        sensor_id=sensor_id,
        plantation_id=sensor.plantation_id,
        created_at=datetime.now()
    )
    db.add(new_image)
    db.commit()
    db.refresh(new_image)

    return new_image
