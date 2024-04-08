"""Models module"""

import uuid

from sqlalchemy import Column, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ElevatorDemand(Base):
    """Elevator Demand Table"""

    __tablename__ = "elevator_demand"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    origin = Column(Integer, nullable=False)
    destination = Column(Integer, nullable=False)
