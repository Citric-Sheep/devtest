from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from . import models, crud
from .database import SessionLocal, engine
from .crud import EventCreate
from .schemas import EventOutput


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/event/", response_model=EventOutput)
def create_event(event: EventCreate, db: Session = Depends(get_db)):
    db_event = crud.insert_event(db, event)
    return db_event


@app.get("/events/", response_model=list[EventOutput])
def list_events(elevator_id: int | None = None, seconds: int = 30, db: Session = Depends(get_db)):
    events = crud.list_events(db, elevator_id, seconds )
    return events

@app.get("/")
def index():
    return {"status": "ok"}