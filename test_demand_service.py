import unittest
from src.services.demand_service import DemandService

class TestDemandService(unittest.TestCase):
    def setUp(self):
        # Create an instance of DemandService for testing
        self.demand_service = DemandService(db_path=":memory:")  # Use in-memory SQLite for testing

    def test_create_demand(self):
        demand = self.demand_service.create_demand(floor=3, timestamp="2024-02-05 12:30:00")
        print(f"\ncreate_demand test: {demand.to_dict()}")
        self.assertIsNotNone(demand)
        self.assertEqual(demand.floor, 3)

    def test_get_demand(self):
        demand = self.demand_service.create_demand(floor=3, timestamp="2024-02-05 12:30:00")
        retrieved_demand = self.demand_service.get_demand(demand_id=demand.demand_id)
        print(f"\nget_demand test: {retrieved_demand.to_dict()}")
        self.assertIsNotNone(retrieved_demand)
        self.assertEqual(retrieved_demand.demand_id, demand.demand_id)

    def test_delete_demand(self):
        demand = self.demand_service.create_demand(floor=2, timestamp="2024-02-05 11:00:00")

        retrieved_demand = self.demand_service.get_demand(demand_id=demand.demand_id)
        print(f"\nget_demand before deletion: {retrieved_demand.to_dict()}")
        self.assertIsNotNone(retrieved_demand)

        self.demand_service.delete_demand(demand_id=demand.demand_id)
        print("Deleted Demand")

        retrieved_demand_after_deletion = self.demand_service.get_demand(demand_id=demand.demand_id)
        print(f"get_demand after deletion: {retrieved_demand_after_deletion}")

        self.assertIsNone(retrieved_demand_after_deletion)

    def tearDown(self):
        # Clean up resources after the test
        self.demand_service.connection.close()

if __name__ == "__main__":
    unittest.main()