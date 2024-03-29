import pytest
from datetime import datetime
from src.storage.utils import datetime_to_integer


@pytest.mark.parametrize(
    ("dt", "expected"),
    [
        (datetime(year=2024, month=4, day=1, hour=10, minute=15), 1015),
        (datetime(year=2024, month=4, day=1, hour=14, minute=30), 1430),
        (datetime(year=2024, month=4, day=1, hour=0, minute=0), 0),
        (datetime(year=2024, month=4, day=1, hour=23, minute=59), 2359),
        (datetime(year=2024, month=4, day=1, hour=0, minute=1), 1),
        (datetime(year=2024, month=4, day=1, hour=1, minute=0), 100),
        (datetime(year=2024, month=4, day=1, hour=1, minute=0), 100),
    ],
)
def test_datetime_to_integer(dt, expected):
    result = datetime_to_integer(dt)
    assert result == expected
