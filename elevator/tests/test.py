import pytest
from app import app
import json

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_log_demand(client):
    # Prepare the data for the POST request
    data = {
        "demand_floor": 5,
        "direction": 1  # Going up
    }

    # Send POST request to log a demand
    response = client.post("/log_demand", json=data)

    # Assert the response status code and message
    assert response.status_code == 201
    assert response.json["message"] == "Demand logged successfully"

def test_get_feature_data(client):
    # Send GET request to fetch feature data
    response = client.get("/get_feature_data")

    # Assert the response status code and the presence of data
    assert response.status_code == 200
    assert "data" in response.json
    assert isinstance(response.json["data"], list)  # Ensure data is a list
