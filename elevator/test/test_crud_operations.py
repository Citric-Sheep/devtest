import json
import pytest
from db import elevator

OK_STATUS_CODE = 200
CREATED_STATUS_CODE = 201
NO_CONTENT_STATUS_CODE = 204
BAD_REQUEST_STATUS_CODE = 400

FIRST_ELEVATOR_TOP_FLOOR = 200
FIRST_ELEVATOR_LOWER_FLOOR = -130

first_elevator_id = 0

test_parameters_for_some_movements = [{"call_floor": 5, "direction": 1, "target_floor": 150},
                                      {"call_floor": 120, "direction": 1, "target_floor": 160},
                                      {"call_floor": 140, "direction": 1, "target_floor": 150},
                                      {"call_floor": 100, "direction": -1, "target_floor": -130},
                                      {"call_floor": 200, "direction": -1, "target_floor": 100}]
record_ids_for_movements = []


class TestCrudOperations:

    def test_create_elevator_and_get_details_from_db(self, client):
        # Define the test variables
        global first_elevator_id

        response = client.post(f"/api/elevators", data={
            "top_floor": FIRST_ELEVATOR_TOP_FLOOR,
            "lower_floor": FIRST_ELEVATOR_LOWER_FLOOR,
        })

        assert response.status_code == CREATED_STATUS_CODE

        response_content = json.loads(response.text)
        first_elevator_id = response_content.get("elevator_id")
        elevator_from_db = elevator.get_elevator_by_id(first_elevator_id)

        assert FIRST_ELEVATOR_TOP_FLOOR == elevator_from_db["top_floor"]
        assert FIRST_ELEVATOR_LOWER_FLOOR == elevator_from_db["lower_floor"]

    def test_wrong_creation_of_elevator(self, client):
        # Define the test variables
        wrong_creation_error_message = "top_floor must be grater than lower_floor"

        response = client.post(f"/api/elevators", data={
            "top_floor": FIRST_ELEVATOR_LOWER_FLOOR,
            "lower_floor": BAD_REQUEST_STATUS_CODE,
        })

        assert response.status_code == BAD_REQUEST_STATUS_CODE

        response_content = json.loads(response.text)
        assert response_content.get('error') == wrong_creation_error_message

    def test_create_elevator_and_get_the_current_elevator_for_app(self, client):
        # Define test variables
        elevator_top_floor = 855
        elevator_lower_floor = -350

        response = client.post(f"/api/elevators", data={
            "top_floor": elevator_top_floor,
            "lower_floor": elevator_lower_floor,
        })

        assert response.status_code == CREATED_STATUS_CODE

        response_content = json.loads(response.text)
        elevator_id = response_content.get("elevator_id")

        response = client.get("/api/elevator/current_elevator")

        assert response.status_code == OK_STATUS_CODE
        response_content = json.loads(response.text)

        assert elevator_id == int(response_content.get("current_elevator_id"))
        assert elevator_top_floor == int(response_content.get("top_floor"))
        assert elevator_lower_floor == int(response_content.get("lower_floor"))

    def test_set_and_first_elevator_as_current_and_compare_with_db(self, client):

        response = client.put(f"/api/elevator/current_elevator/{first_elevator_id}")

        assert response.status_code == NO_CONTENT_STATUS_CODE

        response = client.get("/api/elevator/current_elevator")

        assert response.status_code == OK_STATUS_CODE

        response_content = json.loads(response.text)
        elevator_from_db = elevator.get_elevator_by_id(first_elevator_id)

        assert first_elevator_id == int(response_content.get("current_elevator_id")) == elevator_from_db.get("id")
        assert elevator_from_db.get("is_on_demand") == response_content.get("is_on_demand")
        assert elevator_from_db.get("is_up") == response_content.get("is_up")
        assert elevator_from_db.get("is_vacant") == response_content.get("is_vacant")
        assert elevator_from_db.get("last_record") == response_content.get("last_record")
        assert elevator_from_db.get("top_floor") == response_content.get("top_floor")
        assert elevator_from_db.get("lower_floor") == response_content.get("lower_floor")

    @pytest.mark.parametrize("test_parameters", test_parameters_for_some_movements)
    def test_perform_some_movements_for_first_elevator(self, client, test_parameters):
        # Define test variables
        global record_ids_for_movements

        response = client.post(f"/api/elevators/call", data={
            "call_floor": test_parameters["call_floor"],
            "direction": test_parameters["direction"],
        })

        assert response.status_code == CREATED_STATUS_CODE
        response_content = json.loads(response.text)
        call_move_id = response_content.get("elevator_record_id")

        response = client.post("/api/elevators/move", data={
            "target_floor": test_parameters["target_floor"],
        })

        assert response.status_code == CREATED_STATUS_CODE
        response_content = json.loads(response.text)

        to_floor_move_id = response_content.get('move_record_id')
        assert to_floor_move_id

        record_ids_for_movements.append({
            "call_move_id": call_move_id,
            "to_floor_move_id": to_floor_move_id})

    def test_get_records_of_first_elevator_from_app_and_db(self, client):
        elevator_records_from_db = elevator.get_records_by_elevator_id(first_elevator_id)
        response = client.get(f"/api/elevators/records/{first_elevator_id}")
        assert response.status_code == OK_STATUS_CODE

        elevator_records_from_app = json.loads(response.text)

        for index, record_ids_for_movement in enumerate(record_ids_for_movements):
            expected_values = test_parameters_for_some_movements[index]
            call_move_id = record_ids_for_movement["call_move_id"]
            call_move_db = next((db_record for db_record in elevator_records_from_db
                                 if db_record["id"] == call_move_id))

            call_move_app = next((app_record for app_record in elevator_records_from_app
                                 if app_record["id"] == call_move_id))

            assert expected_values["call_floor"] == call_move_db["target_floor"] == call_move_app["target_floor"]
            assert expected_values["direction"] == call_move_db["direction"] == call_move_app["direction"]

