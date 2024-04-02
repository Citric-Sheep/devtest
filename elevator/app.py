"""
API Endpoints.
"""

from http import HTTPStatus
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from elevator import crud, schema
from elevator.database import engine, get_session
from elevator.model import Base, ElevatorDb, ElevatorDemandDb

app = FastAPI()


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


DbDependency = Annotated[Session, Depends(get_session)]


@app.post("/elevators/", response_model=schema.Elevator)
def create_elevator(elevator: schema.ElevatorCreate, session: DbDependency):
    return crud.create_elevator(session=session, elevator=ElevatorDb(**elevator.model_dump()))


@app.post("/elevator-requests/", response_model=schema.ElevatorDemand)
def create_elevator_demand(elevator_demand: schema.ElevatorDemandCreate, session: DbDependency):
    return crud.create_elevator_demand(
        session=session, elevator_demand=ElevatorDemandDb(**elevator_demand.model_dump())
    )


@app.get("/elevators/{elevator_id}", response_model=schema.Elevator)
def read_elevator(elevator_id: int, db: DbDependency):
    elevator = crud.get_elevator(db, elevator_id)
    if elevator is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Elevator not found.")
    return elevator


@app.get("/elevator-demands/", response_model=list[schema.ElevatorDemand])
def read_latest_elevator_demands(db: DbDependency, skip: int = 0, limit: int = 10):
    return crud.get_latest_elevator_demands(db, skip=skip, limit=limit)


@app.get("/elevators/", response_model=list[schema.Elevator])
def read_elevators(db: DbDependency, skip: int = 0, limit: int = 10):
    return crud.get_elevators(db, skip=skip, limit=limit)


@app.patch("/elevators/{elevator_id}", response_model=schema.Elevator)
def update_elevator(elevator_id: int, elevator: schema.ElevatorUpdate, db: DbDependency):
    updated_elevator = crud.update_elevator_name(db, elevator_id, elevator.name)
    if updated_elevator is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Elevator not found.")
    return updated_elevator


@app.delete("/elevators/{elevator_id}")
def delete_elevator(elevator_id: int, db: DbDependency) -> dict:
    elevator = crud.get_elevator(db, elevator_id)
    if elevator is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Elevator not found.")
    crud.delete_elevator(db, elevator_id)
    return {"message": "Elevator deleted successfully."}


@app.get("/top-floor-demand/by-time")
def get_top_floor_demand_by_time(db: DbDependency, time_window: int = 10) -> dict:
    most_demanded_floor = crud.top_floor_demand_by_time(db, time_window)
    if most_demanded_floor is None:
        return {"message": "No elevator demands found in the specified time window."}
    return {"most_demanded_floor": most_demanded_floor}


@app.get("/top-floor-demand/by-time-and-dow")
def get_top_floor_demand_by_time_and_dow(db: DbDependency, time_window: int = 10) -> dict:
    most_demanded_floor = crud.top_floor_demand_by_time_and_dow(db, time_window)
    if most_demanded_floor is None:
        return {
            "message": "No elevator demands found in the specified time window and day of the week."
        }
    return {"most_demanded_floor": most_demanded_floor}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
