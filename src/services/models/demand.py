from datetime import datetime
class Demand:
    def __init__(self, demand_id:int, floor:int, timestamp:datetime):
        """
        Initialize a Demand object.

        Parameters:
        - demand_id (int): The unique identifier for the demand.
        - floor (int): The floor where the demand is made.
        - timestamp (datetime): The timestamp of the demand.
        """
        self.demand_id = demand_id
        self.floor = floor
        self.timestamp = timestamp
        self.demand_id = demand_id
        self.floor = floor
        self.timestamp = timestamp

    def to_dict(self):
        """
        Convert the Demand object to a dictionary.

        Returns:
        - dict: A dictionary representation of the Demand object.
        """
        return {
            'demand_id': self.demand_id,
            'floor': self.floor,
            'timestamp': self.timestamp
        }

    @classmethod
    def from_dict(cls, data:dict):
        """
        Create a Demand object from a dictionary.

        Parameters:
        - data (dict): The dictionary containing demand data.

        Returns:
        - Demand: The Demand object created from the dictionary.
        """
        return cls(
            demand_id=data['demand_id'],
            floor=data['floor'],
            timestamp=data['timestamp']
        )