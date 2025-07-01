from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from src.database import Base

class ElevatorDemand(Base):
    """
    Model representing elevator demand data.
    
    This captures when and where people call elevators, which is the essential
    data needed to train a prediction model for optimal resting floors.
    
    Attributes:
        id: Unique identifier for the demand
        timestamp: When the demand occurred
        floor: Which floor the demand came from
        direction: Whether the person wanted to go up or down
        elevator_id: Which elevator responded to this demand
    """
    __tablename__ = "elevator_demands"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    floor = Column(Integer, nullable=False, index=True)
    direction = Column(String, nullable=False)  # "up" or "down"
    elevator_id = Column(Integer, ForeignKey("elevators.id"), nullable=False, index=True)
    
    # Relationship to the Elevator model
    elevator = relationship("Elevator", back_populates="demands")
