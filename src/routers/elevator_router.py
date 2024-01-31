from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from src.repository import ElevatorRepository
from src.routers.schemas.elevator_schema import ElevatorCreate, ElevatorResponse
from src.models import Elevator
from src.database import get_db


import logging
logger = logging.getLogger()

router = APIRouter(
    prefix="/elevator",
    tags=['Elevator']
)

def get_elevator_repository(db: Session = Depends(get_db)):
    return ElevatorRepository(db)

@router.post("/elevator/", response_model=ElevatorResponse)
def create_elevator(elevator: ElevatorCreate, repo: ElevatorRepository = Depends(get_elevator_repository)):
    elevator_model = Elevator(**elevator.dict())
    return repo.add(elevator_model)

@router.get("/elevator/{elevator_id}", response_model=ElevatorResponse)
def read_elevator(elevator_id: int, repo: ElevatorRepository = Depends(get_elevator_repository)):
    elevator = repo.get(Elevator, elevator_id)
    if elevator is None:
        raise HTTPException(status_code=404, detail="Elevator not found")
    return elevator

@router.put("/elevator/{elevator_id}", response_model=ElevatorResponse)
def update_elevator(elevator_id: int, elevator: ElevatorCreate, repo: ElevatorRepository = Depends(get_elevator_repository)):
    existing_elevator = repo.get(Elevator, elevator_id)
    if existing_elevator is None:
        raise HTTPException(status_code=404, detail="Elevator not found")
    existing_elevator.current_floor = elevator.current_floor
    existing_elevator.resting_floor = elevator.resting_floor
    existing_elevator.status = elevator.status
    return repo.add(existing_elevator)

@router.delete("/elevator/{elevator_id}", response_model=ElevatorResponse)
def delete_elevator(elevator_id: int, repo: ElevatorRepository = Depends(get_elevator_repository)):
    elevator = repo.get(Elevator, elevator_id)
    if elevator is None:
        raise HTTPException(status_code=404, detail="Elevator not found")
    repo.db_session.delete(elevator)
    repo.db_session.commit()
    return elevator