from calc import add, divide
import pytest


def test_add():
    a = 2
    b = 3

    result = add(a, b)

    assert result == 5


def test_divide_by_zero_raises_error():
    with pytest.raises(ValueError):
        divide(10, 0)