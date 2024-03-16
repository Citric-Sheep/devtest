import sys
sys.path.append('../app')
import json
import pytest
from main import app, db
from models import Demand

@pytest.fixture
def client():
    """Fixture to provide a test client."""
    with app.app_context():
        with app.test_client() as client:
            yield client

def test_create_demand(client):
    """Test for the demand creation route."""
    with app.app_context():  # Establish Flask application context
        # Simulate a POST request to create a demand
        response = client.post("/demand", json={"floor": 5})

        # Check that the response has the expected status code
        assert response.status_code == 201

        # Check that the message in the response is correct
        assert response.json["message"] == "Demand created successfully"

        # Check that the demand has been created correctly in the database
        assert Demand.query.filter_by(floor=5).first() is not None

def test_get_all_demands(client):
    """Test for the route that gets all demands."""
    with app.app_context():  # Establish Flask application context
        # Simulate a GET request to retrieve all demands
        response = client.get("/demands")

        # Check that the response has the expected status code
        assert response.status_code == 200

        # Check that the response contains the demands data (if applicable)
        assert len(response.json) > 0

def test_get_demand(client):
    """Test for the route that gets a demand by its ID."""
    with app.app_context():  # Establish Flask application context
        # Insert a test demand into the database
        demand = Demand(floor=1)
        db.session.add(demand)
        db.session.commit()

        # Simulate a GET request to retrieve the demand by its ID
        response = client.get(f"/demand/{demand.id}")

        # Check that the response has the expected status code
        assert response.status_code == 200

        # Check that the response contains the demand data (if applicable)
        assert response.json["floor"] == 1

def test_update_demand(client):
    """Test for the route that updates a demand by its ID."""
    with app.app_context():  # Establish Flask application context
        # Insert a test demand into the database
        demand = Demand(floor=3)
        db.session.add(demand)
        db.session.commit()

        # Simulate a PUT request to update the demand by its ID
        response = client.put(f"/demand/{demand.id}", json={"floor": 7})

        # Check that the response has the expected status code
        assert response.status_code == 200

        # Check that the demand has been updated correctly in the database
        updated_demand = db.session.get(Demand, demand.id)
        assert updated_demand.floor == 7

def test_delete_demand(client):
    """Test for the route that deletes a demand by its ID."""
    with app.app_context():  # Establish Flask application context
        # Insert a test demand into the database
        demand = Demand(floor=3)
        db.session.add(demand)
        db.session.commit()

        # Simulate a DELETE request to delete the demand by its ID
        response = client.delete(f"/demand/{demand.id}")

        # Check that the response has the expected status code
        assert response.status_code == 200

        # Check that the demand has been deleted correctly from the database
        assert db.session.get(Demand, demand.id) is None
