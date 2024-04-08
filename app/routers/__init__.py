"""FastAPI Routers module"""

from typing import List

from fastapi import APIRouter, Depends
from pydantic import UUID4
from sqlalchemy.orm.session import Session

from app.config.database import get_db_session
from app.constants import WELCOME_MESSAGE
from app.schemas import ElevatorDemandInput, ElevatorDemandOutput
from app.service import ElevatorDemandService

default_router = APIRouter()
demand_router = APIRouter(prefix="/demand")


@demand_router.get(path="/", status_code=200, response_model=List[ElevatorDemandOutput])
def list_records(
    session: Session = Depends(get_db_session),
) -> List[ElevatorDemandOutput]:
    """Read all db records."""
    service = ElevatorDemandService(session=session)
    return service.get_all()


@demand_router.post(path="/", status_code=201, response_model=ElevatorDemandOutput)
def create_record(
    item: ElevatorDemandInput, session: Session = Depends(get_db_session)
) -> ElevatorDemandOutput:
    """Insert record in db."""
    service = ElevatorDemandService(session=session)
    return service.create(input_=item)


@demand_router.get(
    path="/{item_id}", status_code=200, response_model=ElevatorDemandOutput
)
def search_record(
    item_id: UUID4, session: Session = Depends(get_db_session)
) -> ElevatorDemandOutput:
    """Search record by ID."""
    service = ElevatorDemandService(session=session)
    return service.get_one(id_=item_id)


@demand_router.put(
    path="/{item_id}", status_code=200, response_model=ElevatorDemandOutput
)
def update_record(
    item_id: UUID4,
    new_data: ElevatorDemandInput,
    session: Session = Depends(get_db_session),
) -> ElevatorDemandOutput:
    """Update existing record."""
    service = ElevatorDemandService(session=session)
    return service.update(id_=item_id, new_data=new_data)


@demand_router.delete(path="/{item_id}", status_code=204)
def delete_record(item_id: UUID4, session: Session = Depends(get_db_session)) -> None:
    """Delete existing record."""
    service = ElevatorDemandService(session=session)
    service.delete(id_=item_id)


@default_router.get(path="/", status_code=200)
def main() -> dict:
    """Root endpoint"""
    return {"message": WELCOME_MESSAGE}
