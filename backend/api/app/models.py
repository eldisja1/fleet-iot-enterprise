import uuid
from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .database import Base


class Device(Base):
    __tablename__ = "devices"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    status = Column(String, nullable=False)

    telemetry = relationship("Telemetry", back_populates="device", cascade="all, delete")


class Telemetry(Base):
    __tablename__ = "telemetry"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    device_id = Column(UUID(as_uuid=True), ForeignKey("devices.id", ondelete="CASCADE"), nullable=False)

    latitude = Column(Float)
    longitude = Column(Float)
    speed = Column(Float)
    fuel_level = Column(Float)
    status = Column(String(50))

    created_at = Column(DateTime(timezone=False), server_default=func.now())

    device = relationship("Device", back_populates="telemetry")