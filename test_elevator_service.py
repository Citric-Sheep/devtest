import unittest
from src.services.elevator_service import ElevatorService

class TestElevatorService(unittest.TestCase):
    def setUp(self):
        # Create an instance of ElevatorService for testing
        self.elevator_service = ElevatorService(db_path=":memory:")  # Use in-memory SQLite for testing

    def test_create_elevator(self):
        elevator = self.elevator_service.create_elevator(current_floor=1, resting_floor=1, elevator_status="Idle")
        print(f"\ncreate_elevator test: {elevator.to_dict()}") # Optional, just to better observe via CMD
        self.assertIsNotNone(elevator)
        self.assertEqual(elevator.current_floor, 1)
        self.assertEqual(elevator.resting_floor, 1)
        self.assertEqual(elevator.elevator_status, "Idle")

    def test_get_elevator(self):
        elevator = self.elevator_service.create_elevator(current_floor=1, resting_floor=1, elevator_status="Idle")
        retrieved_elevator = self.elevator_service.get_elevator(elevator_id=elevator.elevator_id)
        print(f"\nget_elevator test: {retrieved_elevator.to_dict()}") # Optional, just to better observe via CMD

        self.assertIsNotNone(retrieved_elevator)
        self.assertEqual(retrieved_elevator.elevator_id, elevator.elevator_id)

    def test_delete_elevator(self):
        elevator = self.elevator_service.create_elevator(current_floor=1, resting_floor=1, elevator_status="Idle")

        retrieved_elevator = self.elevator_service.get_elevator(elevator_id=elevator.elevator_id)
        print(f"\nget_elevator before deletion: {retrieved_elevator.to_dict()}") # Optional, just to better observe via CMD
        self.assertIsNotNone(retrieved_elevator)

        self.elevator_service.delete_elevator(elevator_id=elevator.elevator_id)
        print("Deleted Elevator") # Optional, just to better observe via CMD

        retrieved_elevator_after_deletion = self.elevator_service.get_elevator(elevator_id=elevator.elevator_id)
        print(f"get_elevator after deletion: {retrieved_elevator_after_deletion}") # Optional, just to better observe via CMD

        self.assertIsNone(retrieved_elevator_after_deletion)

    def tearDown(self):
        # Clean up resources after the test
        self.elevator_service.connection.close()

if __name__ == "__main__":
    unittest.main()
