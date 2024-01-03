from pydantic import BaseModel
from datetime import datetime
from enum import Enum


class EventType(Enum):
    door_opened = 'door_opened'
    door_closed = 'door_closed'
    elevator_overloaded = 'elevator_overloaded'
    elevator_started = 'elevator_started'
    floor_reached = 'floor_reached'
    floor_selected = 'floor_selected'
    elevator_demanded = 'elevator_demanded'



class EventBase(BaseModel):
    event_type: EventType
    current_floor: int
    target_floor: int
    load: int
    is_vacant: bool
    captured_at: datetime
    elevator_id: int

class EventCreate(EventBase):
    pass

class EventOutput(EventBase):
    id: int
    inserted_at: datetime



