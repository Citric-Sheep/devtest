"""
SQLAlchemy DB session.
"""

from pathlib import Path
from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

DB_PATH = Path(__file__).resolve().parent.parent / "assets" / "test.db"
# Using SQLite for the given scope and simplicity
DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(DATABASE_URL, echo=True)


def get_session() -> Iterator[Session]:
    with Session(engine) as session:
        yield session
