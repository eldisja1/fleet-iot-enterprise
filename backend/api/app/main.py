from fastapi import FastAPI
from app.routers import devices_router, telemetry_router

app = FastAPI(title="Fleet IoT Enterprise API")

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(devices_router)
app.include_router(telemetry_router)