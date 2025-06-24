from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime, timezone

Base = declarative_base()

class Demand(Base):
    __tablename__ = "demand"
    id = Column(Integer, primary_key=True, index=True)
    elevator_id = Column(Integer, index=True) #por ahora solo un ascensor
    floor = Column(Integer, nullable=False)  # Piso desde donde se llama
    destination_floor = Column(Integer, nullable=False)  # Piso al que quiere ir el usuario
    timestamp_called = Column(DateTime, default=datetime.now(timezone.utc), index=True)

class RestingPeriod(Base):
    __tablename__ = "resting_period"
    id = Column(Integer, primary_key=True, index=True)
    elevator_id = Column(Integer, index=True)
    floor = Column(Integer, nullable=False) 
    resting_start = Column(DateTime, default=datetime.now(timezone.utc), index=True)
    resting_end = Column(DateTime, nullable=True, index=True)
