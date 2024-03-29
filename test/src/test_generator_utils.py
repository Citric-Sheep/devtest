import pytest
from src.generator.utils import generate_two_unique_random_numbers


@pytest.mark.parametrize(
    ("max_value"),
    [
        (10),
        (50),
        (100),
    ],
)
def test_generate_two_unique_random_numbers(max_value: int):
    x, y = generate_two_unique_random_numbers(max_value)
    assert 1 <= x <= max_value
    assert 1 <= y <= max_value
    assert x != y


@pytest.mark.parametrize(
    ("max_value"),
    [
        (1),
        (0),
    ],
)
def test_generate_two_unique_random_numbers_exception(max_value: int):
    with pytest.raises(Exception):
        generate_two_unique_random_numbers(max_value)
