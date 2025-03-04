from app.database import db

class Elevator(db.Model):
    elevator_id = db.Column(db.Integer, primary_key=True)
    current_floor = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(10), nullable=False)
    resting_floor = db.Column(db.Integer)

    demands = db.relationship('Demand', backref='elevator', lazy=True)


class Demand(db.Model):
    demand_id = db.Column(db.Integer, primary_key=True)
    floor_number = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    elevator_id = db.Column(db.Integer, db.ForeignKey('elevator.elevator_id'))


class ElevatorHistory(db.Model):
    history_id = db.Column(db.Integer, primary_key=True)
    elevator_id = db.Column(db.Integer, db.ForeignKey('elevator.elevator_id'), nullable=False)
    resting_floor = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)