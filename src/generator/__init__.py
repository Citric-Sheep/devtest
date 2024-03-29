import numpy as np
import sys
sys.path.append('..')
from .utils import generate_two_unique_random_numbers


def _get_elevator_calls_count(lambda_value: float) -> int:
    """
    Get the count of elevator calls based on a given Poisson distribution.

    Args:
        lambda_value (float): The rate parameter (λ) of the Poisson distribution, representing the average rate of calls.

    Raises:
        Exception: If lambda_value is negative.

    Returns:
        int: The number of elevator calls generated based on the Poisson distribution.
    """
    if lambda_value < 0:
        raise Exception("lambda value must be non-negative")

    calls_count = np.random.poisson(lam=lambda_value)
    return calls_count


def get_elevator_calls(lambda_value: float, floors: int) -> dict[str, int]:
    """
    Generate elevator calls based on a given Poisson distribution.

    Args:
        lambda_value (float): The rate parameter (λ) of the Poisson distribution, representing the average rate of calls.
        floors (int): The total number of floors in the building.

    Raises:
        Exception: If lambda_value is negative.
        Exception: If floors is less than or equal to 1.

    Returns:
        list[dict[str, int]]: A list of dictionaries representing elevator calls. Each dictionary contains the source_floor and destination_floor.
    """
    if lambda_value < 0:
        raise Exception("lambda value must be non-negative")
    if floors <= 1:
        raise Exception("floors must be greater than 1")

    calls_count = _get_elevator_calls_count(lambda_value)
    calls = []
    for _ in range(calls_count):
        source_floor, destination_floor = generate_two_unique_random_numbers(
            max_value=floors
        )
        call = {
            "source_floor": source_floor,
            "destination_floor": destination_floor,
        }
        calls.append(call)
    return calls
