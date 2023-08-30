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


def test_elevator_demand_2(client):
    demand_data_1 = {
        "elevator_id": 1,
        "demand_category": 1,
        "current_floor": 1,
        "destination_floor": 8,
        "current_movement": 3,
        "demand_type": 2
    }

    demand_data_2 = {
        "elevator_id": 1,
        "demand_category": 1,
        "current_floor": 2,
        "destination_floor": 5,
        "current_movement": 1,
        "demand_type": 2
    }

    response_1 = client.post("/elevator/demand",
                             json=demand_data_1)
    response_2 = client.post("/elevator/demand",
                             json=demand_data_2)

    assert response_1.status_code == 200
    assert response_2.status_code == 200

    content_1 = response_1.json()
    content_2 = response_2.json()

    assert content_1["target_floor"] == 8
    assert content_2["target_floor"] == 8
    assert isinstance(content_1["request_id"], int)
    assert isinstance(content_2["request_id"], int)


def test_elevator_update_1(client):
    demand_data = {
        "elevator_id": 1,
        "demand_category": 1,
        "current_floor": 1,
        "destination_floor": 10,
        "current_movement": 3,
        "demand_type": 2
    }
    update_data = {
        "elevator_id": 1,
        "current_floor": 10,
        "current_movement": 1,
        "request_id": 4
    }

    response_1 = client.post("/elevator/demand",
                             json=demand_data)
    response_2 = client.put("/elevator/demand",
                            json=update_data)

    assert response_1.status_code == 200
    assert response_2.status_code == 200

    content_1 = response_1.json()
    content_2 = response_2.json()

    assert content_1["target_floor"] == 10
    assert content_2["target_floor"] == 10
    assert isinstance(content_1["request_id"], int)
    assert content_2["request_id"] is None


def test_elevator_update_2(client):
    demand_data_1 = {
        "elevator_id": 1,
        "demand_category": 1,
        "current_floor": 1,
        "destination_floor": 8,
        "current_movement": 3,
        "demand_type": 2
    }

    demand_data_2 = {
        "elevator_id": 1,
        "demand_category": 1,
        "current_floor": 2,
        "destination_floor": 5,
        "current_movement": 1,
        "demand_type": 2
    }
    update_data_1 = {
        "elevator_id": 1,
        "current_floor": 8,
        "current_movement": 1,
        "request_id": 5
    }
    update_data_2 = {
        "elevator_id": 1,
        "current_floor": 5,
        "current_movement": 1,
        "request_id": 6
    }

    response_1 = client.post("/elevator/demand",
                             json=demand_data_1)
    response_2 = client.post("/elevator/demand",
                             json=demand_data_2)
    response_3 = client.put("/elevator/demand",
                            json=update_data_1)
    response_4 = client.put("/elevator/demand",
                            json=update_data_2)

    assert response_1.status_code == 200
    assert response_2.status_code == 200
    assert response_3.status_code == 200
    assert response_4.status_code == 200

    content_1 = response_1.json()
    content_2 = response_2.json()
    content_3 = response_3.json()
    content_4 = response_4.json()

    assert content_1["target_floor"] == 8
    assert content_2["target_floor"] == 8
    assert content_3["target_floor"] == 5
    assert content_4["target_floor"] == 5
    assert isinstance(content_1["request_id"], int)
    assert isinstance(content_2["request_id"], int)
    assert isinstance(content_3["request_id"], int)
    assert content_4["request_id"] is None


def test_full_ride(client):
    order_1 = {
        "elevator_id": 1,
        "demand_category": 1,
        "current_floor": 1,
        "destination_floor": 8,
        "current_movement": 3,
        "demand_type": 2
    }
    response_1 = client.post("/elevator/demand",
                             json=order_1)
    content_1 = response_1.json()
    assert content_1["target_floor"] == order_1["destination_floor"]

    order_2 = {
        "elevator_id": 1,
        "demand_category": 1,
        "current_floor": 2,
        "destination_floor": 5,
        "current_movement": 1,
        "demand_type": 2
    }
    response_2 = client.post("/elevator/demand",
                             json=order_2)
    content_2 = response_2.json()
    assert content_2["target_floor"] == content_1["target_floor"]

    order_3 = {
        "elevator_id": 1,
        "demand_category": 1,
        "current_floor": 3,
        "destination_floor": 4,
        "current_movement": 1,
        "demand_type": 2
    }
    response_3 = client.post("/elevator/demand",
                             json=order_3)
    content_3 = response_3.json()
    assert content_3["target_floor"] == content_1["target_floor"]

    order_4 = {
        "elevator_id": 1,
        "demand_category": 1,
        "current_floor": 4,
        "destination_floor": 5,
        "current_movement": 1,
        "demand_type": 1
    }
    response_4 = client.post("/elevator/demand",
                             json=order_4)
    content_4 = response_4.json()
    assert content_4["target_floor"] == order_4["destination_floor"]

    order_5 = {
        "elevator_id": 1,
        "current_floor": 5,
        "current_movement": 1,
        "request_id": 10
    }
    response_5 = client.put("/elevator/demand",
                            json=order_5)
    content_5 = response_5.json()
    assert content_5["target_floor"] == content_1["target_floor"]

    order_6 = {
        "elevator_id": 1,
        "demand_category": 2,
        "current_floor": 5,
        "destination_floor": 10,
        "current_movement": 1,
        "demand_type": None
    }
    response_6 = client.post("/elevator/demand",
                             json=order_6)
    content_6 = response_6.json()
    assert content_6["target_floor"] == order_6["destination_floor"]

    order_7 = {
        "elevator_id": 1,
        "current_floor": 10,
        "current_movement": 1,
        "request_id": None
    }
    response_7 = client.put("/elevator/demand",
                            json=order_7)
    content_7 = response_7.json()
    assert content_7["target_floor"] == content_1["target_floor"]

    order_8 = {
        "elevator_id": 1,
        "current_floor": 8,
        "current_movement": 2,
        "request_id": 7
    }
    response_8 = client.put("/elevator/demand",
                            json=order_8)
    content_8 = response_8.json()
    assert content_8["target_floor"] == order_2["destination_floor"]

    order_9 = {
        "elevator_id": 1,
        "demand_category": 2,
        "current_floor": 8,
        "destination_floor": 1,
        "current_movement": 2,
        "demand_type": None
    }
    response_9 = client.post("/elevator/demand",
                             json=order_9)
    content_9 = response_9.json()
    assert content_9["target_floor"] == content_8["target_floor"]

    order_10 = {
        "elevator_id": 1,
        "current_floor": 5,
        "current_movement": 2,
        "request_id": 8
    }
    response_10 = client.put("/elevator/demand",
                             json=order_10)
    content_10 = response_10.json()
    assert content_10["target_floor"] == order_3["destination_floor"]

    order_11 = {
        "elevator_id": 1,
        "demand_category": 2,
        "current_floor": 5,
        "destination_floor": 2,
        "current_movement": 2,
        "demand_type": None
    }
    response_11 = client.post("/elevator/demand",
                              json=order_11)
    content_11 = response_11.json()
    assert content_11["target_floor"] == content_10["target_floor"]

    order_12 = {
        "elevator_id": 1,
        "current_floor": 4,
        "current_movement": 2,
        "request_id": 9
    }
    response_12 = client.put("/elevator/demand",
                             json=order_12)
    content_12 = response_12.json()
    assert content_12["target_floor"] == order_11["destination_floor"]

    order_13 = {
        "elevator_id": 1,
        "demand_category": 2,
        "current_floor": 4,
        "destination_floor": 1,
        "current_movement": 2,
        "demand_type": None
    }
    response_13 = client.post("/elevator/demand",
                              json=order_13)
    content_13 = response_13.json()
    assert content_13["target_floor"] == content_12["target_floor"]

    order_14 = {
        "elevator_id": 1,
        "current_floor": 2,
        "current_movement": 2,
        "request_id": None
    }
    response_14 = client.put("/elevator/demand",
                             json=order_14)
    content_14 = response_14.json()
    assert content_14["target_floor"] == order_9["destination_floor"]

    order_15 = {
        "elevator_id": 1,
        "current_floor": 1,
        "current_movement": 2,
        "request_id": None
    }
    response_15 = client.put("/elevator/demand",
                             json=order_15)
    content_15 = response_15.json()
    assert content_15["target_floor"] == order_15["current_floor"]
