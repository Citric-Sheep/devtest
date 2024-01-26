from src.floor import Floor
import datetime
from models.elevator_history_entry import ElevatorHistoryEntry
from src.person import Person

class Elevator:
    def __init__(self, floor: Floor = Floor(), max_number_of_passengers: int = 10, max_weight: int = 1000) -> None:
        """
        Initializes an Elevator object.

        Args:
            floor (Floor, optional): The current floor of the elevator. Defaults to Floor().
            max_number_of_passengers (int, optional): The maximum number of passengers the elevator can hold. Defaults to 10.
            max_weight (int, optional): The maximum weight capacity of the elevator. Defaults to 1000.
        """
        self.current_floor = floor
        self.prev_floor = Floor()
        self.max_number_of_passengers = max_number_of_passengers
        self.max_weight = max_weight

    def security_check(self, passengers: list[Person]) -> bool:
        """
        Performs a security check to ensure the elevator can safely transport the given passengers.

        Args:
            passengers (list[Person]): The list of passengers to transport.

        Returns:
            bool: True if the security check passes, False otherwise.
        """
        if len(passengers) > self.max_number_of_passengers:
            return False
        
        if sum([p.get_weight() for p in passengers]) > self.max_weight:
            return False
        
        return True

    def __call__(self, floor_number: int, passengers: list[Person]) -> ElevatorHistoryEntry:
        """
        Executes the elevator operation for the given floor number and passengers.

        Args:
            floor_number (int): The floor number to move the elevator to.
            passengers (list[Person]): The list of passengers to transport.

        Returns:
            ElevatorHistoryEntry: The history entry for the elevator operation.
        """
        if self.security_check(passengers):
            self.prev_floor.floor_number = self.current_floor.floor_number
            self.current_floor.set_floor_number(floor_number)
            return ElevatorHistoryEntry(prev_floor=self.prev_floor,
                                        current_floor=self.current_floor,
                                        timestamp=datetime.datetime.now(),
                                        n_passegenrs=len(passengers),
                                        weight=sum([p.get_weight() for p in passengers]))  
        else:
            # logger.Warning("Security check failed, please reduce number of passengers and/or weight")
            pass
