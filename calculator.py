"""Business logic for a tiny calculator service."""

import math


def calculate(a: float, b: float, operation: str) -> float:
    """Perform one arithmetic operation and reject invalid input."""
    for name, value in (("a", a), ("b", b)):
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(f"{name} must be a number")
        if not math.isfinite(value):
            raise ValueError(f"{name} must be finite")

    if operation == "add":
        return a + b
    if operation == "subtract":
        return a - b
    if operation == "multiply":
        return a * b
    if operation == "divide":
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b
    raise ValueError("Unsupported operation")
