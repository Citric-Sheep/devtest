from src.database import DatabaseEntry

class ElevatorHistoryEntry(DatabaseEntry):
    def __init__(self, timestamp, prev_floor, current_floor, n_passegenrs, weight):
        self.timestamp = timestamp
        self.prev_floor = prev_floor
        self.current_floor = current_floor
        self.n_passegenrs = n_passegenrs
        self.weight = weight

    def serialize(self) -> dict:
        return {
            "timestamp": str(self.timestamp),
            "prev_floor": self.prev_floor.floor_number,
            "current_floor": self.current_floor.floor_number,
            "n_passengers": self.n_passegenrs,
            "weight": self.weight
        }
    
    def __str__(self):
        return f"Elevator {self.elevator_id} travelled from floor {self.prev_floor} to {self.current_floor} at {self.timestamp} with {self.n_passengers} passengers weighing {self.weight} kg."
