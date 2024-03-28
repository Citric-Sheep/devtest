import pytest
from flask import Flask
from controllers.demand_controllers import *


# Mocking Flask app to obtain the app context.
app = Flask(__name__)


@pytest.mark.order(5)
def test_create_demand_controller():
    data = {
        "custom_id": 1,
        "elevator_id": 1,
        "start_floor": 2,
        "end_floor": 3,
    }
    result, status_code = create_demand_controller(data)
    assert status_code == 201
    assert "Success" in result


@pytest.mark.order(11)
def test_get_demand_controller():
    # Assuming there are buildings in the database for testing
    with app.test_request_context():
        elevator_id = 1
        response = get_demand_controller(elevator_id)
    assert response.status_code == 200


@pytest.mark.order(17)
def test_update_demand_controller():
    # Mock input data
    data = {"id": 1, "new_values": {"start_floor": 5}}

    # Call the function
    result, status_code = update_demand_controller(data)

    # Assert that the result and status code are correct
    assert result == "Success"
    assert status_code == 200


@pytest.mark.order(23)
def test_delete_demand_controller():
    # Mock input data
    data = {"id": 1}

    # Call the function
    result, status_code = delete_demand_controller(data)

    # Assert that the result and status code are correct
    assert result == "Success"
    assert status_code == 200
