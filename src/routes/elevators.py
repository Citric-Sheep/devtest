from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from src.database import get_db
from src.models.elevator import Elevator
from src.schemas import ElevatorCreate, Elevator as ElevatorSchema, ElevatorDemand

router = APIRouter()

@router.post("/", response_model=ElevatorSchema, status_code=201)
def create_elevator(elevator: ElevatorCreate, db: Session = Depends(get_db)):
    """
    Register a new elevator.
    
    This endpoint adds a new elevator to the system.
    """
    # Validate floor values
    if elevator.min_floor >= elevator.max_floor:
        raise HTTPException(
            status_code=400, 
            detail="min_floor must be less than or equal to max_floor"
        )
    
    db_elevator = Elevator(
        building_id=elevator.building_id,
        max_floor=elevator.max_floor,
        min_floor=elevator.min_floor
    )
    db.add(db_elevator)
    db.commit()
    db.refresh(db_elevator)
    return db_elevator

@router.get("/", response_model=List[ElevatorSchema])
def get_elevators(
    skip: int = 0, 
    limit: int = 100,
    building_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    Get elevators with optional filtering.
    
    This endpoint retrieves elevators with various filtering options.
    """
    query = db.query(Elevator)
    
    # Apply filters if provided
    if building_id is not None:
        query = query.filter(Elevator.building_id == building_id)
    
    # Apply pagination and return results
    return query.offset(skip).limit(limit).all()

@router.get("/{elevator_id}", response_model=ElevatorSchema)
def get_elevator(elevator_id: int, db: Session = Depends(get_db)):
    """
    Get details for a specific elevator.
    
    This endpoint retrieves information about a specific elevator by ID.
    """
    elevator = db.query(Elevator).filter(Elevator.id == elevator_id).first()
    if elevator is None:
        raise HTTPException(status_code=404, detail="Elevator not found")
    return elevator

@router.put("/{elevator_id}", response_model=ElevatorSchema)
def update_elevator(
    elevator_id: int, 
    elevator: ElevatorCreate, 
    db: Session = Depends(get_db)
):
    """
    Update an existing elevator.
    
    This endpoint updates information for an existing elevator.
    """
    db_elevator = db.query(Elevator).filter(Elevator.id == elevator_id).first()
    if db_elevator is None:
        raise HTTPException(status_code=404, detail="Elevator not found")
    
    # Validate floor values
    if elevator.min_floor >= elevator.max_floor:
        raise HTTPException(
            status_code=400, 
            detail="min_floor must be less than or equal to max_floor"
        )
    
    # Update elevator attributes
    db_elevator.building_id = elevator.building_id
    db_elevator.max_floor = elevator.max_floor
    db_elevator.min_floor = elevator.min_floor
    
    db.commit()
    db.refresh(db_elevator)
    return db_elevator

@router.delete("/{elevator_id}", status_code=204)
def delete_elevator(elevator_id: int, db: Session = Depends(get_db)):
    """
    Delete an elevator.
    
    This endpoint removes an elevator from the system.
    """
    db_elevator = db.query(Elevator).filter(Elevator.id == elevator_id).first()
    if db_elevator is None:
        raise HTTPException(status_code=404, detail="Elevator not found")
    
    db.delete(db_elevator)
    db.commit()
    return None

@router.get("/{elevator_id}/demands", response_model=List[ElevatorDemand])
def get_elevator_demands(
    elevator_id: int, 
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get demands for a specific elevator.
    
    This endpoint retrieves all demands that were handled by a specific elevator.
    """
    # Check if elevator exists
    elevator = db.query(Elevator).filter(Elevator.id == elevator_id).first()
    if elevator is None:
        raise HTTPException(status_code=404, detail="Elevator not found")
    
    # Get demands for this elevator
    from src.models.elevator_demand import ElevatorDemand as ElevatorDemandModel
    demands = db.query(ElevatorDemandModel).filter(
        ElevatorDemandModel.elevator_id == elevator_id
    ).offset(skip).limit(limit).all()
    
    return demands
