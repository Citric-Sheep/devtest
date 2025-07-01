import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta

from src.main import app
from src.database import get_db
from src.models.elevator import Elevator
from src.models.elevator_demand import ElevatorDemand

# Create a test client
client = TestClient(app)

@pytest.fixture
def mock_db():
    """Create a mock database session."""
    mock = MagicMock()
    return mock

@pytest.fixture
def mock_get_db(mock_db):
    """Override the get_db dependency for testing."""
    def _get_db():
        yield mock_db
    
    # Override the dependency in the app
    app.dependency_overrides[get_db] = _get_db
    
    yield mock_db
    
    # Clean up after the test
    app.dependency_overrides.clear()

@pytest.fixture
def sample_elevator():
    """Create a sample elevator for testing."""
    # Create a mock elevator instead of a real model instance
    elevator = MagicMock()
    elevator.id = 1
    elevator.building_id = 1
    elevator.max_floor = 10
    elevator.min_floor = 0
    
    # Configure the mock to work with FastAPI's response_model
    elevator.__getitem__.side_effect = lambda key: getattr(elevator, key)
    elevator.keys.return_value = ["id", "building_id", "max_floor", "min_floor"]
    elevator.__iter__.return_value = iter(["id", "building_id", "max_floor", "min_floor"])
    
    return elevator

@pytest.fixture
def sample_demands(sample_elevator):
    """Create sample demand data for testing."""
    now = datetime.now()
    
    # Create mock demand objects
    demands = []
    for i, (floor, direction, time_offset) in enumerate([
        (1, "up", timedelta(hours=2)),
        (3, "down", timedelta(hours=1)),
        (5, "up", timedelta(hours=0)),
        (1, "up", timedelta(days=2)),
        (3, "up", timedelta(days=1))
    ], 1):
        demand = MagicMock()
        demand.id = i
        demand.floor = floor
        demand.direction = direction
        demand.timestamp = now - time_offset
        demand.elevator_id = sample_elevator.id
        
        # Configure the mock to work with FastAPI's response_model
        demand.__getitem__.side_effect = lambda key: getattr(demand, key)
        demand.keys.return_value = ["id", "floor", "direction", "timestamp", "elevator_id"]
        demand.__iter__.return_value = iter(["id", "floor", "direction", "timestamp", "elevator_id"])
        
        demands.append(demand)
    
    return demands
