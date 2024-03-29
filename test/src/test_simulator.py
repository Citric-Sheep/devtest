import pytest
from datetime import datetime
from src.simulator import run
from src.storage import ElevatorDatabase
from src.parameters.utils import generate_lambda_table
import os


@pytest.mark.parametrize(
    ("floors", "lambdas", "start_datetime", "end_datetime", "time_unit_in_minutes"),
    [
        (
            5,
            generate_lambda_table(1.0, 5.0),
            datetime(2024, 4, 1, 8, 0),
            datetime(2024, 4, 1, 9, 0),
            5,

        ),
        (
            10,
            generate_lambda_table(2.5, 3.5),
            datetime(2024, 4, 30, 23, 0),
            datetime(2024, 5, 1, 0, 0),
            10,
        ),
        (
            20,
            generate_lambda_table(0.0, 0.8),
            datetime(2024, 4, 1, 12, 0),
            datetime(2024, 4, 5, 13, 0),
            60,
        ),
    ],
)
def test_run(floors: int, lambdas: dict[str, dict[str, float]], start_datetime, end_datetime, time_unit_in_minutes):
    test_timestamp = datetime.now().timestamp()
    db_name=f"test_simulator_elevator_{test_timestamp}.db"
    csv_filename = f"test_simulator_calls_{test_timestamp}.csv"
    run(
        floors,
        lambdas,
        start_datetime,
        end_datetime,
        time_unit_in_minutes,
        reset=True,
        db_name=db_name,
        csv_filename=csv_filename,
    )
    assert check_database(floors, db_name)
    os.remove(csv_filename)
    os.remove(db_name)


def check_database(floors, db_name):
    db = ElevatorDatabase(db_name=db_name)
    db.cursor.execute("SELECT * FROM call")
    rows = db.cursor.fetchall()
    db.close()

    # check if rows were inserted
    if len(rows) == 0:
        return False

    # Check if source_floor and destination_floor are within the range (1, floors)
    for row in rows:
        source_floor = row[2]
        destination_floor = row[3]
        if not (source_floor in range(1, floors + 1) and destination_floor in range(1, floors + 1)):
            return False

    return True
