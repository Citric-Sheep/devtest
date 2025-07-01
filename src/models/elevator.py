from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.database import Base

class Elevator(Base):
    """
    Model representing an elevator.
    
    This captures information about each elevator in the system.
    
    Attributes:
        id: Unique identifier for the elevator
        building_id: Identifier for the building the elevator is in
        max_floor: The highest floor the elevator can reach
        min_floor: The lowest floor the elevator can reach
    """
    __tablename__ = "elevators"

    id = Column(Integer, primary_key=True, index=True)
    building_id = Column(Integer, nullable=False, index=True)
    max_floor = Column(Integer, nullable=False)
    min_floor = Column(Integer, nullable=False)
    
    # Relationship to the ElevatorDemand model
    demands = relationship("ElevatorDemand", back_populates="elevator")
