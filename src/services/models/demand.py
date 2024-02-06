# ```When people call an elevator this is considered a demand```

from datetime import datetime
class Demand:
    def __init__(self, demand_id:int, floor:int, timestamp:datetime):
        self.demand_id = demand_id
        self.floor = floor
        self.timestamp = timestamp

    def to_dict(self):
        return {
            'demand_id': self.demand_id,
            'floor': self.floor,
            'timestamp': self.timestamp
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            demand_id=data['demand_id'],
            floor=data['floor'],
            timestamp=data['timestamp']
        )