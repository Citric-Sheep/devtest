import os
import json
import csv
import pytest
from time import sleep

CREATED_STATUS_CODE = 201

elevator_id = 0
test_parameters_for_some_movements = [{"call_floor": 5, "direction": 1, "target_floor": 9, "sleep": 0},
                                      {"call_floor": 3, "direction": 1, "target_floor": 8, "sleep": 0},
                                      {"call_floor": 5, "direction": 1, "target_floor": 7, "sleep": 0},
                                      {"call_floor": 6, "direction": 1, "target_floor": 10, "sleep": 20},
                                      {"call_floor": 9, "direction": -1, "target_floor": -2, "sleep": 0},
                                      {"call_floor": 3, "direction": -1, "target_floor": -1, "sleep": 0},
                                      {"call_floor": -2, "direction": 1, "target_floor": 5, "sleep": 20},
                                      {"call_floor": 5, "direction": -1, "target_floor": 1, "sleep": 20},
                                      {"call_floor": 2, "direction": -1, "target_floor": -1, "sleep": 0},
                                      {"call_floor": -1, "direction": 1, "target_floor": 6, "sleep": 0},
                                      {"call_floor": 5, "direction": 1, "target_floor": 10, "sleep": 0}]


class TestElevatorRecordsML:

    def test_create_elevator_for_ml_records(self, client):
        # Define test variables
        global elevator_id

        response = client.post(f"/api/elevators", data={
            "top_floor": 12,
            "lower_floor": -2,
        })

        assert response.status_code == CREATED_STATUS_CODE

        response_content = json.loads(response.text)
        elevator_id = response_content.get("elevator_id")

    @pytest.mark.parametrize("test_parameters", test_parameters_for_some_movements)
    def test_movements_for_ml_records(self, client, test_parameters):

        if test_parameters["sleep"]:
            sleep(test_parameters["sleep"])

        response = client.post(f"/api/elevators/call", data={
            "call_floor": test_parameters["call_floor"],
            "direction": test_parameters["direction"],
        })

        assert response.status_code == CREATED_STATUS_CODE

        response = client.post("/api/elevators/move", data={
            "target_floor": test_parameters["target_floor"],
        })

        assert response.status_code == CREATED_STATUS_CODE

    def test_get_resting_floor_records_to_training_an_ml_model(self, client):
        response = client.get(f"/api/elevator_records_ml/get_ml_records/{elevator_id}")

        resting_floor_records = json.loads(response.text)

        column_names = list(resting_floor_records[0].keys())

        # A csv file is create to look into the data
        file_name = 'training_data/training_data.csv'

        os.makedirs(os.path.dirname(file_name), exist_ok=True)

        with open(file_name, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=column_names)
            writer.writeheader()
            writer.writerows(resting_floor_records)
