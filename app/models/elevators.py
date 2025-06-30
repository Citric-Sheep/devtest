from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, Boolean
from app.database.elevators import Base

class Demand(Base):
    __tablename__ = "demands"

    id = Column(Integer, primary_key=True, index=True)
    floor = Column(Integer, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)  # ← OK aqui


class ElevatorState(Base):
    __tablename__ = "elevator_states"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    floor = Column(Integer, nullable=False)
    vacant = Column(Boolean, nullable=False)