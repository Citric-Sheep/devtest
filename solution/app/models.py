# -*- coding: utf-8 -*-
from app import db
from datetime import datetime

class ElevatorDemand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    target_floor = db.Column(db.Integer, nullable=False)
    actual_floor = db.Column(db.Integer, nullable=False)


class ElevatorState(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    floor = db.Column(db.Integer)
    vacant = db.Column(db.Boolean)
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime,nullable=True)
    duration_sec = db.Column(db.Integer,nullable=True)
    relocation_flag = db.Column(db.Boolean,nullable=True)
    

