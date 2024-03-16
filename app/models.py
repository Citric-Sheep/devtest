from database import db

class Demand(db.Model):
    __tablename__ = 'demands'
    id = db.Column(db.Integer, primary_key=True, index=True)
    # The floor_requested field represents the floor number where the demand originates from.
    floor = db.Column(db.Integer, nullable=False)
    # The timestamp indicates when the demand was created. It's set to the current time by default.
    timestamp = db.Column(db.DateTime, nullable=False, default=db.func.now())

    def serialize(self):
        """Serialize Demand object to a dictionary."""
        return {
            'id': self.id,
            'floor': self.floor,
            'timestamp': self.timestamp.isoformat()
        }

class ElevatorMovement(db.Model):
    __tablename__ = 'elevator_movements'
    id = db.Column(db.Integer, primary_key=True, index=True)
    # The action field describes the type of movement (e.g., going up, going down, stopped).
    action = db.Column(db.String, nullable=False)
    # The current_floor field indicates the current floor where the elevator is located.
    current_floor = db.Column(db.Integer, nullable=False)
    # The elevator_id field links the movement to a specific elevator.
    elevator_id = db.Column(db.Integer, nullable=False)
    # The expected_arrival_time field indicates the estimated time when the elevator is expected to arrive at the next floor. It's nullable because it might not be applicable in all situations.
    expected_arrival_time = db.Column(db.DateTime, nullable=True)
    # The floor_requested field stores the floor requested by a user. It's nullable because the movement might not be a response to a request.
    floor_requested = db.Column(db.Integer, nullable=True)
    # The next_floor field represents the floor where the elevator is heading next. It's nullable because the elevator might not have a next floor (e.g., idle state).
    next_floor = db.Column(db.Integer, nullable=True)
    # The timestamp indicates when the movement occurred. It's set to the current time by default.
    timestamp = db.Column(db.DateTime, nullable=False, default=db.func.now())

    def serialize(self):
        """Serialize ElevatorMovement object to a dictionary."""
        return {
            'id': self.id,
            'action': self.action,
            'current_floor': self.current_floor,
            'elevator_id': self.elevator_id,
            'expected_arrival_time': self.expected_arrival_time.isoformat() if self.expected_arrival_time else None,
            'floor_requested': self.floor_requested,
            'next_floor': self.next_floor,
            'timestamp': self.timestamp.isoformat()
        }
