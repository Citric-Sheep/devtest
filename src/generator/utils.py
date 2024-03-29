import numpy as np


def generate_two_unique_random_numbers(max_value: int) -> tuple[int]:
    """
    Generate two unique random numbers within the range [1, max_value].

    Args:
        max_value (int): The maximum value (inclusive) for the random numbers.

    Raises:
        Exception: If max_value is less than or equal to 1.

    Returns:
        tuple[int]: A tuple containing two unique random numbers.
    """
    if max_value <= 1:
        raise Exception("max_value must be greater than 1")

    number1 = np.random.randint(1, max_value)
    number2 = np.random.randint(1, max_value)

    # Ensure numbers are unique
    while number2 == number1:
        number2 = np.random.randint(1, max_value)

    return number1, number2

