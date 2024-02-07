import time
from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from .elevator import Elevator


class DemandLog(BaseModel):
    id: Optional[str] = None
    elevator_id: Optional[str] = None
    floor: int
    hour: int = datetime.now().hour

    def save(self):
        from src.gateway.database.demand_log_database import DemandLogDatabase

        DemandLogDatabase.create(self)


class SmartElevator(Elevator):
    id: Optional[str] = None
    name: str = "Elevator"
    prediction_model: list[int] = [0 for _ in range(24)]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.id is None:
            from src.gateway.database.elevator_database import ElevatorDatabase

            self.id = ElevatorDatabase.create(self)

    def press_floor_button(self, floor: int):
        if floor not in self.demand_floors:
            self.demand_floors.append(floor)
            DemandLog(elevator_id=self.id, floor=floor).save()

    def train(self):
        from src.gateway.database.demand_log_database import DemandLogDatabase

        demand_historic = DemandLogDatabase.get_by_elevator_id(self.id)

        max_floor_number = max(demand_historic, key=lambda log: log.floor).floor
        tmp = []
        for _ in range(24):
            tmp.append([0 for _ in range(max_floor_number + 1)])

        for log in demand_historic:
            tmp[log.hour][log.floor] += 1

        self.prediction_model = []
        for hour in range(24):
            max_frequency_value = max(tmp[hour])
            if max_frequency_value == 0:
                self.prediction_model.append(0)
                continue
            max_frequency_floor = tmp[hour].index(max_frequency_value)
            self.prediction_model.append(max_frequency_floor)
        # save in database here

    def save(self):
        from src.gateway.database.elevator_database import ElevatorDatabase

        ElevatorDatabase.update(self)

    def load_prediction_model(self):
        from src.gateway.database.elevator_database import ElevatorDatabase

        tmp = ElevatorDatabase.get_by_id(self.id)
        if tmp is not None:
            self.prediction_model = tmp.prediction_model

    def get_best_floor_by_hour(self, hour=datetime.now().hour) -> int:
        if hour < 0 or hour > 23:
            raise ValueError("Invalid hour")
        return self.prediction_model[hour]

    def run(self, seconds_per_floor=1, print_debug=True):
        while not self.demand_is_empty:
            if print_debug:
                self._print_state()

            time.sleep(seconds_per_floor)
            self._evalutate_state()

        self.going_to = self.prediction_model[datetime.now().hour]
        while not self._evalutate_motion():
            time.sleep(seconds_per_floor)

        if print_debug:
            self._print_state()

    def _minimize_cost(self, weights, max_floor_number):
        minimal_cost = float("inf")
        best_floor = 0
        for actual_floor in range(max_floor_number + 1):
            cost = 0
            for destiny_floor in range(max_floor_number + 1):
                cost += weights[destiny_floor] * abs(destiny_floor - actual_floor)
            if cost < minimal_cost:
                minimal_cost = cost
                best_floor = actual_floor
        return best_floor
