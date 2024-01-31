from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from src.repository import DemandRepository
from src.routers.schemas.demand_schema import DemandCreate, DemandResponse
from src.models import Demand
from src.database import get_db


import logging
logger = logging.getLogger()

router = APIRouter(
    prefix="/demand",
    tags=['Demand']
)

def get_demand_repository(db: Session = Depends(get_db)):
    return DemandRepository(db)

@router.post("/demand/", response_model=DemandResponse)
def create_demand(demand: DemandCreate, repo: DemandRepository = Depends(get_demand_repository)):
    demand_model = Demand(**demand.dict())
    return repo.add(demand_model)

@router.get("/demand/{demand_id}", response_model=DemandResponse)
def read_demand(demand_id: int, repo: DemandRepository = Depends(get_demand_repository)):
    demand = repo.get(Demand, demand_id)
    if demand is None:
        raise HTTPException(status_code=404, detail="Demand not found")
    return demand

@router.put("/demand/{demand_id}", response_model=DemandResponse)
def update_demand(demand_id: int, demand: DemandCreate, repo: DemandRepository = Depends(get_demand_repository)):
    existing_demand = repo.get(Demand, demand_id)
    if existing_demand is None:
        raise HTTPException(status_code=404, detail="Demand not found")
    existing_demand.from_floor = demand.from_floor
    existing_demand.to_floor = demand.to_floor
    return repo.add(existing_demand)

@router.delete("/demand/{demand_id}", response_model=DemandResponse)
def delete_demand(demand_id: int, repo: DemandRepository = Depends(get_demand_repository)):
    demand = repo.get(Demand, demand_id)
    if demand is None:
        raise HTTPException(status_code=404, detail="Demand not found")
    repo.db_session.delete(demand)
    repo.db_session.commit()
    return demand