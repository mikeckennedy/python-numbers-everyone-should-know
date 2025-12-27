"""
A small local module for import time benchmarking.

This module is intentionally minimal to measure baseline local import overhead.
"""

CONSTANT = 42
VALUES = [1, 2, 3, 4, 5]


def simple_function():
    """A simple function."""
    return CONSTANT


class SimpleClass:
    """A simple class."""

    def __init__(self, value):
        self.value = value

    def get_value(self):
        return self.value
