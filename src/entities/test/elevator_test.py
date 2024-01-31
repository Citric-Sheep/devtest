import pytest

from src.entities.elevator import Elevator
from src.entities.enumerations.elevator_status import ElevatorStatus


def test_elevator_instance():
    return Elevator()


def test_press_floor_button():
    elevator = Elevator()
    elevator.press_floor_button(1)
    elevator.press_floor_button(1)
    assert elevator.demand_floors == [1]

    elevator.press_floor_button(2)
    assert elevator.demand_floors == [1, 2]


def test_run_elevator_up():
    elevator = Elevator()
    elevator.press_floor_button(2)
    elevator.run(seconds_per_floor=0, print_debug=False)
    assert elevator.actual_floor == 2
    assert elevator.demand_floors == []


def test_run_elevator_down():
    elevator = Elevator()
    elevator.press_floor_button(5)
    elevator.run(seconds_per_floor=0, print_debug=False)
    assert elevator.actual_floor == 5
    assert elevator.demand_floors == []

    elevator.press_floor_button(1)
    elevator.run(seconds_per_floor=0, print_debug=False)
    assert elevator.actual_floor == 1
    assert elevator.demand_floors == []


def test_change_status_elevator():
    elevator = Elevator()
    assert elevator.status == ElevatorStatus.VACANT.value

    elevator.press_floor_button(2)
    elevator._evalutate_state()
    assert elevator.status == ElevatorStatus.DEMAND.value
    elevator.run(seconds_per_floor=0, print_debug=False)

    assert elevator.status == ElevatorStatus.VACANT.value


def test_raise_demand_floors_empty_exception_elevator():
    elevator = Elevator()
    assert elevator.status == ElevatorStatus.VACANT.value

    elevator.press_floor_button(2)
    elevator._evalutate_state()
    elevator.demand_floors = []
    with pytest.raises(Exception):
        elevator._next_floor()


def test_raise_goin_to_is_none_exception_elevator():
    elevator = Elevator()
    assert elevator.status == ElevatorStatus.VACANT.value

    elevator.press_floor_button(2)
    elevator._evalutate_state()
    elevator.going_to = None
    with pytest.raises(Exception):
        elevator._evalutate_motion()
