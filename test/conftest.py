"""
Module for sharing fixtures across multiple files
"""

from collections.abc import Iterator
from contextlib import closing

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import Session, sessionmaker

from elevator.app import app
from elevator.database import get_session
from elevator.model import Base


@pytest.fixture(scope="function")
def db_session() -> Iterator[Session]:
    """
    In-memory SQLite used for testing.
    """
    database_url = "sqlite:///:memory:"
    engine = create_engine(
        database_url, connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    Base.metadata.create_all(bind=engine)
    session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    with closing(session()) as db_session:
        yield db_session
    # Clean-up
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def test_client(db_session: Session) -> Iterator[TestClient]:
    """
    Override FastAPI app session with test one.

    Reference: https://fastapi.tiangolo.com/advanced/testing-database/
    """
    app.dependency_overrides[get_session] = lambda: db_session
    yield TestClient(app)
