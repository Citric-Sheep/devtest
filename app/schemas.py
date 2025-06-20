from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ElevatorCreate(BaseModel):
    current_floor: int

class ElevatorStatusUpdate(BaseModel):
    current_floor: int
    is_moving: bool
    is_occupied: bool

class DemandCreate(BaseModel):
    floor_called_from: int

class Event(BaseModel):
    id: int
    elevator_id: int
    event_type: str
    from_floor: Optional[int]
    to_floor: Optional[int]
    timestamp: datetime

    class Config:
        orm_mode = True
