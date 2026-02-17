import sys
import os
import pytest

# Add source directory to sys.path so we can import the module
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if src_path not in sys.path:
    sys.path.insert(0, src_path)

import pytest
from calculator import multiply, is_even # Assuming the module is named 'calculator.py' and contains the 'calculator' object or function directly.

# If 'multiply' is a standalone function in 'calculator.py':
# from calculator import multiply

# If 'multiply' is a method of a Calculator class:
# from calculator import Calculator
# @pytest.fixture
# def calc():
#    return Calculator()

# REQ-001: multiply(a, b)
@pytest.mark.parametrize(
    "a, b, expected",
    [
        # REQ-001: Should handle positive integers.
        (2, 3, 6),
        (10, 1, 10),
        (1, 1, 1),
        (5, 10, 50),
        # REQ-001: Should handle negative integers.
        (-2, 3, -6),
        (2, -3, -6),
        (-2, -3, 6),
        (-10, -1, 10),
        # REQ-001: Any number multiplied by 0 is 0.
        (5, 0, 0),
        (0, 5, 0),
        (0, 0, 0),
        (-7, 0, 0),
        (0, -7, 0),
        # REQ-001: Mixed positive/negative
        (1, -1, -1),
        (-1, 1, -1),
    ]
)
def test_multiply_various_integers(a, b, expected):
    """
    Test multiply function with positive, negative integers and zero.
    Covers REQ-001.
    """
    assert multiply(a, b) == expected

import sys
import os
import pytest

# Add source directory to sys.path so we can import the module
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if src_path not in sys.path:
    sys.path.insert(0, src_path)

import pytest
from calculator import is_even

# REQ-ID: REQ-002
@pytest.mark.parametrize("n, expected", [
    (2, True),    # REQ-002: Even positive
    (4, True),    # REQ-002: Even positive
    (100, True),  # REQ-002: Even positive
    (0, True),    # Common edge case: Zero is even
    (-2, True),   # Common edge case: Negative even
    (-4, True),   # Common edge case: Negative even
])
def test_is_even_returns_true_for_even_numbers(n, expected):
    assert is_even(n) == expected

# REQ-ID: REQ-002
@pytest.mark.parametrize("n, expected", [
    (1, False),   # REQ-002: Odd positive
    (3, False),   # REQ-002: Odd positive
    (99, False),  # REQ-002: Odd positive
    (-1, False),  # Common edge case: Negative odd
    (-3, False),  # Common edge case: Negative odd
])
def test_is_even_returns_false_for_odd_numbers(n, expected):
    assert is_even(n) == expected