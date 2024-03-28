import pytest
from flask import Flask
from controllers.building_controllers import *


# Mocking Flask app to obtain the app context.
app = Flask(__name__)


@pytest.mark.order(1)
def test_create_building_controller():
    data = {
        "custom_id": 1,
        "name": "Test Building",
        "address": "123 Main St",
        "city": "Test City",
        "country": "Test Country"
    }
    result, status_code = create_building_controller(data)
    assert status_code == 201
    assert "Success" in result


@pytest.mark.order(7)
def test_get_buildings_controller():
    # Assuming there are buildings in the database for testing
    with app.test_request_context():
        building_data = {"name": "Test Building"}
        response = get_buildings_controller(building_data)
    assert response.status_code == 200


@pytest.mark.order(13)
def test_update_building_controller():
    # Mock input data
    data = {"id": 1, "new_values": {"name": "Updated Building Name"}}

    # Call the function
    result, status_code = update_building_controller(data)

    # Assert that the result and status code are correct
    assert result == "Success"
    assert status_code == 200


@pytest.mark.order(27)
def test_delete_building_controller():
    # Mock input data
    data = {"id": 1}

    # Call the function
    result, status_code = delete_building_controller(data)

    # Assert that the result and status code are correct
    assert result == "Success"
    assert status_code == 200
