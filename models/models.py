"""
In this file you'll find all model's definition
"""

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Building(Base):
    """
    Modeling Building with SQLAlchemy
    """
    __tablename__ = 'buildings'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    address = Column(String)
    city = Column(String)
    country = Column(String)

    elevators = relationship("Elevator", back_populates="building")

    def __init__(self, name, address, city, country, custom_id: int = None):
        self.name = name
        self.address = address
        self.city = city
        self.country = country
        if custom_id:
            self.id = custom_id


class Elevator(Base):
    """
    Modeling Elevator with SQLAlchemy
    """
    __tablename__ = 'elevators'

    id = Column(Integer, primary_key=True)
    building_id = Column(Integer, ForeignKey('buildings.id'))
    max_floors = Column(Integer)  # Max amount of floors that this elevator can move between
    local_identifier = Column(Integer)  # When there's more than one elevator per building

    building = relationship("Building", back_populates="elevators")
    demands = relationship("Demand", back_populates="elevator")

    def __init__(self, building_id, max_floors, local_identifier, custom_id: int = None):
        self.building_id = building_id
        self.max_floors = max_floors
        self.local_identifier = local_identifier
        if custom_id:
            self.id = custom_id


class Demand(Base):

    """
    Modeling Demand with SQLAlchemy
    """
    __tablename__ = 'demands'

    id = Column(Integer, primary_key=True)
    elevator_id = Column(Integer, ForeignKey('elevators.id'))
    start_floor = Column(Integer)
    end_floor = Column(Integer)
    timestamp = Column(DateTime, default=datetime.now())

    elevator = relationship("Elevator", back_populates="demands")

    def __init__(self, elevator_id, start_floor, end_floor, custom_id: int = None):
        self.elevator_id = elevator_id
        self.start_floor = start_floor
        self.end_floor = end_floor
        if custom_id:
            self.id = custom_id
