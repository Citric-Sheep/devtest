import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from src.tests.conftest import client, mock_db, mock_get_db, sample_elevator, sample_demands
from src.models.elevator_demand import ElevatorDemand

def test_create_demand(mock_db, mock_get_db, sample_elevator):
    """Test creating a new demand."""
    # Setup mock
    mock_db.query.return_value.filter.return_value.first.return_value = sample_elevator
    
    # Create a mock for the new demand
    new_demand = ElevatorDemand(
        id=100,
        floor=3,
        direction="up",
        elevator_id=1,
        timestamp=datetime.now()
    )
    
    # Configure mock to return the new demand after add and refresh
    def mock_add(demand):
        return None
    
    def mock_refresh(demand):
        demand.id = new_demand.id
        demand.timestamp = new_demand.timestamp
        return None
    
    mock_db.add.side_effect = mock_add
    mock_db.refresh.side_effect = mock_refresh
    
    # Make the request
    response = client.post(
        "/demands/",
        json={
            "floor": 3,
            "direction": "up",
            "elevator_id": 1
        }
    )
    
    # Assertions
    assert response.status_code == 201
    data = response.json()
    assert data["floor"] == 3
    assert data["direction"] == "up"
    assert data["elevator_id"] == 1
    assert "id" in data
    assert "timestamp" in data
    
    # Verify mock calls
    mock_db.query.assert_called()
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()

def test_create_demand_invalid_direction(mock_db, mock_get_db, sample_elevator):
    """Test creating a demand with invalid direction."""
    # Setup mock
    mock_db.query.return_value.filter.return_value.first.return_value = sample_elevator
    
    # Make the request
    response = client.post(
        "/demands/",
        json={
            "floor": 3,
            "direction": "sideways",  # Invalid direction
            "elevator_id": sample_elevator.id
        }
    )
    
    # Assertions
    assert response.status_code == 400
    assert "Direction must be 'up' or 'down'" in response.json()["detail"]

def test_create_demand_invalid_elevator(mock_db, mock_get_db):
    """Test creating a demand with non-existent elevator ID."""
    # Setup mock to return None (elevator not found)
    mock_db.query.return_value.filter.return_value.first.return_value = None
    
    # Make the request
    response = client.post(
        "/demands/",
        json={
            "floor": 3,
            "direction": "up",
            "elevator_id": 999  # Non-existent elevator ID
        }
    )
    
    # Assertions
    assert response.status_code == 404
    assert "Elevator not found" in response.json()["detail"]

def test_get_demands(mock_db, mock_get_db, sample_demands):
    """Test getting all demands."""
    # Setup mock
    mock_db.query.return_value.order_by.return_value.offset.return_value.limit.return_value.all.return_value = sample_demands
    
    # Make the request
    response = client.get("/demands/")
    
    # Assertions
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5  # We created 5 sample demands
    
    # Verify mock calls
    mock_db.query.assert_called()

def test_get_demands_with_floor_filter(mock_db, mock_get_db, sample_demands):
    """Test getting demands filtered by floor."""
    # Setup mock to return only demands for floor 1
    floor_1_demands = [d for d in sample_demands if d.floor == 1]
    mock_db.query.return_value.filter.return_value.order_by.return_value.offset.return_value.limit.return_value.all.return_value = floor_1_demands
    
    # Make the request
    response = client.get("/demands/?floor=1")
    
    # Assertions
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2  # We created 2 demands for floor 1
    assert all(item["floor"] == 1 for item in data)
    
    # Verify mock calls
    mock_db.query.assert_called()

def test_get_demands_with_direction_filter(mock_db, mock_get_db, sample_demands):
    """Test getting demands filtered by direction."""
    # Setup mock to return only demands with direction "up"
    up_demands = [d for d in sample_demands if d.direction == "up"]
    mock_db.query.return_value.filter.return_value.order_by.return_value.offset.return_value.limit.return_value.all.return_value = up_demands
    
    # Make the request
    response = client.get("/demands/?direction=up")
    
    # Assertions
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 4  # We created 4 demands with direction "up"
    assert all(item["direction"] == "up" for item in data)
    
    # Verify mock calls
    mock_db.query.assert_called()

def test_get_demands_with_date_filter(mock_db, mock_get_db, sample_demands):
    """Test getting demands filtered by date range."""
    # Setup mock to return only demands from the last day
    yesterday = datetime.now() - timedelta(days=1)
    recent_demands = [d for d in sample_demands if d.timestamp >= yesterday]
    mock_db.query.return_value.filter.return_value.order_by.return_value.offset.return_value.limit.return_value.all.return_value = recent_demands
    
    # Make the request
    yesterday_str = yesterday.isoformat()
    response = client.get(f"/demands/?start_date={yesterday_str}")
    
    # Assertions
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3  # We created 3 demands within the last day
    
    # Verify mock calls
    mock_db.query.assert_called()

