from datetime import datetime
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import logging

# Base model class
Base = declarative_base()

# This handles buildings - pretty straightforward
class Building(Base):
    __tablename__ = 'buildings'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)  # Building name
    floors = Column(Integer, nullable=False)  # How many floors
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Link to elevators
    elevators = relationship("Elevator", back_populates="building")
    
    def __repr__(self):
        return f"Building #{self.id}: {self.name} ({self.floors} floors)"


# Elevator model - the main thing we're tracking
class Elevator(Base):
    __tablename__ = 'elevators'
    
    # Basic info
    id = Column(Integer, primary_key=True)
    building_id = Column(Integer, ForeignKey('buildings.id'), nullable=False)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships - lots of them!
    building = relationship("Building", back_populates="elevators")
    calls = relationship("ElevatorCall", back_populates="elevator")
    trips = relationship("ElevatorTrip", back_populates="elevator")
    states = relationship("ElevatorState", back_populates="elevator")
    time_stats = relationship("TimeStatistic", back_populates="elevator")
    floor_stats = relationship("FloorStatistic", back_populates="elevator")
    
    def __str__(self):
        return f"Elevator {self.name} in {self.building_id}"
    
    def __repr__(self):
        return f"<Elevator {self.id}: {self.name}>"
    
    # Get the latest state
    def get_state(self, s):
        return s.query(ElevatorState).filter(
            ElevatorState.elevator_id == self.id
        ).order_by(ElevatorState.timestamp.desc()).first()
    
    # Is it sitting idle?
    def is_resting(self, s):
        state = self.get_state(s)
        return state and state.is_vacant and not state.is_moving
    
    # Where is it resting?
    def rest_floor(self, s):
        state = self.get_state(s)
        if state and state.is_vacant and not state.is_moving:
            return state.floor
        return None


# When someone calls the elevator
class ElevatorCall(Base):
    __tablename__ = 'elevator_calls'
    
    # Basic info
    id = Column(Integer, primary_key=True)
    elevator_id = Column(Integer, ForeignKey('elevators.id'), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    floor = Column(Integer, nullable=False)  # Which floor called
    direction = Column(String, CheckConstraint("direction IN ('up', 'down')"), nullable=False)
    wait_time = Column(Integer)  # How long they waited (seconds)
    
    # Link back to elevator
    elevator = relationship("Elevator", back_populates="calls")
    
    def __repr__(self):
        return f"Call #{self.id} - Floor {self.floor} going {self.direction}"


# A trip the elevator makes
class ElevatorTrip(Base):
    __tablename__ = 'elevator_trips'
    
    # Trip details
    id = Column(Integer, primary_key=True)
    elevator_id = Column(Integer, ForeignKey('elevators.id'), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime)  # Null until trip completes
    origin_floor = Column(Integer, nullable=False)
    destination_floor = Column(Integer, nullable=False)
    occupancy = Column(Boolean, nullable=False)  # Had passengers?
    
    # Link to elevator
    elevator = relationship("Elevator", back_populates="trips")
    
    def __repr__(self):
        status = "Completed" if self.end_time else "In progress"
        return f"Trip: {self.origin_floor}→{self.destination_floor} ({status})"
    
    # How long the trip took
    def trip_time(self):
        if not self.end_time:
            return None
        return (self.end_time - self.start_time).total_seconds()


# Current state of an elevator
class ElevatorState(Base):
    __tablename__ = 'elevator_states'
    
    # State info
    id = Column(Integer, primary_key=True)
    elevator_id = Column(Integer, ForeignKey('elevators.id'), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    floor = Column(Integer, nullable=False)  # Current floor
    is_vacant = Column(Boolean, nullable=False)  # Empty?
    is_moving = Column(Boolean, nullable=False)  # Moving?
    
    # Link to elevator
    elevator = relationship("Elevator", back_populates="states")
    
    # Helper to check if it's just sitting there
    @property
    def is_resting(self):
        return self.is_vacant and not self.is_moving
    
    def __repr__(self):
        if self.is_vacant and not self.is_moving:
            status = "resting"
        elif not self.is_vacant:
            status = "occupied"
        else:
            status = "moving"
        return f"State: Floor {self.floor}, {status}"


# Stats by time of day - for ML predictions
class TimeStatistic(Base):
    __tablename__ = 'time_statistics'
    
    # Basic info
    id = Column(Integer, primary_key=True)
    elevator_id = Column(Integer, ForeignKey('elevators.id'), nullable=False)
    date = Column(Date, nullable=False)
    hour = Column(Integer, CheckConstraint("hour BETWEEN 0 AND 23"), nullable=False)
    
    # Stats
    calls_count = Column(Integer, default=0)
    most_common_origin_floor = Column(Integer)  # Where people call from most
    most_common_destination_floor = Column(Integer)  # Where they go most
    
    # Link to elevator
    elevator = relationship("Elevator", back_populates="time_stats")
    
    def __str__(self):
        return f"Stats for {self.date} at {self.hour}:00 - {self.calls_count} calls"


# Stats by floor - for ML predictions
class FloorStatistic(Base):
    __tablename__ = 'floor_statistics'
    
    # Basic info
    id = Column(Integer, primary_key=True)
    elevator_id = Column(Integer, ForeignKey('elevators.id'), nullable=False)
    floor = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)
    
    # Stats
    calls_count = Column(Integer, default=0)  # How many calls from this floor
    avg_wait_time = Column(Float)  # Average wait time in seconds
    
    # Link to elevator
    elevator = relationship("Elevator", back_populates="floor_stats")
    
    def __str__(self):
        wait = f"{self.avg_wait_time:.1f}s" if self.avg_wait_time else "unknown"
        return f"Floor {self.floor} on {self.date}: {self.calls_count} calls, avg wait {wait}"