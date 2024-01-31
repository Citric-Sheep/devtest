from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from src.repository import FloorRepository
from src.routers.schemas.floor_schema import FloorCreate, FloorResponse
from src.models import Floor
from src.database import get_db


import logging
logger = logging.getLogger()

router = APIRouter(
    prefix="/floor",
    tags=['Floor']
)

def get_floor_repository(db: Session = Depends(get_db)):
    return FloorRepository(db)

@router.post("/floor/", response_model=FloorResponse)
def create_floor(floor: FloorCreate, repo: FloorRepository = Depends(get_floor_repository)):
    floor_model = Floor(**floor.dict())
    return repo.add(floor_model)

@router.get("/floor/{floor_id}", response_model=FloorResponse)
def read_floor(floor_id: int, repo: FloorRepository = Depends(get_floor_repository)):
    floor = repo.get(Floor, floor_id)
    if floor is None:
        raise HTTPException(status_code=404, detail="Floor not found")
    return floor

@router.put("/floor/{floor_id}", response_model=FloorResponse)
def update_floor(floor_id: int, floor: FloorCreate, repo: FloorRepository = Depends(get_floor_repository)):
    existing_floor = repo.get(Floor, floor_id)
    if existing_floor is None:
        raise HTTPException(status_code=404, detail="Floor not found")
    existing_floor.name = floor.name
    return repo.add(existing_floor)

@router.delete("/floor/{floor_id}", response_model=FloorResponse)
def delete_floor(floor_id: int, repo: FloorRepository = Depends(get_floor_repository)):
    floor = repo.get(Floor, floor_id)
    if floor is None:
        raise HTTPException(status_code=404, detail="Floor not found")
    repo.db_session.delete(floor)
    repo.db_session.commit()
    return floor