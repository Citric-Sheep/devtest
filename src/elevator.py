from src.floor import Floor
import datetime
from models.elevator_history_entry import ElevatorHistoryEntry
from src.person import Person

class Elevator:
    def __init__(self, floor: Floor = Floor(), max_number_of_passengers: int = 10, max_weight: int = 1000) -> None:
        self.current_floor = floor
        self.prev_floor = Floor()
        self.max_number_of_passengers = max_number_of_passengers
        self.max_weight = max_weight

    def security_check(self, passengers: list[Person]) -> bool:
        if len(passengers) > self.max_number_of_passengers:
            return False
        
        if sum([p.get_weight() for p in passengers]) > self.max_weight:
            return False
        
        return True

    def __call__(self, floor_number: int, passengers: list[Person]) -> ElevatorHistoryEntry:
        if self.security_check(passengers):
            self.prev_floor.floor_number = self.current_floor.floor_number
            self.current_floor.set_floor_number(floor_number)
            return ElevatorHistoryEntry(prev_floor = self.prev_floor,
                                        current_floor = self.current_floor,
                                        timestamp = datetime.datetime.now(),
                                        n_passegenrs=len(passengers),
                                        weight=sum([p.get_weight() for p in passengers]))  
        else:
            # logger.Warning("Security check failed, please reduce number of passengers and/or weight")
            pass