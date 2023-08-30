###############
# Test cases #
###############

def test_elevator_demand_1(client):
    demand_data = {
        "elevator_id": 1,
        "demand_category": 1,
        "current_floor": 1,
        "destination_floor": 10,
        "current_movement": 3,
        "demand_type": 2
    }

    response = client.post("/elevator/demand",
                           json=demand_data)
    assert response.status_code == 200

    content = response.json()
    assert content["target_floor"] == 10
    assert isinstance(content["request_id"], int)
