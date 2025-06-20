from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import crud, schemas

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/elevator/")
def create_elevator(payload: schemas.ElevatorCreate, db: Session = Depends(get_db)):
    return crud.create_elevator(db, current_floor=payload.current_floor)

@router.patch("/elevator/{elevator_id}/status")
def update_status(elevator_id: int, payload: schemas.ElevatorStatusUpdate, db: Session = Depends(get_db)):
    result = crud.update_elevator_status(db, elevator_id, payload.current_floor, payload.is_moving, payload.is_occupied)
    return {"status": "updated"} if result else {"status": "elevator not found"}

@router.post("/demand/")
def create_demand(payload: schemas.DemandCreate, db: Session = Depends(get_db)):
    crud.create_demand(db, floor_called_from=payload.floor_called_from)
    return {"status": "demand recorded"}

@router.get("/events/", response_model=list[schemas.Event])
def get_all_events(db: Session = Depends(get_db)):
    return crud.get_events(db)
