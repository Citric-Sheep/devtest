import pytest
from barbara_solution.main import (
    Elevator,
    ElevatorRequest,
    ScheduledJob,
)


@pytest.fixture
def setup_elevator(client):
    """Creates an operational elevator for test usage."""
    payload = {
        "name": "Elevator A",
        "capacity": 10,
        "is_operational": True,
        "current_floor": 1,
    }
    resp = client.post("/elevators", json=payload)
    print(resp, type(resp))
    return resp.get_json()["elevator_id"]


def test_create_elevator(client):
    payload = {
        "name": "Elevator B",
        "capacity": 8,
        "is_operational": True,
        "current_floor": 5,
    }
    response = client.post("/elevators", json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert "elevator_id" in data
    elevator_id = data["elevator_id"]

    # Confirm in the database
    elevator = Elevator.query.get(elevator_id)
    assert elevator is not None
    assert elevator.name == "Elevator B"


def test_create_request(client, setup_elevator):
    elevator_id = setup_elevator
    request_payload = {
        "floor": 10,
        "direction": "up",
        "request_type": "external",
        "elevator_id": elevator_id,
    }
    resp = client.post("/requests", json=request_payload)
    assert resp.status_code == 201
    data = resp.get_json()
    assert "request_id" in data

    # DB check
    req_db = ElevatorRequest.query.get(data["request_id"])
    assert req_db is not None
    assert req_db.floor == 10
    assert req_db.direction == "up"


def test_create_job_happy_path(client, setup_elevator):
    elevator_id = setup_elevator
    # Create a request first
    req_payload = {
        "floor": 2,
        "direction": "down",
        "request_type": "external",
        "elevator_id": elevator_id,
    }
    req_resp = client.post("/requests", json=req_payload)
    req_data = req_resp.get_json()
    request_id = req_data["request_id"]

    job_payload = {
        "elevator_id": elevator_id,
        "scheduled_time": "2025-02-01T10:00:00",
        "floor_arrival": 2,
        "floor_destination": 1,
        "requests": [request_id],
    }
    job_resp = client.post("/jobs", json=job_payload)
    assert job_resp.status_code == 201
    job_data = job_resp.get_json()
    assert "job_id" in job_data

    # DB check
    job_db = ScheduledJob.query.get(job_data["job_id"])
    assert job_db is not None
    assert job_db.floor_arrival == 2
    assert job_db.floor_destination == 1


def test_create_job_elevator_not_operational(client):
    # Create a non-operational elevator
    payload = {
        "name": "Broken Elevator",
        "capacity": 8,
        "is_operational": False,
    }
    resp = client.post("/elevators", json=payload)
    elevator_id = resp.get_json()["elevator_id"]

    # Attempt to create a job on a non-operational elevator
    job_payload = {
        "elevator_id": elevator_id,
        "scheduled_time": "2025-03-01T09:00:00",
        "floor_arrival": 5,
        "floor_destination": 10,
    }
    job_resp = client.post("/jobs", json=job_payload)
    assert job_resp.status_code == 400
    data = job_resp.get_json()
    assert "error" in data
    assert data["error"] == "Elevator is not operational"


def test_create_job_invalid_sequence(client, setup_elevator):
    elevator_id = setup_elevator
    # Create a "previous job" with a scheduled time in the future
    prev_job_payload = {
        "elevator_id": elevator_id,
        "scheduled_time": "2025-05-01T10:00:00",
        "floor_arrival": 1,
        "floor_destination": 8,
    }
    prev_resp = client.post("/jobs", json=prev_job_payload)
    prev_job_id = prev_resp.get_json()["job_id"]

    # Attempt to create a new job with a scheduled_time
    # earlier than the previous job
    new_job_payload = {
        "elevator_id": elevator_id,
        "scheduled_time": "2025-04-30T09:00:00",
        "floor_arrival": 8,
        "floor_destination": 1,
        "previous_job_id": prev_job_id,
    }
    resp = client.post("/jobs", json=new_job_payload)
    assert resp.status_code == 400
    data = resp.get_json()
    assert "error" in data
    assert data["error"] == "Invalid scheduling time by previous job"
