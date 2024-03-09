from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ElevatorMovement(Base):
    __tablename__ = 'elevator_movements'

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime)
    elevator_id = Column(Integer)
    current_floor = Column(Integer)
    next_floor = Column(Integer, nullable=True)
    action = Column(String)
    floor_requested = Column(Integer)   
    expected_arrival_time = Column(DateTime, nullable=True)  # Nuevo campo

class Demand(Base):
    __tablename__ = 'demands'

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime)
    floor_requested = Column(Integer)
