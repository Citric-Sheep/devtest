import os
import tempfile
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from src.db import Base
from src.main import app
from src.models import Building, Elevator, ElevatorCall, ElevatorTrip, ElevatorState, TimeStatistic, FloorStatistic

@pytest.fixture
def client():
    # Create a temporary database file
    db_fd, db_path = tempfile.mkstemp()
    app.config['TESTING'] = True
    
    # Override the database URL
    test_db_url = f'sqlite:///{db_path}'
    
    # Create test engine and session
    engine = create_engine(test_db_url)
    session_factory = sessionmaker(bind=engine)
    Session = scoped_session(session_factory)
    
    # Create tables
    Base.metadata.create_all(engine)
    
    # Patch the app to use the test database
    with app.app_context():
        app.config['DATABASE_URL'] = test_db_url
        
        # Create a test client
        with app.test_client() as client:
            yield client
    
    # Clean up
    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def db_session(client):
    # Create a new session for each test
    engine = create_engine(app.config['DATABASE_URL'])
    session_factory = sessionmaker(bind=engine)
    session = session_factory()
    
    try:
        yield session
    finally:
        session.close()

@pytest.fixture
def sample_building(db_session):
    building = Building(name="Test Building", floors=10)
    db_session.add(building)
    db_session.commit()
    return building

@pytest.fixture
def sample_elevator(db_session, sample_building):
    elevator = Elevator(building_id=sample_building.id, name="Test Elevator")
    db_session.add(elevator)
    db_session.commit()
    return elevator