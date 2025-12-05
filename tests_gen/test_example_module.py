import sys
import os
import pytest

# Add source directory to sys.path so we can import the module
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../examples/src_project"))
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from example_module import add

def test_add_basic():
    # TODO: Replace placeholders with real assertions
    result = add(1, 1)
    assert result is not None

def test_add_bad_inputs():
    with pytest.raises(Exception):
        add(*[None for _ in range(2)])


import sys
import os
import pytest

# Add source directory to sys.path so we can import the module
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../examples/src_project"))
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from example_module import safe_divide

def test_safe_divide_basic():
    # TODO: Replace placeholders with real assertions
    result = safe_divide(0.5, 0.5)
    assert result is not None

def test_safe_divide_bad_inputs():
    with pytest.raises(Exception):
        safe_divide(*[None for _ in range(2)])


import sys
import os
import pytest

# Add source directory to sys.path so we can import the module
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../examples/src_project"))
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from example_module import Math

def test_Math_square_basic():
    obj = Math()
    result = obj.square(1)
    assert result is not None

def test_Math_square_bad_inputs():
    obj = Math()
    with pytest.raises(Exception):
        getattr(obj, "square")(*[None for _ in range(1)])
