import sys
import os
import pytest

# Add source directory to sys.path so we can import the module
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../examples/src_project"))
if src_path not in sys.path:
    sys.path.insert(0, src_path)

import pytest
import example_module

# REQ-ID: REQ-101

@pytest.mark.parametrize("a, b, expected", [
    (1, 2, 3),          # Positive integers
    (0, 5, 5),          # Handling zero (first argument)
    (5, 0, 5),          # Handling zero (second argument)
    (0, 0, 0),          # Handling zero (both arguments)
    (-1, -2, -3),       # Handling negative integers (both negative)
    (-1, 2, 1),         # Handling negative integers (mixed signs, negative first)
    (1, -2, -1),        # Handling negative integers (mixed signs, negative second)
    (-5, 5, 0),         # Handling negative integers (mixed signs, result zero)
    (1000, 2000, 3000), # Larger positive integers
    (-1_000_000, 500_000, -500_000), # Larger mixed integers
])
def test_add_handles_negatives_and_zeros(a, b, expected):
    # REQ-ID: REQ-101: Should handle negatives and zeros.
    assert example_module.add(a, b) == expected

@pytest.mark.parametrize("a, b", [
    (1, 2),
    (0, 5),
    (-1, -2),
    (-1, 2),
    (100, -200),
    (0, 0),
    (2**60, 2**61), # Large integers (Python's int type handles arbitrary precision)
    (-2**60, 2**61),
])
def test_add_commutative_property(a, b):
    # REQ-ID: REQ-101: Commutative property: add(a,b) == add(b,a).
    assert example_module.add(a, b) == example_module.add(b, a)

import sys
import os
import pytest

# Add source directory to sys.path so we can import the module
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../examples/src_project"))
if src_path not in sys.path:
    sys.path.insert(0, src_path)

import pytest
from example_module import safe_divide

# REQ-102: safe_divide(x:float, y:float) -> float

def test_safe_divide_positive_numbers():
    # REQ-102: Basic division
    assert safe_divide(4.0, 2.0) == 2.0

@pytest.mark.parametrize("x, y, expected", [
    (10.0, 2.0, 5.0),
    (5.0, 1.0, 5.0),
    (0.0, 5.0, 0.0),
    (-4.0, 2.0, -2.0),  # REQ-102: Preserve sign
    (4.0, -2.0, -2.0),  # REQ-102: Preserve sign
    (-10.0, -2.0, 5.0), # REQ-102: Preserve sign
    (3.0, 2.0, 1.5),
    (1.0, 3.0, pytest.approx(0.3333333333333333))
])
def test_safe_divide_various_valid_inputs(x, y, expected):
    # REQ-102: Basic division, preserve sign, handle decimals
    assert safe_divide(x, y) == expected

@pytest.mark.parametrize("x", [1.0, -1.0, 0.0, 100.0, -100.0])
def test_safe_divide_by_zero_raises_value_error(x):
    # REQ-102: Raise ValueError with message "division by zero" on y == 0
    with pytest.raises(ValueError) as excinfo:
        safe_divide(x, 0.0)
    assert str(excinfo.value) == "division by zero"

import sys
import os
import pytest

# Add source directory to sys.path so we can import the module
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../examples/src_project"))
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from example_module import Math

# REQ-ID: REQ-103
def test_Math_square_basic():
    obj = Math()
    result = obj.square(1)
    assert result is not None

def test_Math_square_bad_inputs():
    obj = Math()
    with pytest.raises(Exception):
        getattr(obj, "square")(*[None for _ in range(1)])
