"""Tests for app module"""

from typing import Optional

import pytest
from fastapi.testclient import TestClient

from app import app
from app.constants import WELCOME_MESSAGE
from app.schemas import ElevatorDemandOutput


def test_get_request_to_root() -> None:
    """
    Test GET request to root endpoint.
    :return: None
    """
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": WELCOME_MESSAGE}


@pytest.mark.parametrize(
    ("input_", "status_code"),
    (
        # Good request
        ({"origin": 0, "destination": 1}, 201),
        ({"origin": 2, "destination": 5}, 201),
        # Bad request
        ({"origin": 0, "destination": 0}, 400),
        ({"origin": 2, "destination": 2}, 400),
    ),
)
def test_get_requests(input_: Optional[dict], status_code: int) -> None:
    """Test GET requests"""
    client = TestClient(app)
    demand = client.post("/demand/", json=input_)
    assert demand.status_code == status_code
    if demand.status_code == 201:
        response = client.get(f"/demand/{ElevatorDemandOutput(**demand.json()).id}")
        assert response.status_code == 200


@pytest.mark.parametrize(
    ("input_", "status_code"),
    (
        # Good request
        ({"origin": 0, "destination": 1}, 201),
        ({"origin": 2, "destination": 5}, 201),
        ({"destination": 7, "origin": 3}, 201),
        # Bad request
        ({"origin": 0, "destination": 0}, 400),
        ({"origin": 2, "destination": 2}, 400),
        ({"origin": 8, "destination": 8}, 400),
        # Unprocessable Entity
        ({"origin": 7, "destination": None}, 422),
        ({"origin": "foo", "destination": 1}, 422),
        ({"name": 1, "origin": 1}, 422),
        ({}, 422),
        (None, 422),
    ),
)
def test_app_post(input_: Optional[dict], status_code: int) -> None:
    """
    Test POST requests.
    :param input_: Demand Input (ElevatorDemandInput).
    :param status_code: HTTP Status Code (int).
    :return: None
    """
    client = TestClient(app)
    response = client.post("/demand/", json=input_)
    assert response.status_code == status_code
    if status_code == 201:
        output = ElevatorDemandOutput(**response.json())
        assert isinstance(output, ElevatorDemandOutput)
        assert output.origin == input_["origin"]
        assert output.destination == input_["destination"]
