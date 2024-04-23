from database import drop_all_tables, setup_database, engine

from models import Elevator

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import asyncio

import logging

logger = logging.getLogger(__name__)


async def initialize_db(from_scratch=True):
    # engine = await engine_to_database()
    if from_scratch:
        await drop_all_tables(engine)
        await setup_database(engine)
        await Elevator.initial_condition(engine)
    # yield engine
    await engine.dispose()


async def initial_condition(async_session: AsyncSession):
    logger.info("Initial condition")
    async_session.begin()
    init = Elevator(prev_resting_floor=0, whos_calling=0, where_to=0, resting_floor=0)
    async_session.add(init)
    try:
        await async_session.commit()
    except Exception as e:
        await async_session.rollback()
        raise e
    return init


async def get_states(async_session: AsyncSession, limit: int = 3):
    logger.info("Getting states")
    async_session.begin()
    query = select(Elevator).order_by(Elevator.time_stamp.desc()).limit(limit)
    result = await async_session.execute(query)
    states = result.scalars().all()
    await async_session.commit()
    return states


async def get_current_floor(async_session: AsyncSession):
    logger.info("Getting current floor")
    async_session.begin()
    query = select(Elevator).order_by(Elevator.time_stamp.desc()).limit(1)
    result = await async_session.execute(query)
    floor = result.scalar()
    await async_session.commit()
    return floor


async def call_elevator(from_floor: int, to_floor: int, async_session: AsyncSession):
    logger.info(f"Calling elevator from {from_floor} to {to_floor}")
    async_session.begin()
    prev_resting_floor = await get_current_floor(async_session)
    floor = prev_resting_floor.resting_floor
    elevator_event = Elevator(
        prev_resting_floor=floor,
        whos_calling=from_floor,
        where_to=to_floor,
        resting_floor=Elevator.resting_floor_logic(where_to=to_floor),
    )

    async_session.add(elevator_event)
    try:
        await async_session.commit()
    except Exception as e:
        await async_session.rollback()
        raise e
    return elevator_event


if __name__ == "__main__":
    import asyncio
    from pathlib import Path

    this_dir = Path(__file__).parent

    logging.basicConfig(
        level=logging.INFO,
        handlers=[
            logging.FileHandler(
                Path(this_dir.joinpath("./logs/db_creation.log")), mode="w"
            ),
            logging.StreamHandler(),
        ],
        format="(%(name)s) - %(asctime)s - %(levelname)s - %(message)s",
    )
    logger = logging.getLogger(__name__)

    asyncio.run(initialize_db(from_scratch=True))
