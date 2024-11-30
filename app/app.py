from fastapi import FastAPI
from app.routers import sensors

app = FastAPI()

app.include_router(sensors.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Sensor Data API"}
