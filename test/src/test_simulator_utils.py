import pytest
from src.simulator.utils import validate_params
from datetime import datetime


@pytest.mark.parametrize(
    ("floors", "start_datetime", "end_datetime", "time_unit_in_minutes"),
    [
        (10, datetime(2024, 4, 1, 12, 0), datetime(2024, 4, 1, 13, 0), 10),
    ],
)
def test_validate_params(floors, start_datetime, end_datetime, time_unit_in_minutes):
    assert validate_params(floors, start_datetime, end_datetime, time_unit_in_minutes)


@pytest.mark.parametrize(
    ("floors", "start_datetime", "end_datetime", "time_unit_in_minutes"),
    [
        (0, datetime(2024, 4, 1, 12, 0), datetime(2024, 4, 1, 13, 0), 10),
        (1, datetime(2024, 4, 1, 12, 0), datetime(2024, 4, 1, 13, 0), 10),
        (10, datetime(2024, 4, 1, 13, 0), datetime(2024, 3, 1, 13, 0), 10),
        (10, datetime(2024, 4, 1, 13, 0), datetime(2024, 4, 1, 13, 0), 10),
        (10, datetime(2024, 4, 1, 12, 0), datetime(2024, 4, 1, 13, 0), 2.5),
        (10, datetime(2024, 4, 1, 12, 0), datetime(2024, 4, 1, 13, 0), 0),
        (10, datetime(2024, 4, 1, 12, 0), datetime(2024, 4, 1, 13, 0), -1),
    ],
)
def test_validate_params_exception(floors, start_datetime, end_datetime, time_unit_in_minutes):
    with pytest.raises(Exception):
        validate_params(floors, start_datetime, end_datetime, time_unit_in_minutes)