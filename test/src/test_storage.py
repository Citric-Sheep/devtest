import pytest
import os
from src.storage import ElevatorDatabase
from datetime import datetime
from sqlite3 import ProgrammingError


@pytest.fixture
def temp_db():
    test_timestamp = datetime.now().timestamp()
    db_name = f"test_elevator_{test_timestamp}.db"
    db = ElevatorDatabase(db_name=db_name)
    yield db
    db.close()
    os.remove(db_name)



def test_connect(temp_db):
    assert temp_db.connector is not None
    assert temp_db.cursor is not None



def test_create_tables(temp_db):
    # Check if the 'call' table exists
    temp_db.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='call';")
    result = temp_db.cursor.fetchone()
    assert result is not None


@pytest.mark.parametrize(
    ("data"),
    [
        ([(1, 1200, 1, 2), (2, 600, 3, 4)]),
    ],
)
def test_insert(temp_db, data):
    temp_db._insert(data)
    # Check if the data was inserted
    temp_db.cursor.execute("SELECT * FROM call")
    result = temp_db.cursor.fetchall()
    assert len(result) == len(data)


@pytest.mark.parametrize(
    ("calls", "day_of_week", "dt", "expected"),
    [
        (
            [
                {
                    "source_floor": 1,
                    "destination_floor": 2
                },
                {
                    "source_floor": 3,
                    "destination_floor": 4
                }
            ],
            "Monday",
            datetime(year=2024, month=4, day=1, hour=10, minute=0),
            [(1, 1000, 1, 2), (1, 1000, 3, 4)]
        ),
        (
            [
                {
                    "source_floor": 5,
                    "destination_floor": 1
                },
            ],
            "Thursday",
            datetime(year=2024, month=5, day=1, hour=7, minute=55),
            [(4, 755, 5, 1)]
        ),
    ],
)
def test_push(temp_db, calls, day_of_week, dt, expected):
    # Push some calls
    temp_db.push(calls, day_of_week, dt)
    # Check if the data was pushed
    temp_db.cursor.execute("SELECT * FROM call")
    result = temp_db.cursor.fetchall()
    assert len(result) == len(calls)
    assert result == expected



def test_export(temp_db):
    temp_db._insert([(1, 123, 1, 2), (2, 456, 3, 4)])
    csv_filename = f"test_calls_{datetime.now().timestamp()}.csv"
    temp_db.export(csv_filename)
    assert os.path.exists(csv_filename)
    os.remove(csv_filename)



def test_reset(temp_db):
    temp_db._insert([(1, 123, 1, 2), (2, 456, 3, 4)])
    temp_db.reset()
    # Check if the 'call' table was recreated
    temp_db.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='call';")
    result = temp_db.cursor.fetchone()
    assert result is not None


def test_close(temp_db):
    temp_db.close()
    with pytest.raises(ProgrammingError):
        temp_db.cursor.execute("SELECT * FROM calls")

