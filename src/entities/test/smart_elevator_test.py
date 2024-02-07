from src.entities.smart_elevator import SmartElevator


def test_smart_elevator_instance():
    return SmartElevator()


def test_frequency_prediction():
    elevator = SmartElevator()
    most_used_floor = 4

    for _ in range(10):
        for floor in range(1, 5):
            elevator.press_floor_button(floor)
            elevator.press_floor_button(most_used_floor)
            elevator.run(seconds_per_floor=0, print_debug=False)

    elevator.train()
    elevator.run(seconds_per_floor=0, print_debug=False)
    assert elevator.get_best_floor_by_hour() == most_used_floor
    # the elevator should go to the most used floor


def test_frequency_prediction_v2():
    elevator = SmartElevator()
    most_used_floor = 2

    for _ in range(10):
        elevator.press_floor_button(most_used_floor)
        elevator.run(seconds_per_floor=0, print_debug=False)

    elevator.train()
    elevator.run(seconds_per_floor=0, print_debug=False)
    assert elevator.get_best_floor_by_hour() == 2

    most_used_floor = 0
    for _ in range(10):
        elevator.press_floor_button(most_used_floor)
        elevator.run(seconds_per_floor=0, print_debug=False)

    elevator.train()
    elevator.run(seconds_per_floor=0, print_debug=False)
    assert elevator.get_best_floor_by_hour() == 0


def test_cost_minimization():
    elevator = SmartElevator()
    weights = [5, 4, 3, 4, 5]
    best_floor = elevator._minimize_cost(weights, 4)
    assert best_floor == 2

    weights = [0, 0, 0, 0, 5]
    best_floor = elevator._minimize_cost(weights, 4)
    assert best_floor == 4

    weights = [5, 0, 0, 0, 0]
    best_floor = elevator._minimize_cost(weights, 4)
    assert best_floor == 0
