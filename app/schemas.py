from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ElevatorMovementBase(BaseModel):
    timestamp: datetime
    elevator_id: int
    current_floor: int
    next_floor: Optional[int]
    action: str
    expected_arrival_time: Optional[datetime]  # Nuevo campo

class ElevatorMovementCreate(ElevatorMovementBase):
    floor_requested: Optional[int]
    # direction: str


class ElevatorMovementUpdate(ElevatorMovementBase):
    pass
#Here we can modify the data in cases where you have a new preferred resting floor so you could change
# The system behaviour for your own pourposes
class ElevatorMovement(ElevatorMovementBase):
    id: int

    class Config:
        orm_mode = True

class DemandBase(BaseModel):
    timestamp: datetime
    floor_requested: int

class DemandCreate(DemandBase):
    pass

class DemandUpdate(DemandBase):
    pass

class Demand(DemandBase):
    id: int

    class Config:
        orm_mode = True
