from datetime import datetime, timedelta
import sys
sys.path.append('..')
from src.storage import ElevatorDatabase
from src.generator import get_elevator_calls
from .utils import log_time, log_params, validate_params

def run(
        floors: int,
        lambdas: dict[str, dict[str, float]],
        start_datetime: datetime,
        end_datetime: datetime,
        time_unit_in_minutes: int,
        reset: bool = False,
        db_name: str = "elevator.db",
        csv_filename: str = "calls.csv",
    ) -> None:
    """
    Run the elevator simulation.

    Args:
        floors (int): The total number of floors in the building.
        lambdas (dict[str, dict[str, float]]): A dictionary containing lambda values for each day of the week and each hour.
        start_datetime (datetime): The start datetime of the simulation.
        end_datetime (datetime): The end datetime of the simulation.
        time_unit_in_minutes (int): The time unit in minutes for each simulation step.
        reset (bool, optional): Whether to reset the database before running the simulation. Defaults to False.
        db_name (str, optional): The filename of the database. Defaults to "elevator.db".
        csv_filename (str, optional): The filename of the CSV file for exporting data. Defaults to "calls.csv".
    """
    validate_params(floors, start_datetime, end_datetime, time_unit_in_minutes)

    # log params
    log_params(floors, lambdas, start_datetime, end_datetime, time_unit_in_minutes)

    # init database
    db = ElevatorDatabase(db_name)
    # reset database if needed
    if reset:
        db.reset()

    # start time defined in parameters
    t = start_datetime

    # discrete event simulation loop
    print("\n[SIMULATION STARTED]\n")
    while t < end_datetime:
        # extract feature: day_of_week
        day_of_week = t.strftime('%A')
        # use day of week and hour to get lambda value
        hour = t.strftime('%H')
        lambda_value = lambdas[day_of_week][hour]
        # generate calls using lambda value
        calls = get_elevator_calls(lambda_value, floors)
        # if any calls, push them to the storage
        if len(calls) > 0:
            db.push(calls, day_of_week, t)
        # to track simulation progress
        log_time(t)
        # increase time for next iteration
        t += timedelta(minutes=time_unit_in_minutes)
    print("\n[SIMULATION ENDED]\n")

    # export data to csv
    db.export(filename=csv_filename)
    print("\n[DATA EXPORTED]\n")
    # close database connection
    db.close()
