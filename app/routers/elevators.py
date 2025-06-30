from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models.elevators import Demand, ElevatorState
from app.schemas.elevators import DemandOut, DemandCreate, StateOut, StateCreate
from app.database.elevators import SessionLocal

router = APIRouter(prefix="/api", tags=["elevators"])


def get_db():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


# POST /demands
@router.post("/demands", response_model=DemandOut)
def create_demand(demand: DemandCreate, db: Session = Depends(get_db)):
    """
    Registers a new elevator demand when a user calls the elevator from a specific floor.
    """
    rec = Demand(floor=demand.floor)
    db.add(rec)
    db.flush()
    db.refresh(rec)
    return rec


# POST /state
@router.post("/state", response_model=StateOut)
def create_state(state: StateCreate, db: Session = Depends(get_db)):
    """
    Records the elevator’s current state, including its current floor and whether it is vacant.
    """
    rec = ElevatorState(floor=state.floor, vacant=state.vacant)
    db.add(rec)
    db.flush()
    db.refresh(rec)
    return rec


# GET /analytics
@router.get("/analytics")
def analyze_positioning(db: Session = Depends(get_db), limit: int = 50, threshold: int = 3):
    """
    Analyzes elevator positioning efficiency by comparing resting positions with upcoming demands.
    """
    states = (
        db.query(ElevatorState)
        .order_by(ElevatorState.timestamp.asc())
        .limit(limit)
        .all()
    )

    if not states:
        raise HTTPException(status_code=404, detail="No elevator states found.")

    distances = []

    for state in states:
        demand = (
            db.query(Demand)
            .filter(Demand.timestamp > state.timestamp)
            .order_by(Demand.timestamp.asc())
            .first()
        )
        if demand:
            distance = abs(demand.floor - state.floor)
            distances.append(distance)

    if not distances:
        raise HTTPException(status_code=404, detail="Not enough state → demand pairs found.")

    avg_distance = sum(distances) / len(distances)

    return {
        "average_distance": round(avg_distance, 2),
        "threshold": threshold,
        "mispositioned": avg_distance > threshold,
        "message": "Elevator is frequently poorly positioned." if avg_distance > threshold else "Positioning is within acceptable range."
    }
