import pytest
from fastapi.testclient import TestClient
from main import app, Base, engine, SessionLocal

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_and_teardown():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_create_elevator():
    response = client.post("/elevator/", json={"current_floor": 0})
    assert response.status_code == 200
    assert "id" in response.json()

def test_update_elevator_status():
    elevator = client.post("/elevator/", json={"current_floor": 0}).json()
    elevator_id = elevator["id"]
    payload = {
        "current_floor": 3,
        "is_moving": True,
        "is_occupied": False
    }
    response = client.patch(f"/elevator/{elevator_id}/status", json=payload)
    assert response.status_code == 200
    assert response.json()["status"] == "updated"

def test_create_demand():
    client.post("/elevator/", json={"current_floor": 0})  # Cria elevador 1
    response = client.post("/demand/", json={"floor_called_from": 5})
    assert response.status_code == 200
    assert response.json()["status"] == "demand recorded"

def test_events_logged():
    client.post("/elevator/", json={"current_floor": 0})
    client.post("/demand/", json={"floor_called_from": 2})
    client.patch("/elevator/1/status", json={
        "current_floor": 5,
        "is_moving": True,
        "is_occupied": False
    })
    response = client.get("/events/")
    assert response.status_code == 200
    events = response.json()
    assert any(e["event_type"] == "CALL" for e in events)
    assert any(e["event_type"] == "MOVE" for e in events)
