from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func

DATABASE_URL = "postgresql://postgres:david.123@localhost:5432/citric_elevator"
engine = create_engine(DATABASE_URL)

Base = declarative_base()

class ElevatorState(Base):
    __tablename__ = "elevator_state"
    
    id = Column(Integer, primary_key=True, index=True)
    current_floor = Column(Integer)  # Add the current_floor column
    demand_floor = Column(Integer)  # Add the demand_floor column
    next_floor = Column(Integer)  # Add the demand_floor column
    call_datetime = Column(DateTime(timezone=True)) 
    def __repr__(self):
        return f"<ElevatorState(id={self.id}, current_floor={self.current_floor}, demand_floor={self.demand_floor}, next_floor={self.next_floor}, call_datetime={self.call_datetime})>"
# Create the tables in the database
Base.metadata.create_all(bind=engine)