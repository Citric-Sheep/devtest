from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ElevatorCreate(BaseModel):
    name: str
    
class Elevator(BaseModel):
    id: int
    name: str
    class Config:
        orm_mode = True
        
class DemandCreate(BaseModel):
    elevator_id: int
    floor: int
    timestamp: datetime
    direction: str
    
class Demand(BaseModel):
    id: int
    elevator_id: int
    floor: int
    timestamp: datetime
    direction: str
    surge_tag: bool
    class Config:
        orm_mode = True
        
class RestingCreate(BaseModel):
    elevator_id: int
    floor: int
    start_time: datetime
    
class RestingEnd(BaseModel):
    end_time: datetime
    
class RestingPeriod(BaseModel):
    id: int
    elevator_id: int
    floor: int
    start_time: datetime
    end_time: Optional[datetime]
    duration_sec: Optional[int]
    peak_hours_flag: bool
    relocation_flag: bool
    non_optimal_rested: bool
    class Config:
        orm_mode = True 