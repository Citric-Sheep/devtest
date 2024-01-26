from src.database import DatabaseEntry

class ElevatorHistoryEntry(DatabaseEntry):
    def __init__(self, timestamp, prev_floor, current_floor, n_passengers, weight):
        """
        Initialize an ElevatorHistoryEntry object.

        Args:
            timestamp (datetime): The timestamp of the elevator entry.
            prev_floor (Floor): The previous floor of the elevator.
            current_floor (Floor): The current floor of the elevator.
            n_passengers (int): The number of passengers in the elevator.
            weight (float): The weight of the passengers in the elevator.

        Returns:
            None
        """
        self.timestamp = timestamp
        self.prev_floor = prev_floor
        self.current_floor = current_floor
        self.n_passengers = n_passengers
        self.weight = weight

    def serialize(self) -> dict:
        """
        Serialize the ElevatorHistoryEntry object into a dictionary.

        Returns:
            dict: A dictionary representation of the ElevatorHistoryEntry object.
        """
        return {
            "timestamp": str(self.timestamp),
            "prev_floor": self.prev_floor.floor_number,
            "current_floor": self.current_floor.floor_number,
            "n_passengers": self.n_passengers,
            "weight": self.weight
        }
    
    def __str__(self):
        """
        Return a string representation of the ElevatorHistoryEntry object.

        Returns:
            str: A string representation of the ElevatorHistoryEntry object.
        """
        return f"Elevator travelled from floor {self.prev_floor} to {self.current_floor} at {self.timestamp} with {self.n_passengers} passengers weighing {self.weight} kg."
