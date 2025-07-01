from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional

# Elevator schemas
class ElevatorBase(BaseModel):
    """Base schema for elevator data."""
    building_id: int = Field(..., description="Building identifier")
    max_floor: int = Field(..., description="Maximum floor the elevator can reach")
    min_floor: int = Field(..., description="Minimum floor the elevator can reach")

class ElevatorCreate(ElevatorBase):
    """Schema for creating a new elevator."""
    pass

class Elevator(ElevatorBase):
    """Schema for elevator response including database fields."""
    id: int

    class Config:
        orm_mode = True

# Elevator demand schemas
class ElevatorDemandBase(BaseModel):
    """Base schema for elevator demand data."""
    floor: int = Field(..., description="Floor where the demand originated")
    direction: str = Field(..., description="Direction of travel ('up' or 'down')")
    elevator_id: int = Field(..., description="ID of the elevator that responded to this demand")

class ElevatorDemandCreate(ElevatorDemandBase):
    """Schema for creating a new elevator demand."""
    pass

class ElevatorDemand(ElevatorDemandBase):
    """Schema for elevator demand response including database fields."""
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True

# Analytics schemas
class DemandAnalytics(BaseModel):
    """Schema for demand analytics response."""
    floor: int
    count: int
    
class TimeBasedDemandAnalytics(BaseModel):
    """Schema for time-based demand analytics."""
    hour: int
    floor: int
    count: int
    
class FloorDirectionAnalytics(BaseModel):
    """Schema for floor-direction distribution analytics."""
    floor: int
    up_count: int
    down_count: int
