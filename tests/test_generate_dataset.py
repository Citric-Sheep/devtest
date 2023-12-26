from scr.generate_dataset import GenerateDataset
from datetime import datetime
import pytest



@pytest.fixture
def generator():
    return GenerateDataset()


def test_floor_weights_mapping(generator):
    generator.floor_capacities = {
        "Residential": 20,
        "Social": 100,
        "entrance": 200,
        "Company": 40,
    }

    generator.floor_types = {"1": "entrance", "10": "Social", "2": "Company"}

    generator.floor_number = 10

    expected_result = [
        0.43043478260869567,
        0.08260869565217391,
        0.03913043478260869,
        0.03913043478260869,
        0.03913043478260869,
        0.03913043478260869,
        0.03913043478260869,
        0.03913043478260869,
        0.03913043478260869,
        0.21304347826086953,
    ]
    # Call the method to be tested
    generator.floor_weights_mapping()

    # Check the results/assertions
    assert hasattr(
        generator, "weight_list"
    )  # Check if weight_list attribute is created
    assert (
        len(generator.weight_list) == generator.floor_number
    )  # Check if the length is correct
    assert generator.weight_list == expected_result
    assert isinstance(generator.weight_list, list)  # Check if the result is an integer


def test_pick_random_floor_weighted(generator):
    # Set mock values for testing (replace these with appropriate values for your test)
    generator.floor_number = 5
    generator.weight_list = [0.5, 0.1, 0.3, 0.2, 0.2]

    # Call the method to be tested
    result = generator.pick_random_floor_weighted()

    # Check the results/assertions
    assert isinstance(result, int)  # Check if the result is an integer
    assert (
        1 <= result <= generator.floor_number
    )  # Check if the result is within the valid floor range


def test_pick_next_door(generator):
    # Set mock values for testing (replace these with appropriate values for your test)
    generator.floor_number = 5
    generator.weight_list = [0.2, 0.1, 0.3, 0.2, 0.2]
    generator.demand_floor = 3  # Set a specific demand floor for testing

    # Call the method to be tested
    result = generator.pick_next_door()

    # Check the results/assertions
    assert isinstance(result, int)  # Check if the result is an integer
    assert (
        result != generator.demand_floor
    )  # Check if the result is different from the demand floor
    assert (
        1 <= result <= generator.floor_number
    )  # Check if the result is within the valid floor range


def test_calculate_interval_minutes(generator):
    # Set mock values for testing (replace these with appropriate values for your test)
    generator.current_floor = 2
    generator.demand_floor = 4
    generator.next_floor = 3
    generator.min_time_interval_seconds = 60
    generator.max_time_interval_seconds = 300
    generator.interval_per_floor_seconds = 30
    generator.start_time = datetime(
        2023, 1, 1, 12, 0, 0
    )  # Set a specific start time for testing
    generator.peak_hours = [{"start": 9, "end": 17}]
    generator.peak_multiplier = 1.5
    generator.random_minutes_range = {"min": 5, "max": 15}

    # Call the method to be tested
    result = generator.calculate_interval_minutes()

    # Check the results/assertions
    assert isinstance(
        result, (int, float)
    )  # Check if the result is a valid numeric type
    assert result >= 0  # Check if the result is a non-negative value
