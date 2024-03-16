import sys
sys.path.append('../app')
import json
import pytest
from main import app, db
from models import ElevatorMovement

@pytest.fixture
def client():
    """Fixture to provide a test client."""
    with app.app_context():
        with app.test_client() as client:
            yield client

def test_create_elevator_movement(client):
    """Test for creating a new elevator movement."""
    with app.app_context():
        # Simulate a POST request to create a new elevator movement
        response = client.post("/elevator_movement", json={
            "elevator_id": 1,
            "current_floor": 2,
            "next_floor": 3,
            "action": "move_up",
            "floor_requested": 4,
            "expected_arrival_time": "2024-03-15T12:00:00"
        })

        # Check that the response has the expected status code
        assert response.status_code == 201

        # Check that the message in the response is correct
        assert response.json["message"] == "Elevator movement created successfully"

        # Check that the elevator movement has been created correctly in the database
        assert ElevatorMovement.query.filter_by(elevator_id=1).first() is not None

def test_get_all_elevator_movements(client):
    """Test for getting all elevator movements."""
    with app.app_context():
        # Simulate a GET request to retrieve all elevator movements
        response = client.get("/elevator_movements")

        # Check that the response has the expected status code
        assert response.status_code == 200

        # Check that the response contains the elevator movements data (if applicable)
        assert len(response.json) > 0

def test_get_elevator_movement(client):
    """Test for getting an elevator movement by its ID."""
    with app.app_context():
        # Insert a test elevator movement into the database
        movement = ElevatorMovement(elevator_id=1, current_floor=2, next_floor=3, action="move_up", floor_requested=4, expected_arrival_time="2024-03-15T12:00:00")
        db.session.add(movement)
        db.session.commit()

        # Simulate a GET request to retrieve the elevator movement by its ID
        response = client.get(f"/elevator_movement/{movement.id}")

        # Check that the response has the expected status code
        assert response.status_code == 200

        # Check that the response contains the elevator movement data (if applicable)
        assert response.json["elevator_id"] == 1

def test_update_elevator_movement(client):
    """Test for updating an elevator movement by its ID."""
    with app.app_context():
        # Insert a test elevator movement into the database
        movement = ElevatorMovement(elevator_id=1, current_floor=2, next_floor=3, action="move_up", floor_requested=4, expected_arrival_time="2024-03-15T12:00:00")
        db.session.add(movement)
        db.session.commit()

        # Simulate a PUT request to update the elevator movement by its ID
        response = client.put(f"/elevator_movement/{movement.id}", json={"current_floor": 3})

        # Check that the response has the expected status code
        assert response.status_code == 200

        # Check that the elevator movement has been updated correctly in the database
        updated_movement = db.session.get(ElevatorMovement, movement.id)
        assert updated_movement.current_floor == 3

def test_delete_elevator_movement(client):
    """Test for deleting an elevator movement by its ID."""
    with app.app_context():
        # Insert a test elevator movement into the database
        movement = ElevatorMovement(elevator_id=1, current_floor=2, next_floor=3, action="move_up", floor_requested=4, expected_arrival_time="2024-03-15T12:00:00")
        db.session.add(movement)
        db.session.commit()

        # Simulate a DELETE request to delete the elevator movement by its ID
        response = client.delete(f"/elevator_movement/{movement.id}")

        # Check that the response has the expected status code
        assert response.status_code == 200

        # Check that the elevator movement has been deleted correctly from the database
        assert db.session.get(ElevatorMovement, movement.id) is None
