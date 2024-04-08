"""Tests for app module"""

from typing import Optional

import pytest
from fastapi.testclient import TestClient

from app import app
from app.constants import WELCOME_MESSAGE
from app.schemas import ElevatorDemandOutput

ORIGIN: str = "origin"
DESTINATION: str = "destination"
API_ENDPOINT: str = "/demand"
NOT_FOUND: str = "Not Found"

SAMPLE_CASES = (
    # Good request
    ({ORIGIN: 0, DESTINATION: 1}, 201),
    ({ORIGIN: 2, DESTINATION: 5}, 201),
    ({DESTINATION: 7, ORIGIN: 3}, 201),
    ({DESTINATION: 9, ORIGIN: 4}, 201),
    # Bad request: some business rule does not apply
    ({ORIGIN: 0, DESTINATION: 0}, 400),
    ({ORIGIN: 2, DESTINATION: 2}, 400),
    ({ORIGIN: 8, DESTINATION: 8}, 400),
    # Unprocessable request: some input data is wrong
    ({ORIGIN: 7, DESTINATION: None}, 422),
    ({ORIGIN: "foo", DESTINATION: 1}, 422),
    ({"name": 123, ORIGIN: 1}, 422),
    ({ORIGIN: 1}, 422),
    (None, 422),
    ({}, 422),
)


@pytest.mark.parametrize(
    ("endpoint", "status_code", "message"),
    (
        ("/", 200, WELCOME_MESSAGE),
        (API_ENDPOINT, 200, ""),
        ("/admin", 404, NOT_FOUND),
        ("/index", 404, NOT_FOUND),
    ),
)
def test_other_endpoints(endpoint: str, status_code: int, message: str) -> None:
    """
    Test request to other endpoints.
    :parameter endpoint: Endpoint to send request.
    :parameter status_code: Expected status code.
    :return: None
    """
    client = TestClient(app)
    response = client.get(endpoint)
    assert response.status_code == status_code
    if "detail" in response.json():
        assert message in response.json()["detail"]
    if "message" in response.json():
        assert message in response.json()["message"]


@pytest.mark.parametrize(
    ("input_", "status_code"),
    SAMPLE_CASES,
)
def test_get_requests(input_: Optional[dict], status_code: int) -> None:
    """
    Test GET requests.
    :parameter input_: Input data.
    :parameter status_code: Expected status code.
    :return: None
    """
    client = TestClient(app)
    demand = client.post(url=API_ENDPOINT, json=input_)
    assert demand.status_code == status_code
    if demand.status_code == 201:
        response = client.get(
            url=f"{API_ENDPOINT}/{ElevatorDemandOutput(**demand.json()).id}"
        )
        assert response.status_code == 200


@pytest.mark.parametrize(
    ("input_", "status_code"),
    SAMPLE_CASES,
)
def test_app_post(input_: Optional[dict], status_code: int) -> None:
    """
    Test POST requests.
    :parameter input_: Input data.
    :parameter status_code: Expected status code.
    :return: None
    """
    client = TestClient(app)
    response = client.post(url=API_ENDPOINT, json=input_)
    assert response.status_code == status_code
    if status_code == 201:
        output = ElevatorDemandOutput(**response.json())
        assert isinstance(output, ElevatorDemandOutput)
        assert output.origin == input_[ORIGIN]
        assert output.destination == input_[DESTINATION]


@pytest.mark.parametrize(
    ("input_", "status_code"),
    SAMPLE_CASES,
)
def test_put_requests(input_: Optional[dict], status_code: int) -> None:
    """
    Test PUT requests.
    :parameter input_: Input data.
    :parameter status_code: Expected status code.
    :return: None
    """
    client = TestClient(app)
    demand = client.post(url=API_ENDPOINT, json=input_)
    assert demand.status_code == status_code
    if demand.status_code == 201:
        new_data = {ORIGIN: 0, DESTINATION: 9}
        response = client.put(
            url=f"{API_ENDPOINT}/{ElevatorDemandOutput(**demand.json()).id}",
            json=new_data,
        )
        assert response.status_code == 200
        output = ElevatorDemandOutput(**response.json())
        assert output.origin == new_data[ORIGIN]
        assert output.destination == new_data[DESTINATION]


@pytest.mark.parametrize(
    ("input_", "status_code"),
    SAMPLE_CASES,
)
def test_delete_requests(input_: Optional[dict], status_code: int) -> None:
    """
    Test DELETE requests.
    :parameter input_: Input data.
    :parameter status_code: Expected status code.
    :return: None
    """
    client = TestClient(app)
    demand = client.post(url=API_ENDPOINT, json=input_)
    assert demand.status_code == status_code
    if demand.status_code == 201:
        response = client.delete(
            url=f"{API_ENDPOINT}/{ElevatorDemandOutput(**demand.json()).id}"
        )
        assert response.status_code == 204
