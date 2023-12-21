from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from datetime import datetime
from create_table import RestingFloors
# Assume you already have the functions for creating and getting elevator states from the previous example
from crud_elevator import *
def create_session():
    DATABASE_URL = "postgresql://postgres:david.123@localhost:5432/citric_elevator"
    engine = create_engine(DATABASE_URL)
    return Session(engine)

def create_resting_floor(session, elevator_id, resting_floor):
    # Check if elevator_id exists in elevator_state table
    elevator_state = get_elevator_state_by_id(session, elevator_id)
    if elevator_state:
        resting_floor_instance = RestingFloors(
            elevator_id=elevator_id,
            resting_floor=resting_floor
        )
        session.add(resting_floor_instance)
        session.commit()
        return resting_floor_instance
    else:
        print(f"Elevator with id {elevator_id} does not exist.")
        return None

# Read
def get_all_resting_floors(session):
    return session.query(RestingFloors).all()

def get_resting_floor_by_id(session, resting_floor_id):
    return session.query(RestingFloors).filter_by(id=resting_floor_id).first()

# Update
def update_resting_floor(session, resting_floor_id, new_floor):
    resting_floor = session.query(RestingFloors).filter_by(id=resting_floor_id).first()
    if resting_floor:
        resting_floor.resting_floor = new_floor
        session.commit()
        return resting_floor
    return None

# Delete
def delete_resting_floor(session, resting_floor_id):
    resting_floor = session.query(RestingFloors).filter_by(id=resting_floor_id).first()
    if resting_floor:
        session.delete(resting_floor)
        session.commit()
        return resting_floor
    return None

# Example Usage
if __name__ == "__main__":
    session = create_session()

    # Create
    resting_floor = create_resting_floor(session, elevator_id=1, resting_floor=3)

    # Read
    all_floors = get_all_resting_floors(session)
    print("All Resting Floors:")
    for floor in all_floors:
        print(floor.id, floor.elevator_id, floor.resting_floor)

    specific_floor = get_resting_floor_by_id(session, resting_floor_id=1)
    print("\nResting Floor by ID:")
    print(specific_floor.id, specific_floor.elevator_id, specific_floor.resting_floor)

    # Update
    updated_floor = update_resting_floor(session, resting_floor_id=1, new_floor=5)
    print("\nUpdated Resting Floor:")
    print(updated_floor.id, updated_floor.elevator_id, updated_floor.resting_floor)

    # Delete
    deleted_floor = delete_resting_floor(session, resting_floor_id=1)
    print("\nDeleted Resting Floor:")
    print(deleted_floor.id, deleted_floor.elevator_id, deleted_floor.resting_floor)

    # Close the session
    session.close()
