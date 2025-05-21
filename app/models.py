from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Elevator(Base):
    __tablename__ = "elevators"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    demands = relationship("DemandEvent", back_populates="elevator")
    restings = relationship("RestingPeriod", back_populates="elevator")
    
class DemandEvent(Base):
    __tablename__ = "demands"
    id = Column(Integer, primary_key=True, index=True)
    elevator_id = Column(Integer, ForeignKey("elevators.id"))
    floor = Column(Integer)
    timestamp = Column(DateTime)
    direction = Column(String)
    surge_tag = Column(Boolean, default=False)
    elevator = relationship("Elevator", back_populates="demands")
    
class RestingPeriod(Base):
    __tablename__ = "restings"
    id = Column(Integer, primary_key=True, index=True)
    elevator_id = Column(Integer, ForeignKey("elevators.id"))
    floor = Column(Integer)
    start_time = Column(DateTime)
    end_time = Column(DateTime, nullable=True)
    duration_sec = Column(Integer, nullable=True)
    peak_hours_flag = Column(Boolean, default=False)
    relocation_flag = Column(Boolean, default=False)
    non_optimal_rested = Column(Boolean, default=False)
    elevator = relationship("Elevator", back_populates="restings")
     