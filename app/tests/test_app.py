import os
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine
import uuid


@pytest.fixture(autouse=True, scope="function")
def clean_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield


def create_elevator(client, name=None):
    if name is None:
        import uuid
        name = f"TestElevator_{uuid.uuid4()}"
    resp = client.post("/elevators/", json={"name": name})
    assert resp.status_code == 200
    return resp.json()["id"]

def test_create_demand():
    client = TestClient(app)
    eid = create_elevator(client)
    payload = {
        "elevator_id": eid,
        "floor": 3,
        "timestamp": "2024-06-27T09:00:00",
        "direction": "up"
    }
    resp = client.post("/demand/", json=payload)
    assert resp.status_code == 200
    assert resp.json()["floor"] == 3
    
def test_create_resting():
    client = TestClient(app)
    eid = create_elevator(client)
    payload = {
        "elevator_id": eid,
        "floor": 2,
        "start_time": "2024-06-27T08:00:00"
    }
    resp = client.post("/resting/", json=payload)
    assert resp.status_code == 200
    assert resp.json()["floor"] == 2
    
def test_idle_relocation():
    client = TestClient(app)
    eid = create_elevator(client)
    resp = client.post("/resting/", json={
        "elevator_id": eid,
        "floor": 2,
        "start_time": "2024-06-27T08:00:00" 
    }).json()
    rid = resp["id"]
    end_resp = client.patch(f"/resting/{rid}/end", json={"end_time": "2024-06-27T08:12:00"}).json()
    assert end_resp["relocation_flag"] is True
    
def test_peak_hours_non_optimal():
    client = TestClient(app)
    eid = create_elevator(client)
    resp = client.post("/resting/", json={
        "elevator_id": eid,
        "floor": 4,
        "start_time": "2024-06-27T08:15:00"  
    }).json()
    assert resp ["non_optimal_rested"] is True
    
def test_demand_surge():
    client = TestClient(app)
    eid = create_elevator(client)
    for minute in [0, 1]:
        client.post("/demand/", json={
        "elevator_id": eid,
        "floor": 6,
        "timestamp": f"2024-06-27T09:0{minute}:00",
        "direction": "up" 
        })
    resp = client.post("/demand/", json={
        "elevator_id": eid,
        "floor": 6,
        "timestamp": "2024-06-27T09:02:00",
        "direction": "up"   
    }).json()
    assert resp["surge_tag"] is True
    
def test_export():
    client = TestClient(app)
    resp = client.get("/export/")
    assert resp.status_code == 200
    assert "demands" in resp.json()