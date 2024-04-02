import json
from time import sleep

DIRECTION_UP = 1
DIRECTION_DOWN = -1
BAD_REQUEST_STATUS_CODE = 400
CREATED_STATUS_CODE = 201
CALL_MOVEMENT_TYPE = "Call"
COMMING_TO_FLOOR = "Coming to floor"


class TestElevator:

    def test_create_an_elevator(self, client):
        # Define test variables
        elevator_top_floor = -8
        elevator_lower_floor = 10

        response = client.post(f"/api/elevators", data={
            "top_floor": elevator_lower_floor,
            "lower_floor": elevator_top_floor,
        })

        # Verify the entire object of elevator
        assert True

    def test_call_elevator(self, client):
        # Define test variables
        call_floor = 5
        direction = 1

        response = client.post(f"/api/elevators/call", data={
            "call_floor": call_floor,
            "direction": direction,
        })

        debug = ""

    def test_move_to_floor_in_wrong_direction(self, client):
        # Define test variables
        target_floor = 4
        wrong_movement_error_message = "You probably call the elevator to up/down and select the the opposite"

        response = client.post("/api/elevators/move", data={
            "target_floor": target_floor,
        })

        response_content = json.loads(response.text)

        assert response.status_code == BAD_REQUEST_STATUS_CODE
        assert response_content.get('error') == wrong_movement_error_message

    def test_move_to_floor_in_right_direction(self, client):
        # Define test variables
        target_floor = 9

        response = client.post("/api/elevators/move", data={
            "target_floor": target_floor,
        })

        response_content = json.loads(response.text)

        assert response.status_code == CREATED_STATUS_CODE
        assert response_content.get('move_record_id')

    def test_call_and_move_two_times(self, client):
        # Define test variables
        call_floor1 = 5
        call_floor2 = 7
        direction = 1
        target_floor1 = 8
        target_floor2 = 9

        sleep(15)

        response = client.post(f"/api/elevators/call", data={
            "call_floor": call_floor1,
            "direction": direction,
        })

        response = client.post("/api/elevators/move", data={
            "target_floor": target_floor1,
        })

        response = client.post(f"/api/elevators/call", data={
            "call_floor": call_floor2,
            "direction": direction,
        })

        response = client.post("/api/elevators/move", data={
            "target_floor": target_floor2,
        })

        response_content = json.loads(response.text)

        assert response.status_code == CREATED_STATUS_CODE
        assert response_content.get('move_record_id')
