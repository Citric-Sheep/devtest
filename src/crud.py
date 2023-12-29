from models import ElevatorCall, get_db
from datetime import datetime

db = next(get_db())


def add_call(current_floor: int, target_floor: int, user_floor: int,
             date: str):
    """Creates a new elevator call in the database.

    Args:
        call (ElevatorCall): Elevator call data
        
    """
    timestamp = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    call = ElevatorCall(target_floor=target_floor,
                        current_floor=current_floor,
                        user_floor=user_floor,
                        timestamp=timestamp)
    db.add(call)
    db.commit()
    return call


def delete_call(id: int):
    """Deletes the call with the inputed id.
    
    Args :
        id (int): The id of the elevator call to delete
    """
    if db.query(ElevatorCall).count() == 0:
        print(f"No call found with id: {id}")
    else:
        db.query(ElevatorCall).filter(ElevatorCall.id == id).delete()
        db.commit()
        print(f"Deleted call with id: {id}")


def delete_all_calls():
    """Deletes all elevator calls from the database.
    
    """
    if db.query(ElevatorCall).count() == 0:
        print("No calls found")
    else:
        db.query(ElevatorCall).delete()
        db.commit()
        print("Deleted all calls")


def get_calls():
    """Retrieves all elevator calls from the database.
    
    Returns:
        [list | None]: A list of all elevator calls 
    
    """
    return db.query(ElevatorCall).all()


def get_last_call():
    if db.query(ElevatorCall).count() == 0:
        print("No calls found")
        return None
    call = db.query(ElevatorCall).order_by(ElevatorCall.id.desc()).first()
    return call


def update_call(id: int, target_floor: int, current_floor: int,
                user_floor: int, date: str):
    """Updates an elevator call in the database.

    Args:
        id (int): The id of the elevator call to update
        target_floor (int): The requested floor to go to
        current_floor (int): The current floor of the elevator
        user_floor (int): The floor from which the elevator was called
        date (str): The timestamp of the elevator call

    """
    if db.query(ElevatorCall).count() == 0:
        try:
            call = db.query(ElevatorCall).filter(ElevatorCall.id == id).first()
            call.target_floor = target_floor
            call.current_floor = current_floor
            call.user_floor = user_floor
            call.timestamp = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
            db.commit()
            print(f"Updated call with id: {id}")
        except Exception as e:
            db.rollback()
            print(f"Error updating call with id: {id}")


if __name__ == "__main__":
    # Example usage
    # Create a new call
    add_call(12, 3, 1, "2021-12-01 12:00:00")

    # Read calls
    print(*get_calls(), sep="\n")
    last_id = get_last_call().id

    # Update_call
    update_call(last_id, 12, 10, 3, "2021-12-01 12:20:00")

    # Delete a call
    delete_call(last_id)
