import json
from time import sleep

DIRECTION_UP = 1
DIRECTION_DOWN = -1
BAD_REQUEST_STATUS_CODE = 400
CREATED_STATUS_CODE = 201


class TestElevatorBehavior:

    def test_create_an_elevator(self, client):
        # Define test variables
        elevator_top_floor = -8
        elevator_lower_floor = 10

        response = client.post(f"/api/elevators", data={
            "top_floor": elevator_lower_floor,
            "lower_floor": elevator_top_floor,
        })

        assert response.status_code == CREATED_STATUS_CODE

    def test_up_call_elevator(self, client):
        # Define test variables
        call_floor = 5
        direction = DIRECTION_UP

        response = client.post(f"/api/elevators/call", data={
            "call_floor": call_floor,
            "direction": direction,
        })

        assert response.status_code == CREATED_STATUS_CODE

    def test_move_up_to_floor_in_wrong_direction(self, client):
        # Define test variables
        target_floor = 4
        wrong_movement_error_message = "You probably call the elevator to up/down and select the the opposite"

        response = client.post("/api/elevators/move", data={
            "target_floor": target_floor,
        })

        response_content = json.loads(response.text)

        assert response.status_code == BAD_REQUEST_STATUS_CODE
        assert response_content.get('error') == wrong_movement_error_message

    def test_move_up_to_floor_in_right_direction(self, client):
        # Define test variables
        target_floor = 9

        response = client.post("/api/elevators/move", data={
            "target_floor": target_floor,
        })

        response_content = json.loads(response.text)

        assert response.status_code == CREATED_STATUS_CODE
        assert response_content.get('move_record_id')

    def test_down_call_elevator(self, client):
        # Define test variables
        call_floor = 4
        direction = DIRECTION_DOWN

        response = client.post(f"/api/elevators/call", data={
            "call_floor": call_floor,
            "direction": direction,
        })

        assert response.status_code == CREATED_STATUS_CODE

    def test_move_down_to_floor_in_wrong_direction(self, client):
        # Define test variables
        target_floor = 6
        wrong_movement_error_message = "You probably call the elevator to up/down and select the the opposite"

        response = client.post("/api/elevators/move", data={
            "target_floor": target_floor,
        })

        response_content = json.loads(response.text)

        assert response.status_code == BAD_REQUEST_STATUS_CODE
        assert response_content.get('error') == wrong_movement_error_message

    def test_move_down_to_floor_in_right_direction(self, client):
        # Define test variables
        target_floor = 3

        response = client.post("/api/elevators/move", data={
            "target_floor": target_floor,
        })

        response_content = json.loads(response.text)

        assert response.status_code == CREATED_STATUS_CODE
        assert response_content.get('move_record_id')

    def test_call_and_move_up_two_times(self, client):
        # Define test variables
        call_floor1 = 5
        call_floor2 = 7
        target_floor1 = 8
        target_floor2 = 9

        # This sleep is to generate and space of time to put the elevator in resting floor
        sleep(15)

        response = client.post(f"/api/elevators/call", data={
            "call_floor": call_floor1,
            "direction": DIRECTION_UP,
        })

        assert response.status_code == CREATED_STATUS_CODE

        response = client.post("/api/elevators/move", data={
            "target_floor": target_floor1,
        })

        response_content = json.loads(response.text)

        assert response.status_code == CREATED_STATUS_CODE
        assert response_content.get('move_record_id')

        response = client.post(f"/api/elevators/call", data={
            "call_floor": call_floor2,
            "direction": DIRECTION_UP,
        })

        assert response.status_code == CREATED_STATUS_CODE

        response = client.post("/api/elevators/move", data={
            "target_floor": target_floor2,
        })

        response_content = json.loads(response.text)

        assert response.status_code == CREATED_STATUS_CODE
        assert response_content.get('move_record_id')

    def test_call_and_move_down_two_times(self, client):
        # Define test variables
        call_floor1 = 8
        call_floor2 = 6
        target_floor1 = 1
        target_floor2 = 5

        # This sleep is to generate and space of time to put the elevator in resting floor
        sleep(15)

        response = client.post(f"/api/elevators/call", data={
            "call_floor": call_floor1,
            "direction": DIRECTION_DOWN,
        })

        assert response.status_code == CREATED_STATUS_CODE

        response = client.post("/api/elevators/move", data={
            "target_floor": target_floor1,
        })

        response_content = json.loads(response.text)

        assert response.status_code == CREATED_STATUS_CODE
        assert response_content.get('move_record_id')

        response = client.post(f"/api/elevators/call", data={
            "call_floor": call_floor2,
            "direction": DIRECTION_DOWN,
        })

        assert response.status_code == CREATED_STATUS_CODE

        response = client.post("/api/elevators/move", data={
            "target_floor": target_floor2,
        })

        response_content = json.loads(response.text)

        assert response.status_code == CREATED_STATUS_CODE
        assert response_content.get('move_record_id')

    def test_move_down_move_up(self, client):
        # Define test variables
        call_floor1 = -1
        call_floor2 = -8
        target_floor1 = -7
        target_floor2 = 9

        # This sleep is to generate and space of time to put the elevator in resting floor
        sleep(10)

        response = client.post(f"/api/elevators/call", data={
            "call_floor": call_floor1,
            "direction": DIRECTION_DOWN,
        })

        assert response.status_code == CREATED_STATUS_CODE

        response = client.post("/api/elevators/move", data={
            "target_floor": target_floor1,
        })

        response_content = json.loads(response.text)

        assert response.status_code == CREATED_STATUS_CODE
        assert response_content.get('move_record_id')

        response = client.post(f"/api/elevators/call", data={
            "call_floor": call_floor2,
            "direction": DIRECTION_UP,
        })

        assert response.status_code == CREATED_STATUS_CODE

        response = client.post("/api/elevators/move", data={
            "target_floor": target_floor2,
        })

        response_content = json.loads(response.text)

        assert response.status_code == CREATED_STATUS_CODE
        assert response_content.get('move_record_id')

    def test_move_up_move_down(self, client):
        # Define test variables
        call_floor1 = 2
        call_floor2 = 5
        target_floor1 = 4
        target_floor2 = 1

        # This sleep is to generate and space of time to put the elevator in resting floor

        response = client.post(f"/api/elevators/call", data={
            "call_floor": call_floor1,
            "direction": DIRECTION_UP,
        })

        assert response.status_code == CREATED_STATUS_CODE

        response = client.post("/api/elevators/move", data={
            "target_floor": target_floor1,
        })

        response_content = json.loads(response.text)

        assert response.status_code == CREATED_STATUS_CODE
        assert response_content.get('move_record_id')

        response = client.post(f"/api/elevators/call", data={
            "call_floor": call_floor2,
            "direction": DIRECTION_DOWN,
        })

        assert response.status_code == CREATED_STATUS_CODE

        response = client.post("/api/elevators/move", data={
            "target_floor": target_floor2,
        })

        response_content = json.loads(response.text)

        assert response.status_code == CREATED_STATUS_CODE
        assert response_content.get('move_record_id')
