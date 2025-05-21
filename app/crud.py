from sqlalchemy.orm import Session
from . import models, schemas
from datetime import timedelta

def create_elevator(db: Session, elevator: schemas.ElevatorCreate):
    db_elevator = models.Elevator(name=elevator.name)
    db.add(db_elevator)
    db.commit()
    db.refresh(db_elevator)
    return db_elevator

def create_demand(db: Session, demand: schemas.DemandCreate):
    #Business Rule: Demand Surge Tag
    five_min_ago = demand.timestamp - timedelta(minutes=5)
    recent = db.query(models.DemandEvent).filter(
        models.DemandEvent.floor == demand.floor,
        models.DemandEvent.timestamp >= five_min_ago
    ).count()
    surge = recent >= 2 #Third demand triggers it
    db_demand = models.DemandEvent(**demand.dict(), surge_tag=surge)
    db.add(db_demand)
    db.commit()
    db.refresh(db_demand)
    all_demands = db.query(models.DemandEvent).all()
    #print(f"ALL DEMANDS IN DB: {[{'floor': d.floor, 'timestamp': d.timestamp} for d in all_demands]}")
    #print(f"DEBUG: floor={demand.floor}, timestamp={demand.timestamp}, recent={recent}, surge={surge} ")
    return db_demand

def create_resting(db: Session, resting: schemas.RestingCreate):
    #Business Rule: Peak Hours & non-optimal rest
    hour = resting.start_time.hour
    peak = (7 <= hour < 10) or (16 <= hour < 19)
    non_optimal = peak and resting.floor != 1
    db_resting = models.RestingPeriod(
        **resting.dict(),
        peak_hours_flag=peak,
        non_optimal_rested=non_optimal
    )
    db.add(db_resting)
    db.commit()
    db.refresh(db_resting)
    return db_resting

def end_resting(db: Session, resting_id: int, end_time):
    from datetime import timezone
    rest = db.query(models.RestingPeriod).filter(models.RestingPeriod.id == resting_id).first()
    if rest:
        rest.end_time = end_time
        rest.duration_sec = int((end_time - rest.start_time).total_seconds())
        #Business Rule: Idle Relocation
        rest.relocation_flag = rest.duration_sec > 600
        db.commit()
        db.refresh(rest)
    return rest

def get_demands(db: Session):
    return db.query(models.DemandEvent).all()

def get_restings(db: Session):
    return db.query(models.RestingPeriod).all()