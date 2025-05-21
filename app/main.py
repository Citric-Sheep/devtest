from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import Base, engine, SessionLocal

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Elevator ML Data Logger")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@app.post("/elevators/", response_model=schemas.Elevator)
def create_elevator(elevator: schemas.ElevatorCreate, db: Session = Depends(get_db)):
    return crud.create_elevator(db, elevator)

@app.post("/demand/", response_model=schemas.Demand)
def create_demand(demand: schemas.DemandCreate, db: Session = Depends(get_db)):
    return crud.create_demand(db, demand)

@app.post("/resting/", response_model=schemas.RestingPeriod)
def create_resting(resting: schemas.RestingCreate, db: Session = Depends(get_db)):
    return crud.create_resting(db, resting)

@app.patch("/resting/{resting_id}/end", response_model=schemas.RestingPeriod)
def end_resting(resting_id: int, end: schemas.RestingEnd, db: Session = Depends(get_db)):
    result = crud.end_resting(db, resting_id, end.end_time)
    if not result:
        raise HTTPException(status_code=404, detail="Resting not found")
    return result

@app.get("/demands/", response_model=list[schemas.Demand])
def get_demands(db: Session = Depends(get_db)):
    return crud.get_demands(db)

@app.get("/restings/", response_model=list[schemas.RestingPeriod])
def get_restings(db: Session = Depends(get_db)):
    return crud.get_restings(db)

@app.get("/export/")
def export_all(db: Session = Depends(get_db)):
    demands = crud.get_demands(db)
    restings = crud.get_restings(db)
    #Return as flat JSON for ML
    return {
        "demands": [d.__dict__ for d in demands],
        "restings": [r.__dict__ for r in restings]
    }