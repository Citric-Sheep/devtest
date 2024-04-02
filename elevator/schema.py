"""
Pydantic models used in FastAPI endpoints.
"""

from datetime import datetime

from pydantic import BaseModel


class ElevatorCreate(BaseModel):
    name: str


class ElevatorUpdate(BaseModel):
    name: str | None = None


class Elevator(BaseModel, from_attributes=True):
    id: int
    name: str


class ElevatorDemandCreate(BaseModel):
    elevator_id: int
    pressed_at_floor: int
    requested_at: datetime | None = None


class ElevatorDemand(BaseModel, from_attributes=True):
    id: int
    elevator_id: int
    pressed_at_floor: int
    requested_at: datetime
