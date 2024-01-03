from datetime import datetime
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Enum
from sqlalchemy.orm import relationship

from .database import Base
from .schemas import EventType


class Elevator(Base):
    __tablename__ = "elevators"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(String)
    building_id = Column(String)
    device_id = Column(Integer, ForeignKey("devices.id"), unique=True)
    is_active = Column(Boolean)

    events = relationship("Event", back_populates="elevator")
    predictions = relationship("Prediction", back_populates="elevator")
    device = relationship("Device", back_populates="elevator", uselist=False)


class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    model = Column(String)
    firmware_version = Column(String)
    last_update = Column(DateTime)

    elevator = relationship("Elevator", back_populates="device")


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(Enum(EventType))
    current_floor = Column(Integer)
    target_floor = Column(Integer)
    load = Column(Integer)
    is_vacant = Column(Boolean)
    captured_at = Column(DateTime)
    inserted_at = Column(DateTime, default=datetime.utcnow)

    elevator_id = Column(Integer, ForeignKey("elevators.id"))
    elevator = relationship("Elevator", back_populates="events")



class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    resting_floor = Column(Integer)
    inserted_at = Column(DateTime)

    elevator_id = Column(Integer, ForeignKey("elevators.id"))
    elevator = relationship("Elevator", back_populates="predictions")