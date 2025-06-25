from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class RestingPeriodBase(BaseModel):
    floor: int
    elevator_id: Optional[int] = 1

class RestingPeriodCreate(RestingPeriodBase):
    resting_start: Optional[datetime] = None 
    resting_end: Optional[datetime] = None

class RestingPeriodRead(RestingPeriodBase):
    id: int
    resting_start: datetime
    resting_end: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
