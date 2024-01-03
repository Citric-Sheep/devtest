from .schemas import EventCreate
from .models import Event
from sqlalchemy.orm import Session
from datetime import datetime, timedelta



def insert_event(session: Session, event: EventCreate):
    db_event = Event(**event.model_dump())
    session.add(db_event)
    session.commit()
    session.refresh(db_event)

    return db_event


# TODO: implement pagination to handle long timespans
def list_events(session: Session, elevator_id: int, seconds: int = 30) -> list[Event]:
    time_threshold = datetime.utcnow() - timedelta(seconds=seconds)

    events = session.query(Event).\
        filter(Event.elevator_id == elevator_id).\
        filter(Event.inserted_at >= time_threshold).\
        all()

    return events