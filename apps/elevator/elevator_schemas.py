##############
# libraries #
##############

from pydantic import BaseModel
from typing import Optional


#################################
# Elevator Demand Schema #
#################################

class ElevatorDemand(BaseModel):
    elevator_id: int
    demand_category: int
    current_floor: int
    destination_floor: int
    current_movement: Optional[int]
    demand_type: Optional[int]


class ElevatorUpdate(BaseModel):
    elevator_id: int
    current_floor: int
    current_movement: int


class ElevatorStatus(BaseModel):
    elevator_id: int
    current_floor: int
    destination_floor: int
