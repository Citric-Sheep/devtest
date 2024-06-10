from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Elevator(db.Model):  # Elevador -> Elevator
    elevator_id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String, nullable=False)  # modelo -> model
    capacity = db.Column(db.Integer, nullable=False)  # capacidade -> capacity

class Floor(db.Model):  # Andar -> Floor
    floor_id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False)  # numero -> number

class ElevatorDemand(db.Model):  # DemandaElevador -> ElevatorDemand
    demand_id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    floor_id = db.Column(db.Integer, db.ForeignKey('floor.floor_id'), nullable=False)  # andar_id -> floor_id
    elevator_id = db.Column(db.Integer, db.ForeignKey('elevator.elevator_id'), nullable=False)
    direction = db.Column(db.String, nullable=False)  # direcao -> direction
    request_type = db.Column(db.String, nullable=False)  # tipo -> type

class ElevatorRestFloor(db.Model):  # AndarRepousoElevador -> ElevatorRestFloor
    rest_id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    elevator_id = db.Column(db.Integer, db.ForeignKey('elevator.elevator_id'), nullable=False)
    floor_id = db.Column(db.Integer, db.ForeignKey('floor.floor_id'), nullable=False)  # andar_id -> floor_id
    reason = db.Column(db.String, nullable=False)  # motivo -> reason
