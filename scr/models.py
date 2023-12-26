# models.py
from sqlalchemy import Column, Integer, DateTime
from scr.db import Base


class ElevatorState(Base):
    __tablename__ = "elevator_state"

    id = Column(Integer, primary_key=True, index=True)
    current_floor = Column(Integer)
    demand_floor = Column(Integer)
    next_floor = Column(Integer)
    call_datetime = Column(DateTime(timezone=True))

    def __repr__(self):
        return f"<ElevatorState(id={self.id}, current_floor={self.current_floor}, demand_floor={self.demand_floor}, next_floor={self.next_floor}, call_datetime={self.call_datetime})>"
