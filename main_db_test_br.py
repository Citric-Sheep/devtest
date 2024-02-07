# Main code to showcase the elevator project features with focus on the bussiness rules
from src.services.elevator_service import ElevatorService
from src.services.demand_service import DemandService

def main():
    # Initialize SQLite database and services
    elevator_service = ElevatorService(db_path="data/database.sqlite")
    demand_service = DemandService(db_path="data/database.sqlite")

    # Create sample elevators
    elevator1 = elevator_service.create_elevator(current_floor=1, resting_floor=1, elevator_status="Idle")
    elevator2 = elevator_service.create_elevator(current_floor=2, resting_floor=2, elevator_status="Idle")
    elevator3 = elevator_service.create_elevator(current_floor=3, resting_floor=3, elevator_status="Idle")

    # Create sample demands
    demand1 = demand_service.create_demand(floor=5, timestamp="2024-02-05 13:00:00")
    demand2 = demand_service.create_demand(floor=2, timestamp="2024-02-05 14:30:00")
    demand3 = demand_service.create_demand(floor=0, timestamp="2024-02-05 15:45:00")

    print("\nSample Elevators:")
    print("Elevator 1:", elevator1.to_dict())
    print("Elevator 2:", elevator2.to_dict())
    print("Elevator 3:", elevator3.to_dict())

    print("\nSample Demands:")
    print("Demand 1:", demand1.to_dict())
    print("Demand 2:", demand2.to_dict())
    print("Demand 3:", demand3.to_dict())

    # Update elevator information
    print("\nUpdated Elevator 1 (Usual):")

    updated_elevator1 = elevator_service.update_elevator(
        elevator_id=elevator1.elevator_id, current_floor=4, resting_floor=5, elevator_status="Moving"
    )
    print(updated_elevator1.to_dict())

    print("\nUpdated Elevator 2 (Bussiness rule 1):")
    updated_elevator2 = elevator_service.update_elevator(
        elevator_id=elevator2.elevator_id, current_floor=5, resting_floor=3, elevator_status="Moving"
    )
    print(updated_elevator2.to_dict())

    print("\nUpdated Elevator 3 (Bussiness rule 2):")
    updated_elevator3 = elevator_service.update_elevator(
        elevator_id=elevator3.elevator_id, current_floor=5, elevator_status="Moving"
    )
    print(updated_elevator3.to_dict())

    # Retrieve Elevator and Demand
    retrieved_elevator = elevator_service.get_elevator(elevator_id=elevator1.elevator_id)
    retrieved_demand = demand_service.get_demand(demand_id=demand1.demand_id)

    print("\nRetrieved Elevator 1:", retrieved_elevator.to_dict())
    print("Retrieved Demand 1:", retrieved_demand.to_dict())

    # Delete Elevator
    elevator_service.delete_elevator(elevator_id=elevator1.elevator_id)
    print("\nDeleted Elevator 1")
    # Delete Demand
    demand_service.delete_demand(demand_id=demand1.demand_id)
    print("\nDeleted Demand 1")

    # Retrieve elevator and demand after deletion
    retrieved_elevator_after_deletion = elevator_service.get_elevator(elevator_id=elevator1.elevator_id)
    retrieved_demand_after_deletion = demand_service.get_demand(demand_id=demand1.demand_id)

    print("\nRetrieved Elevator 1 after deletion:", retrieved_elevator_after_deletion)
    print("Retrieved Demand 1 after deletion:", retrieved_demand_after_deletion)

if __name__ == "__main__":
    main()
