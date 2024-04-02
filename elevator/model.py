"""
SQLAlchemy Elevator Models.
"""

from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class ElevatorDb(Base):
    __tablename__ = "elevator"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    demands = relationship("ElevatorDemandDb", backref="elevator", cascade="all, delete")


class ElevatorDemandDb(Base):
    __tablename__ = "elevator_demand"

    id = Column(Integer, primary_key=True, autoincrement=True)
    elevator_id = Column(Integer, ForeignKey("elevator.id", ondelete="CASCADE"))
    requested_at = Column(DateTime, default=datetime.utcnow)
    pressed_at_floor = Column(Integer)
