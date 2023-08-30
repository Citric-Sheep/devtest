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
    current_movement: int
    demand_type: Optional[int] = None


class ElevatorUpdate(BaseModel):
    elevator_id: int
    current_floor: int
    current_movement: int
    request_id: Optional[int] = None


class ElevatorStatus(BaseModel):
    elevator_id: int
    current_floor: int
    destination_floor: int
