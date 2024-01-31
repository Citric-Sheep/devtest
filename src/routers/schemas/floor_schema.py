from pydantic import BaseModel
from typing import Optional


class FloorCreate(BaseModel):
    name: str

class FloorResponse(BaseModel):
    id: int
    name: str