import pytest
from flask import Flask
from controllers.elevator_controllers import *

# Mocking Flask app to obtain the app context.
app = Flask(__name__)


@pytest.mark.order(3)
def test_create_elevator_controller():
    data = {
        "custom_id": 1,
        "building_id": 1,
        "max_floors": 5,
        "local_identifier": 3
    }
    result, status_code = create_elevator_controller(data)
    assert status_code == 201
    assert "Success" in result


@pytest.mark.order(9)
def test_get_elevators_controller():
    # Assuming there are elevators in the database for testing
    with app.test_request_context():
        elevator_id = 1
        response = get_elevators_controller(elevator_id)
    assert response.status_code == 200


@pytest.mark.order(15)
def test_update_elevator_controller():
    # Mock input data
    data = {"id": 1, "new_values": {"local_identifier": 2}}

    # Call the function
    result, status_code = update_elevator_controller(data)

    # Assert that the result and status code are correct
    assert result == "Success"
    assert status_code == 200


@pytest.mark.order(25)
def test_delete_elevator_controller():
    # Mock input data
    data = {"id": 1}

    # Call the function
    result, status_code = delete_elevator_controller(data)

    # Assert that the result and status code are correct
    assert result == "Success"
    assert status_code == 200
