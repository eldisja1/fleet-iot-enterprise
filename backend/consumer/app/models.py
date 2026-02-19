import uuid
from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from .database import Base


class Device(Base):
    __tablename__ = "devices"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    device_code = Column(String(100), unique=True, nullable=False)
    name = Column(String(255))
    status = Column(String(50), default="offline")

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    telemetry = relationship("Telemetry", back_populates="device")


class Telemetry(Base):
    __tablename__ = "telemetry"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    device_id = Column(
        UUID(as_uuid=True),
        ForeignKey("devices.id", ondelete="CASCADE"),
        nullable=False
    )

    latitude = Column(Float)
    longitude = Column(Float)
    speed = Column(Float)
    fuel_level = Column(Float)
    status = Column(String)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    device = relationship("Device", back_populates="telemetry")
