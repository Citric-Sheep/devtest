import pytest
from src.parameters.utils import (
    _generate_lambda_values,
    generate_lambda_table,
)
from src.constants import DAYS_OF_THE_WEEK


@pytest.mark.parametrize(
    ("min_lambda", "max_lambda"),
    [
        (1.0, 5.0),
        (2.0, 3.0),
        (3.0, 3.0),
    ],
)
def test__generate_lambda_values(min_lambda: float, max_lambda: float):
    lambda_values = _generate_lambda_values(min_lambda, max_lambda)
    assert isinstance(lambda_values, dict)
    assert len(lambda_values) == 24
    for hour, value in lambda_values.items():
        assert hour in [str(i).zfill(2) for i in range(24)]
        assert isinstance(value, float)
        assert min_lambda <= value <= max_lambda


@pytest.mark.parametrize(
    ("min_lambda", "max_lambda"),
    [
        (-1.0, 5.0),
        (2.0, -3.0),
    ],
)
def test__generate_lambda_values_exception_a(min_lambda: float, max_lambda: float):
    with pytest.raises(Exception):
        _generate_lambda_values(min_lambda, max_lambda)


@pytest.mark.parametrize(
    ("min_lambda", "max_lambda"),
    [
        (2.0, 1.0),
        (3.0, 1.0),
    ],
)
def test__generate_lambda_values_exception_b(min_lambda: float, max_lambda: float):
    with pytest.raises(Exception):
        _generate_lambda_values(min_lambda, max_lambda)


@pytest.mark.parametrize(
    ("min_lambda", "max_lambda"),
    [
        (1.0, 5.0),
        (2.0, 3.0),
        (3.0, 3.0),
    ],
)
def test_generate_lambda_table(min_lambda: float, max_lambda: float):
    lambda_table = generate_lambda_table(min_lambda, max_lambda)
    assert isinstance(lambda_table, dict)
    assert len(lambda_table) == 7
    for day, lambda_values_per_hour in lambda_table.items():
        assert day in DAYS_OF_THE_WEEK
        assert isinstance(lambda_values_per_hour, dict)
        assert len(lambda_values_per_hour) == 24
        for hour, value in lambda_values_per_hour.items():
            assert hour in [str(i).zfill(2) for i in range(24)]
            assert isinstance(value, float)
            assert min_lambda <= value <= max_lambda


@pytest.mark.parametrize(
    ("min_lambda", "max_lambda"),
    [
        (-1.0, 5.0),
        (2.0, -3.0),
    ],
)
def test_generate_lambda_table_exception_a(min_lambda: float, max_lambda: float):
    with pytest.raises(Exception):
        generate_lambda_table(min_lambda, max_lambda)


@pytest.mark.parametrize(
    ("min_lambda", "max_lambda"),
    [
        (2.0, 1.0),
        (3.0, 1.0),
    ],
)
def test_generate_lambda_table_exception_b(min_lambda: float, max_lambda: float):
    with pytest.raises(Exception):
        generate_lambda_table(min_lambda, max_lambda)
