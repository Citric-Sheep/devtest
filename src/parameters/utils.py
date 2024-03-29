import numpy as np
import sys
sys.path.append('..')
from src.constants import DAYS_OF_THE_WEEK


def _generate_lambda_values(
        min_lambda: float,
        max_lambda: float,
    ) -> dict[str, float]:
    """
    Generate random lambda values between min_lambda and max_lambda for 24 hours.

    Args:
        min_lambda (float): The minimum lambda value for the Poisson distribution.
        max_lambda (float): The maximum lambda value for the Poisson distribution.

    Raises:
        Exception: If min_lambda or max_lambda is negative.
        Exception: If min_lambda is greater than max_lambda.

    Returns:
        dict[str, float]: A dictionary where each key represents an hour of the day (in 24-hour format),
        and the value is a random lambda value within the specified range.
    """
    if min_lambda < 0 or max_lambda < 0:
        raise Exception("lambda values must be non-negative")
    if max_lambda < min_lambda:
        raise Exception("min_lambda cannot be greater than max_lambda")

    lambda_values_per_hour = {
        str(hour).zfill(2): np.random.uniform(min_lambda, max_lambda)
        for hour in range(24)
    }
    return lambda_values_per_hour



def generate_lambda_table(
        min_lambda: float,
        max_lambda: float,
    ) -> dict[str, dict[str, float]]:
    """
    Generate a dictionary with keys as days of the week and values as lambda values for each hour.

    Args:
        min_lambda (float): The minimum lambda value for the Poisson distribution.
        max_lambda (float): The maximum lambda value for the Poisson distribution.

    Raises:
        Exception: If min_lambda or max_lambda is negative.
        Exception: If min_lambda is greater than max_lambda.

    Returns:
        dict[str, dict[str, float]]: A dictionary where each key is a day of the week, and the value is another dictionary
        containing lambda values for each hour of that day.
    """
    if min_lambda < 0 or max_lambda < 0:
        raise Exception("lambda values must be non-negative")
    if max_lambda < min_lambda:
        raise Exception("min_lambda cannot be greater than max_lambda")

    lambda_dict = {
        day: _generate_lambda_values(min_lambda, max_lambda)
        for day in DAYS_OF_THE_WEEK
    }
    return lambda_dict
