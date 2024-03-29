from datetime import datetime


def log_lambdas(
        lambdas: dict[str, dict[str, float]],
        time_unit_in_minutes: float
    ) -> None:
    """
    Log the lambda values for each hour of each day.

    Args:
        lambdas (dict[str, dict[str, float]]): A dictionary containing lambda values for each hour of each day.
        time_unit_in_minutes (float): The time unit in minutes used for the simulation.

    """
    print("\tLAMBDAS:\n")
    for day in lambdas:
        print(f"\t\t{day.upper()}\n")
        values = lambdas[day]
        for hour in values:
            lambda_value = values[hour]
            print(f"\t\t\t[{hour}:00]: {lambda_value:.2f} calls each {time_unit_in_minutes} minutes")
        print("\n")


def log_params(
        floors: int,
        lambdas: dict[str, dict[str, float]],
        start_datetime: datetime,
        end_datetime: datetime,
        time_unit_in_minutes: int
    ) -> None:
    """
    Log the parameters used for the simulation.

    Args:
        floors (int): The number of floors in the building.
        lambdas (dict[str, dict[str, float]]): A dictionary containing lambda values for each hour of each day.
        start_datetime (datetime): The starting datetime for the simulation.
        end_datetime (datetime): The ending datetime for the simulation.
        time_unit_in_minutes (int): The time unit in minutes used for the simulation.
    """
    print("\n[PARAMETERS]\n")
    print("\tFLOORS:", floors, "\n")
    print("\tSTART DATETIME:", start_datetime)
    print("\tEND DATETIME:", end_datetime, "\n")
    print("\tTIME UNIT IN MINUTES:", time_unit_in_minutes, "\n")
    log_lambdas(lambdas, time_unit_in_minutes)


def log_time(dt: datetime) -> None:
    """
    Log the current time if it's midnight.

    Args:
        dt (datetime): The datetime object representing the current time.
    """
    # if midnight we log time
    # note: this may not log anything depending TIME_UNIT_IN_MINUTES value
    if dt.hour == 0 and dt.minute == 0:
        print("\tCURRENT TIME:", dt)


def validate_params(
        floors: int,
        start_datetime: datetime,
        end_datetime: datetime,
        time_unit_in_minutes: int
    ) -> bool:
    """
    Validate the parameters used for the simulation.

    Args:
        floors (int): The number of floors in the building.
        start_datetime (datetime): The starting datetime for the simulation.
        end_datetime (datetime): The ending datetime for the simulation.
        time_unit_in_minutes (int): The time unit in minutes used for the simulation.

    Raises:
        Exception: If floors is less than or equal to 1.
        Exception: If end_datetime is less than or equal to start_datetime.
        Exception: If time_unit_in_minutes is not a positive integer.

    Returns:
        bool: True if parameters are valid.
    """
    if floors <= 1:
        raise Exception("floors must be greater than 1")
    if end_datetime <= start_datetime:
        raise Exception("end datetime must be greater than start datetime")
    if not isinstance(time_unit_in_minutes, int) or time_unit_in_minutes <= 0:
        raise Exception("time_unit_in_minutes must be a positive integer")
    return True
