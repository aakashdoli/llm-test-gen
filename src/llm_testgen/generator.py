SKELETON_FUNC = """
import pytest
from {module} import {func}

def test_{func}_basic():
    # TODO: Replace placeholders with real assertions
    result = {func}({call_args})
    assert result is not None

def test_{func}_bad_inputs():
    with pytest.raises(Exception):
        {func}(*[None for _ in range({argc})])
""".lstrip()

SKELETON_METHOD = """
import pytest
from {module} import {cls}

def test_{cls}_{func}_basic():
    obj = {cls}()
    result = obj.{func}({call_args})
    assert result is not None

def test_{cls}_{func}_bad_inputs():
    obj = {cls}()
    with pytest.raises(Exception):
        getattr(obj, "{func}")(*[None for _ in range({argc})])
""".lstrip()

def rule_based_skeleton(fn: FunctionInfo) -> str:
    call_args = _default_args(fn)
    # If qualname has a dot, treat it as Class.method
    if "." in fn.qualname:
        cls = fn.qualname.split(".", 1)[0]
        return SKELETON_METHOD.format(
            module=fn.module, cls=cls, func=fn.name,
            call_args=call_args, argc=len(fn.args)
        )
    # Otherwise it's a top-level function
    return SKELETON_FUNC.format(
        module=fn.module, func=fn.name,
        call_args=call_args, argc=len(fn.args)
    )
