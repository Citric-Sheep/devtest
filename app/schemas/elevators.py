from datetime import datetime
from pydantic import BaseModel, Field


class DemandCreate(BaseModel):
    floor: int = Field(..., ge=0, description="Andar onde o usuário chamou o elevador")

class DemandOut(DemandCreate):
    id: int
    timestamp: datetime

    model_config = {
        "from_attributes": True  # substitui orm_mode no Pydantic v2
    }
    

class StateCreate(BaseModel):
    floor: int
    vacant: bool

class StateOut(StateCreate):
    id: int
    timestamp: datetime

    model_config = {
        "from_attributes": True
    }