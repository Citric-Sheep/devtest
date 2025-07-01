"""
Script to initialize the database with sample data.
This is useful for development and testing purposes.
"""

import os
import sys
from datetime import datetime, timedelta
import random

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from src.database import engine, Base, SessionLocal
from src.models.elevator import Elevator
from src.models.elevator_demand import ElevatorDemand

def init_db():
    """Initialize the database with tables and sample data."""
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Create a session
    db = SessionLocal()
    
    try:
        # Check if we already have data
        if db.query(Elevator).count() > 0:
            print("Database already contains data. Skipping initialization.")
            return
        
        # Create sample elevators
        print("Creating sample elevators...")
        elevators = [
            Elevator(building_id=1, max_floor=10, min_floor=0),
            Elevator(building_id=2, max_floor=10, min_floor=-2),
            Elevator(building_id=3, max_floor=20, min_floor=0),
        ]
        
        for elevator in elevators:
            db.add(elevator)
        
        db.commit()
        
        # Create sample demands
        print("Creating sample demands...")
        
        # Get the elevator IDs
        elevator_ids = [elevator.id for elevator in db.query(Elevator).all()]
        
        # Create demands for the past week
        now = datetime.now()
        
        # Create 100 random demands
        demands = []
        for _ in range(100):
            # Random time in the past week
            hours_ago = random.randint(0, 24 * 7)  # Up to a week ago
            timestamp = now - timedelta(hours=hours_ago)
            
            # Random floor
            floor = random.randint(0, 20)
            
            # Random direction
            direction = random.choice(["up", "down"])
            
            # Random elevator (or None)
            elevator_id = random.choice(elevator_ids)
            
            demand = ElevatorDemand(
                floor=floor,
                direction=direction,
                timestamp=timestamp,
                elevator_id=elevator_id
            )
            demands.append(demand)
        
        db.bulk_save_objects(demands)
        db.commit()
        
        print(f"Database initialized with {len(elevators)} elevators and {len(demands)} demands.")
    
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
