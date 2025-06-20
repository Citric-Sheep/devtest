from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Elevator(Base):
    __tablename__ = "elevators"
    id = Column(Integer, primary_key=True, index=True)
    current_floor = Column(Integer, nullable=False)
    is_moving = Column(Boolean, default=False)
    is_occupied = Column(Boolean, default=False)
    last_updated = Column(DateTime, default=datetime.utcnow)

class ElevatorEvent(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    elevator_id = Column(Integer, ForeignKey("elevators.id"))
    event_type = Column(String, nullable=False)  # CALL, MOVE, REST
    from_floor = Column(Integer, nullable=True)
    to_floor = Column(Integer, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

class Demand(Base):
    __tablename__ = "demands"
    id = Column(Integer, primary_key=True, index=True)
    floor_called_from = Column(Integer, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
