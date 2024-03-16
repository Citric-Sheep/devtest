import sys
sys.path.append('../app')
import pytest
from main import app, db
from models import Demand, ElevatorMovement
from process import preprocessing
from flask import jsonify

@pytest.fixture
def client():
    """Fixture to provide a test client."""
    with app.app_context():
        with app.test_client() as client:
            yield client

def test_preprocessing_route(client):
    """Test preprocessing route with different min_stops values."""
    with app.app_context():
        # Insert some test data into the database
        # This step may vary depending on your specific test environment

        # Simulate a GET request with min_stops = 1
        response = client.get("/predictor/preprocessing?min_stops=1")

        # Check that the response has the expected status code
        assert response.status_code == 200

        # Check that the response contains JSON data
        assert response.is_json

        # Check that the response data is correct (you may need to adjust this based on your preprocessing function)
        expected_data = preprocessing(1)
        assert response.json == jsonify([vars(item) for item in expected_data]).json

        # Simulate a GET request with min_stops = 2
        response = client.get("/predictor/preprocessing?min_stops=2")

        # Check that the response has the expected status code
        assert response.status_code == 200

        # Check that the response contains JSON data
        assert response.is_json

        # Check that the response data is correct (you may need to adjust this based on your preprocessing function)
        expected_data = preprocessing(2)
        assert response.json == jsonify([vars(item) for item in expected_data]).json
