"""Service Layer"""

from typing import List

from fastapi import HTTPException
from pydantic import UUID4
from sqlalchemy.orm.session import Session

from app.repository import ElevatorDemandRepository
from app.schemas import ElevatorDemandInput, ElevatorDemandOutput


class ElevatorDemandService:
    """Service to interact with ElevatorDemand Repository"""

    def __init__(self, session: Session) -> None:
        """Init function"""
        self.repository = ElevatorDemandRepository(session=session)

    def create(self, input_: ElevatorDemandInput) -> ElevatorDemandOutput:
        """Create demand in db"""
        if input_.origin == input_.destination:
            raise HTTPException(
                status_code=400, detail="Origin and Destination floors are the same."
            )
        return self.repository.create(input_)

    def get_all(self) -> List[ElevatorDemandOutput]:
        """List all demand in db"""
        return self.repository.get_all()

    def get_one(self, id_: UUID4) -> ElevatorDemandOutput:
        """Get details of certain demand from db"""
        item = self.repository.get_item(id_)
        if not item:
            raise HTTPException(status_code=400, detail="Demand object does not exist.")
        return ElevatorDemandOutput(**item.__dict__)

    def update(self, id_: UUID4, new_data: ElevatorDemandInput) -> ElevatorDemandOutput:
        """Update demand details"""
        existing = self.repository.get_item(item_id=id_)
        if not bool(existing):
            raise HTTPException(status_code=400, detail="Demand object does not exist.")
        return self.repository.update(item=existing, new_data=new_data)

    def delete(self, id_: UUID4) -> bool:
        """Delete existing demand"""
        existing = self.repository.get_item(item_id=id_)
        if not bool(existing):
            raise HTTPException(status_code=400, detail="Demand object does not exist.")
        return self.repository.delete(item=existing)
