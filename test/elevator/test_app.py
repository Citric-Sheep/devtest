from http import HTTPStatus

from fastapi.testclient import TestClient


def test_api_interaction(test_client: TestClient):
    # Add elevator
    response = test_client.post("/elevators/", json={"name": "elevator1"})
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data["name"] == "elevator1"
    created_elevator_id = data["id"]
    # Add elevator demands
    for pressed_at_floor in (1, 2, 1, 3, 1):
        response = test_client.post(
            "/elevator-requests/",
            json={
                "elevator_id": created_elevator_id,
                "pressed_at_floor": pressed_at_floor,
            },
        )
        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert data["elevator_id"] == created_elevator_id
        assert data["pressed_at_floor"] == pressed_at_floor
    # Most frequent floor around current time should be 1
    response = test_client.get("/top-floor-demand/by-time").json()
    assert response["most_demanded_floor"] == 1
