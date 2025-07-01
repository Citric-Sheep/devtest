from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from typing import List, Optional
from datetime import datetime, timedelta

from src.database import get_db
from src.models.elevator_demand import ElevatorDemand
from src.models.elevator import Elevator
from src.schemas import ElevatorDemandCreate, ElevatorDemand as ElevatorDemandSchema
from src.schemas import DemandAnalytics, TimeBasedDemandAnalytics, FloorDirectionAnalytics

router = APIRouter()

@router.post("/", response_model=ElevatorDemandSchema, status_code=201)
def create_demand(demand: ElevatorDemandCreate, db: Session = Depends(get_db)):
    """
    Record a new elevator demand.
    
    This endpoint records when someone calls an elevator from a specific floor,
    indicating which direction they want to go and which elevator responded to this demand.
    """
    # Validate direction
    if demand.direction not in ["up", "down"]:
        raise HTTPException(status_code=400, detail="Direction must be 'up' or 'down'")
    
    # Validate elevator_id
    elevator = db.query(Elevator).filter(Elevator.id == demand.elevator_id).first()
    if elevator is None:
        raise HTTPException(status_code=404, detail="Elevator not found")
    
    db_demand = ElevatorDemand(
        floor=demand.floor, 
        direction=demand.direction,
        elevator_id=demand.elevator_id
    )
    db.add(db_demand)
    db.commit()
    db.refresh(db_demand)
    return db_demand

@router.get("/", response_model=List[ElevatorDemandSchema])
def get_demands(
    skip: int = 0, 
    limit: int = 100,
    floor: Optional[int] = None,
    direction: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    """
    Get elevator demands with optional filtering.
    
    This endpoint retrieves historical demand data with various filtering options.
    """
    query = db.query(ElevatorDemand)
    
    # Apply filters if provided
    if floor is not None:
        query = query.filter(ElevatorDemand.floor == floor)
    if direction is not None:
        if direction not in ["up", "down"]:
            raise HTTPException(status_code=400, detail="Direction must be 'up' or 'down'")
        query = query.filter(ElevatorDemand.direction == direction)
    if start_date is not None:
        query = query.filter(ElevatorDemand.timestamp >= start_date)
    if end_date is not None:
        query = query.filter(ElevatorDemand.timestamp <= end_date)
    
    # Apply pagination and return results
    return query.order_by(ElevatorDemand.timestamp.desc()).offset(skip).limit(limit).all()

@router.get("/analytics/demand-by-floor", response_model=List[DemandAnalytics])
def get_demand_by_floor(
    start_date: Optional[datetime] = Query(None, description="Start date for analysis"),
    end_date: Optional[datetime] = Query(None, description="End date for analysis"),
    db: Session = Depends(get_db)
):
    """
    Get demand frequency by floor.
    
    This endpoint analyzes historical demand data to show which floors
    have the highest demand frequency within the specified date range.
    """
    # Default to last 7 days if no dates provided
    if start_date is None:
        start_date = datetime.now() - timedelta(days=7)
    if end_date is None:
        end_date = datetime.now()
    
    result = db.query(
        ElevatorDemand.floor,
        func.count(ElevatorDemand.id).label("count")
    ).filter(
        ElevatorDemand.timestamp >= start_date,
        ElevatorDemand.timestamp <= end_date
    ).group_by(
        ElevatorDemand.floor
    ).order_by(
        func.count(ElevatorDemand.id).desc()
    ).all()
    
    return [{"floor": floor, "count": count} for floor, count in result]

@router.get("/analytics/demand-by-hour", response_model=List[TimeBasedDemandAnalytics])
def get_demand_by_hour(
    start_date: Optional[datetime] = Query(None, description="Start date for analysis"),
    end_date: Optional[datetime] = Query(None, description="End date for analysis"),
    floor: Optional[int] = Query(None, description="Filter by specific floor"),
    db: Session = Depends(get_db)
):
    """
    Get demand frequency by hour of day and floor.
    
    This endpoint analyzes historical demand data to show which hours
    of the day have the highest demand frequency for each floor within 
    the specified date range.
    """
    # Default to last 7 days if no dates provided
    if start_date is None:
        start_date = datetime.now() - timedelta(days=7)
    if end_date is None:
        end_date = datetime.now()
    
    query = db.query(
        extract('hour', ElevatorDemand.timestamp).label("hour"),
        ElevatorDemand.floor,
        func.count(ElevatorDemand.id).label("count")
    ).filter(
        ElevatorDemand.timestamp >= start_date,
        ElevatorDemand.timestamp <= end_date
    )
    
    # Apply floor filter if provided
    if floor is not None:
        query = query.filter(ElevatorDemand.floor == floor)
    
    result = query.group_by(
        extract('hour', ElevatorDemand.timestamp),
        ElevatorDemand.floor
    ).order_by(
        extract('hour', ElevatorDemand.timestamp),
        ElevatorDemand.floor
    ).all()
    
    return [{"hour": hour, "floor": floor, "count": count} for hour, floor, count in result]

@router.get("/analytics/direction-distribution", response_model=List[FloorDirectionAnalytics])
def get_direction_distribution(
    start_date: Optional[datetime] = Query(None, description="Start date for analysis"),
    end_date: Optional[datetime] = Query(None, description="End date for analysis"),
    db: Session = Depends(get_db)
):
    """
    Get up/down distribution by floor.
    
    This endpoint analyzes historical demand data to show the distribution
    of up vs. down requests for each floor within the specified date range.
    """
    # Default to last 7 days if no dates provided
    if start_date is None:
        start_date = datetime.now() - timedelta(days=7)
    if end_date is None:
        end_date = datetime.now()
    
    # Get up counts by floor
    up_counts = db.query(
        ElevatorDemand.floor,
        func.count(ElevatorDemand.id).label("up_count")
    ).filter(
        ElevatorDemand.timestamp >= start_date,
        ElevatorDemand.timestamp <= end_date,
        ElevatorDemand.direction == "up"
    ).group_by(
        ElevatorDemand.floor
    ).subquery()
    
    # Get down counts by floor
    down_counts = db.query(
        ElevatorDemand.floor,
        func.count(ElevatorDemand.id).label("down_count")
    ).filter(
        ElevatorDemand.timestamp >= start_date,
        ElevatorDemand.timestamp <= end_date,
        ElevatorDemand.direction == "down"
    ).group_by(
        ElevatorDemand.floor
    ).subquery()
    
    # Join the results
    result = db.query(
        ElevatorDemand.floor,
        func.coalesce(up_counts.c.up_count, 0).label("up_count"),
        func.coalesce(down_counts.c.down_count, 0).label("down_count")
    ).outerjoin(
        up_counts, ElevatorDemand.floor == up_counts.c.floor
    ).outerjoin(
        down_counts, ElevatorDemand.floor == down_counts.c.floor
    ).group_by(
        ElevatorDemand.floor
    ).order_by(
        ElevatorDemand.floor
    ).all()
    
    return [
        {"floor": floor, "up_count": up_count, "down_count": down_count} 
        for floor, up_count, down_count in result
    ]
