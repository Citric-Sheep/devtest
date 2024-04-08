"""Schemas module"""

from pydantic import UUID4, BaseModel, Field


class ElevatorDemandInput(BaseModel):
    """Elevator Demand schema to validate input."""

    origin: int = Field(ge=0)
    destination: int = Field(ge=0)


class ElevatorDemandOutput(BaseModel):
    """Elevator Demand schema in output."""

    id: UUID4
    origin: int
    destination: int
