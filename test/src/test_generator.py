import pytest
from src.generator import (
    _get_elevator_calls_count,
    get_elevator_calls,
)


@pytest.mark.parametrize(
    ("lambda_value"),
    [
        (1.0),
        (2.0),
        (3.0),
    ],
)
def test__get_elevator_calls_count(lambda_value: float):
    calls_count = _get_elevator_calls_count(lambda_value)
    assert isinstance(calls_count, int)
    assert calls_count >= 0


@pytest.mark.parametrize(
    ("lambda_value"),
    [
        (-1.0),
    ],
)
def test__get_elevator_calls_count_exception(lambda_value: float):
    with pytest.raises(Exception):
        _get_elevator_calls_count(lambda_value)


@pytest.mark.parametrize(
    ("lambda_value", "floors"),
    [
        (1.0, 5),
        (2.0, 10),
        (3.0, 20),
    ],
)
def test_get_elevator_calls(lambda_value: float, floors: int):
    calls = get_elevator_calls(lambda_value, floors)
    assert isinstance(calls, list)
    for call in calls:
        assert isinstance(call, dict)
        assert "source_floor" in call
        assert "destination_floor" in call
        assert isinstance(call["source_floor"], int)
        assert isinstance(call["destination_floor"], int)


@pytest.mark.parametrize(
    ("lambda_value", "floors"),
    [
        (-1.0, 10),
    ],
)
def test_get_elevator_calls_exception_a(lambda_value: float, floors: int):
    with pytest.raises(Exception):
        get_elevator_calls(lambda_value, floors)


@pytest.mark.parametrize(
    ("lambda_value", "floors"),
    [
        (1.0, 0),
    ],
)
def test_get_elevator_calls_exception_b(lambda_value: float, floors: int):
    with pytest.raises(Exception):
        get_elevator_calls(lambda_value, floors)
