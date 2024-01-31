from pydantic import BaseModel
from typing import Optional


class DemandCreate(BaseModel):
    from_floor: int
    to_floor: int
    status: str

class DemandResponse(BaseModel):
    id: int
    from_floor: int
    to_floor: int
    created_at: str
    status: str
