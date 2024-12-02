from fastapi import FastAPI
from routers import sensor
from scheduler import start_scheduler

app = FastAPI()

# Include Routers
app.include_router(sensor.router)

# Start Scheduler on Application Startup
# @app.on_event("startup")
# def startup_event():
#     start_scheduler()

@app.get("/")
async def root():
    return {"message": "Welcome to the Sensor Data API"}
