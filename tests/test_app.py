"""Tests for app module"""

import pytest
from fastapi.testclient import TestClient

from app import app
from app.constants import WELCOME_MESSAGE


def test_get_request_to_root() -> None:
    """
    Test GET request to root endpoint.
    :return: None
    """
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": WELCOME_MESSAGE}
