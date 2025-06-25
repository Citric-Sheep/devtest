from pydantic import BaseModel

class RestingFloorRequest(BaseModel):
    hour: int
    weekday: int
    demand_count: int
    avg_floor: float
    most_common_floor: int
    avg_direction: float
    peak_hours: int
