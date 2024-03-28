from models.models import Building, Elevator, Demand


def test_building_model_init():
    building = Building(name="Test Building", address="123 Main St", city="Test City", country="Test Country")
    assert building.name == "Test Building"
    assert building.address == "123 Main St"
    assert building.city == "Test City"
    assert building.country == "Test Country"


def test_elevator_model_init():
    elevator = Elevator(building_id=1, max_floors=10, local_identifier=3)
    assert elevator.building_id == 1
    assert elevator.max_floors == 10
    assert elevator.local_identifier == 3


def test_demand_model_init():
    demand = Demand(elevator_id=1, start_floor=3, end_floor=5)
    assert demand.elevator_id == 1
    assert demand.start_floor == 3
    assert demand.end_floor == 5
