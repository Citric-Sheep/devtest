from pydantic import BaseModel

class Demand(BaseModel):
    src_floor : int
    dest_floor : int
    weight : float