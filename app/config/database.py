"""Database config"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from app.models import ElevatorDemand

engine = create_engine("sqlite:///database.sqlite")
local_session = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def create_database() -> None:
    """
    Create tables and sqlite db file.
    :return: None
    """
    ElevatorDemand.metadata.create_all(bind=engine)


def get_db_session() -> Session:
    """
    Generate a database session.
    :return: DB session
    """
    db_session = local_session()
    try:
        yield db_session
    finally:
        db_session.close()


if __name__ == "__main__":
    pass
