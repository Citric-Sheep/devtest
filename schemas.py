"""
Modelos Pydantic
"""

from pydantic import BaseModel
from datetime import datetime


class ElevatorGet(BaseModel):
    time_stamp: datetime
    prev_resting_floor: int
    whos_calling: int
    where_to: int
    resting_floor: int


class ElevatorState(BaseModel):
    resting_floor: int


class ElevatorCall(ElevatorState):
    time_stamp: datetime
    whos_calling: int
    where_to: int
