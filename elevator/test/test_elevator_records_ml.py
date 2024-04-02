class TestElevatorRecordsML:
    def test_movements_for_ml_records(self, client):
        pass

    def test_ml_records(self, client):
        elevator_id = 1
        response = client.get(f"/api/elevator_records_ml/get_ml_records/{elevator_id}")
        # Confirm if the data with the same floor as target and current are resting floor
        debug = ""
