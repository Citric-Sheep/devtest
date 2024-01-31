from pydantic import BaseModel
from typing import Optional


class ElevatorCreate(BaseModel):
    current_floor: int
    resting_floor: int
    status: str

class ElevatorResponse(BaseModel):
    id: int
    current_floor: int
    resting_floor: int
    status: str