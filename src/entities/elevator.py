import time
from typing import Optional

from pydantic import BaseModel

from .enumerations.elevator_status import ElevatorStatus


class Elevator(BaseModel):
    actual_floor: int = 0
    going_to: Optional[int] = None
    demand_floors: list[int] = []

    @property
    def demand_is_empty(self):
        return len(self.demand_floors) == 0

    @property
    def status(self):
        if self.demand_is_empty:
            return ElevatorStatus.VACANT.value
        return ElevatorStatus.DEMAND.value

    def press_floor_button(self, floor: int):
        if floor not in self.demand_floors:
            self.demand_floors.append(floor)

    def run(self, seconds_per_floor=1, print_debug=True):
        while not self.demand_is_empty:
            if print_debug:
                self._print_state()

            time.sleep(seconds_per_floor)
            self._evalutate_state()

        if print_debug:
            self._print_state()

    def _next_floor(self):
        if self.demand_is_empty:
            raise Exception("Demand_floors is empty")
        return min(self.demand_floors, key=lambda floor: abs(self.actual_floor - floor))

    def _arrive_to_destination(self):
        if self.going_to in self.demand_floors:
            self.demand_floors.remove(self.going_to)
        self.going_to = None

    def _move_to_floor(self, floor: int):
        if floor > self.actual_floor:
            self.actual_floor += 1
        elif floor < self.actual_floor:
            self.actual_floor -= 1

    def _evalutate_motion(self) -> bool:
        if self.going_to is None:
            raise Exception("Doing_to is None")
        if self.going_to == self.actual_floor:
            self._arrive_to_destination()
            return True

        self._move_to_floor(self.going_to)
        return False

    def _evalutate_state(self):
        if self.demand_is_empty:
            return
        if self.going_to is None:
            self.going_to = self._next_floor()
        self._evalutate_motion()

    def _print_state(self):
        print(
            f"Floor:{self.actual_floor}, GoingTo:{self.going_to}, Demand:{self.demand_floors}, State: {self.status}"
        )
