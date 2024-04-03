from fastapi.testclient import TestClient
from elevator import app

client = TestClient(app)


def test_run_app():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "This is a dev test for elevator challenge"}


def test_go_to_floor():
    response = client.get("/8")
    assert response.status_code == 200
    assert response.json() == {"message": f"You went to floor #8."}


def test_repeated_go_to_floor():
    client.get("/8")
    response = client.get("/8")
    assert response.status_code == 422
    assert response.json() == {"message": "You're already on the 8 floor"}
