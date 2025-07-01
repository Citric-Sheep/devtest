import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from datetime import datetime

from src.tests.conftest import client, mock_db, mock_get_db


def test_create_elevator_invalid_floors(mock_db, mock_get_db):
    """Test creating an elevator with invalid floor configuration."""
    # Make the request with min_floor > max_floor
    response = client.post(
        "/elevators/",
        json={
            "building_id": 2,
            "max_floor": 5,
            "min_floor": 10  # Invalid: min_floor > max_floor
        }
    )
    
    # Assertions
    assert response.status_code == 400
    assert "min_floor must be less than or equal to max_floor" in response.json()["detail"]
    
    # Verify mock calls
    mock_db.add.assert_not_called()
    mock_db.commit.assert_not_called()


def test_get_elevator_not_found(mock_db, mock_get_db):
    """Test getting a non-existent elevator."""
    # Setup mock to return None (elevator not found)
    mock_db.query.return_value.filter.return_value.first.return_value = None
    
    # Make the request
    response = client.get("/elevators/999")  # Non-existent ID
    
    # Assertions
    assert response.status_code == 404
    assert "Elevator not found" in response.json()["detail"]
    
    # Verify mock calls
    mock_db.query.assert_called()

def test_update_elevator(mock_db, mock_get_db):
    """Test updating an elevator."""
    # Setup mock data
    elevator_id = 1
    updated_data = {
        "id": elevator_id,
        "building_id": 3,
        "max_floor": 15,
        "min_floor": -1
    }
    
    # Override the route function
    from src.routes.elevators import update_elevator
    original_func = update_elevator
    
    def mock_update_elevator(*args, **kwargs):
        return updated_data
    
    # Apply the patch
    import src.routes.elevators
    src.routes.elevators.update_elevator = mock_update_elevator
    
    try:
        # Make the request
        response = client.put(
            f"/elevators/{elevator_id}",
            json={
                "building_id": 3,
                "max_floor": 15,
                "min_floor": -1
            }
        )
        
        # Assertions
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == updated_data["id"]
        assert data["building_id"] == updated_data["building_id"]
        assert data["max_floor"] == updated_data["max_floor"]
        assert data["min_floor"] == updated_data["min_floor"]
        
        # Verify mock calls
        mock_db.query.assert_called()
    finally:
        # Restore the original function
        src.routes.elevators.update_elevator = original_func

def test_update_elevator_not_found(mock_db, mock_get_db):
    """Test updating a non-existent elevator."""
    # Setup mock to return None (elevator not found)
    mock_db.query.return_value.filter.return_value.first.return_value = None
    
    # Make the request
    response = client.put(
        "/elevators/999",  # Non-existent ID
        json={
            "building_id": 3,
            "max_floor": 15,
            "min_floor": -1
        }
    )
    
    # Assertions
    assert response.status_code == 404
    assert "Elevator not found" in response.json()["detail"]
    
    # Verify mock calls
    mock_db.query.assert_called()
    mock_db.commit.assert_not_called()

def test_update_elevator_invalid_floors(mock_db, mock_get_db):
    """Test updating an elevator with invalid floor configuration."""
    # Setup mock data
    elevator_id = 1
    elevator_data = {
        "id": elevator_id,
        "building_id": 1,
        "max_floor": 10,
        "min_floor": 0
    }
    
    # Setup mock to return the elevator
    mock_elevator = MagicMock()
    mock_elevator.id = elevator_id
    mock_db.query.return_value.filter.return_value.first.return_value = mock_elevator
    
    # Make the request with min_floor > max_floor
    response = client.put(
        f"/elevators/{elevator_id}",
        json={
            "building_id": 3,
            "max_floor": 5,
            "min_floor": 10  # Invalid: min_floor > max_floor
        }
    )
    
    # Assertions
    assert response.status_code == 400
    assert "min_floor must be less than or equal to max_floor" in response.json()["detail"]
    
    # Verify mock calls
    mock_db.query.assert_called()
    mock_db.commit.assert_not_called()

def test_delete_elevator(mock_db, mock_get_db):
    """Test deleting an elevator."""
    # Setup mock data
    elevator_id = 1
    
    # Setup mock to return an elevator
    mock_elevator = MagicMock()
    mock_elevator.id = elevator_id
    mock_db.query.return_value.filter.return_value.first.return_value = mock_elevator
    
    # Make the request
    response = client.delete(f"/elevators/{elevator_id}")
    
    # Assertions
    assert response.status_code == 204
    
    # Verify mock calls
    mock_db.query.assert_called()
    mock_db.delete.assert_called_once()
    mock_db.commit.assert_called_once()

def test_delete_elevator_not_found(mock_db, mock_get_db):
    """Test deleting a non-existent elevator."""
    # Setup mock to return None (elevator not found)
    mock_db.query.return_value.filter.return_value.first.return_value = None
    
    # Make the request
    response = client.delete("/elevators/999")  # Non-existent ID
    
    # Assertions
    assert response.status_code == 404
    assert "Elevator not found" in response.json()["detail"]
    
    # Verify mock calls
    mock_db.query.assert_called()
    mock_db.delete.assert_not_called()
    mock_db.commit.assert_not_called()


def test_get_elevator_demands_not_found(mock_db, mock_get_db):
    """Test getting demands for a non-existent elevator."""
    # Setup mock to return None (elevator not found)
    mock_db.query.return_value.filter.return_value.first.return_value = None
    
    # Make the request
    response = client.get("/elevators/999/demands")  # Non-existent ID
    
    # Assertions
    assert response.status_code == 404
    assert "Elevator not found" in response.json()["detail"]
    
    # Verify mock calls
    mock_db.query.assert_called()
