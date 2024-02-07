class Elevator:
    def __init__(self, elevator_id:int, current_floor:int, resting_floor:int, elevator_status:str):
        """
        Initialize an Elevator object.

        Parameters:
        - elevator_id (int): The unique identifier for the elevator.
        - current_floor (int): The current floor where the elevator is located.
        - resting_floor (int): The resting floor for the elevator when it's not in use.
        - elevator_status (str): The status of the elevator (e.g., "Idle", "Moving").
        """
        self.elevator_id = elevator_id
        self.current_floor = current_floor
        self.resting_floor = resting_floor
        self.elevator_status = elevator_status

    def to_dict(self):
        """
        Convert the Elevator object to a dictionary.

        Returns:
        - dict: A dictionary representation of the Elevator object.
        """
        return {
            'elevator_id': self.elevator_id,
            'current_floor': self.current_floor,
            'resting_floor': self.resting_floor,
            'elevator_status': self.elevator_status
        }

    @classmethod
    def from_dict(cls, data:dict):
        """
        Convert the Elevator object to a dictionary.

        Returns:
        - dict: A dictionary representation of the Elevator object.
        """
        return cls(
            elevator_id=data['elevator_id'],
            current_floor=data['current_floor'],
            resting_floor=data['resting_floor'],
            elevator_status=data['elevator_status']
        )
