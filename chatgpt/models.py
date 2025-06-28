from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class ElevatorDemand(db.Model):
    __tablename__ = 'elevator_demands'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.now)
    floor = db.Column(db.Integer, nullable=False)

    elevator_id = db.Column(db.Integer, db.ForeignKey('elevators.id'), nullable=False)
    elevator = db.relationship('Elevator', back_populates='demands')
    

class ElevatorState(db.Model):
    __tablename__ = 'elevator_states'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.now)
    floor = db.Column(db.Integer, nullable=False)
    vacant = db.Column(db.Boolean, nullable=False)

    elevator_id = db.Column(db.Integer, db.ForeignKey('elevators.id'), nullable=False)
    elevator = db.relationship('Elevator', back_populates='states')

class Elevator(db.Model):
    __tablename__ = 'elevators'
    id       = db.Column(db.Integer, primary_key=True)
    name     = db.Column(db.String(50), nullable=False)

    demands = db.relationship('ElevatorDemand', back_populates='elevator', cascade="all, delete-orphan")
    states  = db.relationship('ElevatorState', back_populates='elevator', cascade="all, delete-orphan")


