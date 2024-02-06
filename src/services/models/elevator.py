class Elevator:
    def __init__(self, elevator_id:int, current_floor:int, resting_floor:int, elevator_status:str):
        self.elevator_id = elevator_id
        self.current_floor = current_floor
        self.resting_floor = resting_floor
        self.elevator_status = elevator_status

    def to_dict(self):
        return {
            'elevator_id': self.elevator_id,
            'current_floor': self.current_floor,
            'resting_floor': self.resting_floor,
            'elevator_status': self.elevator_status
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            elevator_id=data['elevator_id'],
            current_floor=data['current_floor'],
            resting_floor=data['resting_floor'],
            elevator_status=data['elevator_status']
        )
