from sqlalchemy.orm import Session
from app import models
from datetime import datetime

def create_elevator(db: Session, current_floor: int):
    elevator = models.Elevator(current_floor=current_floor)
    db.add(elevator)
    db.commit()
    db.refresh(elevator)
    return elevator

def update_elevator_status(db: Session, elevator_id: int, floor: int, is_moving: bool, is_occupied: bool):
    elevator = db.query(models.Elevator).get(elevator_id)
    if elevator:
        from_floor = elevator.current_floor
        elevator.current_floor = floor
        elevator.is_moving = is_moving
        elevator.is_occupied = is_occupied
        elevator.last_updated = datetime.utcnow()
        db.commit()
        db.refresh(elevator)

        # Evento
        db.add(models.ElevatorEvent(
            elevator_id=elevator_id,
            event_type="MOVE" if is_moving else "REST",
            from_floor=from_floor,
            to_floor=floor
        ))
        db.commit()
        return elevator
    return None

def create_demand(db: Session, floor_called_from: int, elevator_id: int = 1):
    demand = models.Demand(floor_called_from=floor_called_from)
    db.add(demand)
    db.add(models.ElevatorEvent(
        elevator_id=elevator_id,
        event_type="CALL",
        from_floor=floor_called_from
    ))
    db.commit()
    return demand

def get_events(db: Session):
    return db.query(models.ElevatorEvent).all()
