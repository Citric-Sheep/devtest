"""
Modelos SQLAlchemy
"""

from database import Base
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import insert
from datetime import datetime

import logging

logger = logging.getLogger(__name__)


class Elevator(Base):
    __tablename__ = "elevator"
    id: Mapped[int] = mapped_column(primary_key=True)
    time_stamp: Mapped[datetime] = mapped_column(insert_default=datetime.now())
    prev_resting_floor: Mapped[int] = mapped_column()
    whos_calling: Mapped[int] = mapped_column()
    where_to: Mapped[int] = mapped_column()
    resting_floor: Mapped[int] = mapped_column()

    @classmethod
    def resting_floor_logic(cls, where_to: int):
        """
        This eventually would be what the prediction model will determine the best strategy.
        Just for fun I will avoid the resting floor to be the 13th floor.
        """
        return where_to if where_to != 13 else 12

    @classmethod
    async def initial_condition(cls, engine):
        """
        Initial condition for the elevator
        """
        logger = logging.getLogger(f"{__name__}.{__class__.__name__}")
        async with AsyncSession(engine) as session:
            session.begin()
            try:
                await session.execute(
                    insert(Elevator).values(
                        prev_resting_floor=0,
                        whos_calling=0,
                        where_to=0,
                        resting_floor=0,
                    )
                )
                await session.flush()
                await session.commit()
                logger.info(f"{Elevator.__tablename__} initialized")
            except Exception as e:
                await session.rollback()
                raise e
