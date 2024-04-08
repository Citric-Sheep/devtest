"""ORM module"""

from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Mapped, declarative_base, mapped_column

Base = declarative_base()


class Record(Base):
    """Elevator demand"""

    __tablename__ = "record"
    id: Mapped[int] = mapped_column(primary_key=True)
    origin: Mapped[int]
    destination: Mapped[int]

    def __repr__(self):
        """Representation"""
        return (
            f"Demand(id={self.id}, origin={self.origin} destination={self.destination})"
        )


def create_database(engine: Engine):
    """Create Database"""
    Base.metadata.create_all(engine)
