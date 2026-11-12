"""Pure unit tests of arithmetic functions."""

import pytest

from calculator import calculate


def test_addition():
    assert calculate(2, 3, "add") == 5


def test_subtraction():
    assert calculate(9, 4, "subtract") == 5


def test_multiplication():
    assert calculate(3, 7, "multiply") == 21


def test_division():
    assert calculate(12, 3, "divide") == 4


def test_division_by_zero():
    with pytest.raises(ValueError, match="divide by zero"):
        calculate(12, 0, "divide")


def test_invalid_operation():
    with pytest.raises(ValueError, match="Unsupported"):
        calculate(2, 3, "unknown")


def test_rejects_boolean_input():
    with pytest.raises(ValueError, match="must be a number"):
        calculate(True, 3, "add")
