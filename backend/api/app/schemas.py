import uuid
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict


class DeviceResponse(BaseModel):
    id: uuid.UUID
    name: str
    status: str

    class Config:
        from_attributes = True


class TelemetryResponse(BaseModel):
    id: UUID
    device_id: UUID
    latitude: float
    longitude: float
    speed: float
    fuel_level: float
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)