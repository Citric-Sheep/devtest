##############
# libraries #
##############

from pydantic import BaseModel
from typing import Optional

#################################


class ElevatorDemand(BaseModel):
    elevator_id: int
    demand_category: int
    current_floor: int
    destination_floor: int
    demand_type: Optional[int]


class ElevatorStatus(BaseModel):
    elevator_id: int
    current_floor: int
    destination_floor: int
