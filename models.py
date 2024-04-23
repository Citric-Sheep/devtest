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
        # for now resting floor will be the where_to floor
        return where_to

    @classmethod
    async def initial_condition(cls, engine):
        logger = logging.getLogger(f"{__name__}.{__class__.__name__}")
        async with AsyncSession(engine) as session:
            session.begin()
            # Pongo un coso para ver si algo falló
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
                logger.info("Todo fue insertado correctamente en 'Elevator'")
            except Exception as e:
                await session.rollback()
                raise e
