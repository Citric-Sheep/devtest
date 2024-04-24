"""
Main
"""

from fastapi import FastAPI, HTTPException
from sqlalchemy.ext.asyncio import async_sessionmaker

from schemas import ElevatorState, ElevatorGet, ElevatorCall
import services
from database import engine

import logging
from pathlib import Path

### Preparación
this_dir = Path(__file__).parent
logfile = Path(this_dir.joinpath("logs/elevator.log"))
logfile.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    handlers=[
        logging.FileHandler(logfile, mode="w"),
        logging.StreamHandler(),
    ],
    format="(%(name)s) - %(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Armo la session
async_session = async_sessionmaker(bind=engine, expire_on_commit=False)

# Armo el objeto de la app
app = FastAPI(
    title="devtest",
    description="API citric sheep",
)


# Endpoint para obtener los ultimos 3 llamados de ascensor
@app.get("/elevator/", response_model=list[ElevatorGet])
async def get_events(limit: int = 3):
    session = async_session()
    events = await services.get_states(async_session=session, limit=limit)
    if not events:
        raise HTTPException(status_code=404, detail="No events found")
    await session.close()
    return events


@app.get("/elevator/resting_floor", response_model=ElevatorState)
async def get_current_floor():
    session = async_session()
    floor = await services.get_current_floor(async_session=session)
    if not floor:
        raise HTTPException(status_code=404, detail="No events found")
    await session.close()
    return floor


@app.post("/elevator/call", response_model=ElevatorCall)
async def call_elevator(from_floor: int, to_floor: int):
    session = async_session()
    elevator_event = await services.call_elevator(
        from_floor=from_floor, to_floor=to_floor, async_session=session
    )
    await session.close()
    return elevator_event
