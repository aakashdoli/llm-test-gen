from __future__ import annotations
import os
import re
import sys
from pathlib import Path
from typing import List, Optional
from .ast_extract import FunctionInfo
from .prompts import build_prompt
from .llm_provider import LLMProvider
from .guardrails import compiles, safe_content, sanitize

PATH_SETUP_PY = """
import sys
import os
import pytest

# Add source directory to sys.path so we can import the module
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "{rel_path}"))
if src_path not in sys.path:
    sys.path.insert(0, src_path)
""".strip()

SKELETON_PYTEST_FUNC = """
{path_setup}

from {module} import {func}

# REQ-ID: {req_id}
def test_{func}_basic():
    # TODO: Replace placeholders with real assertions
    result = {func}({call_args})
    assert result is not None

def test_{func}_bad_inputs():
    with pytest.raises(Exception):
        {func}(*[None for _ in range({argc})])
""".lstrip()

SKELETON_PYTEST_METHOD = """
{path_setup}

from {module} import {cls}

# REQ-ID: {req_id}
def test_{cls}_{func}_basic():
    obj = {cls}()
    result = obj.{func}({call_args})
    assert result is not None

def test_{cls}_{func}_bad_inputs():
    obj = {cls}()
    with pytest.raises(Exception):
        getattr(obj, "{func}")(*[None for _ in range({argc})])
""".lstrip()

SKELETON_ROBOT = """
*** Settings ***
Documentation     Test suite generated for {module}
...               Traceability: {req_id}
Library           {library_path}

*** Test Cases ***
Test {func} Basic
    [Documentation]    Basic positive test for {func}
    [Tags]    {req_id}
    ${{result}}=    {func_call}    {robot_args}
    Should Not Be Equal    ${{result}}    ${{None}}

Test {func} Error
    [Documentation]    Verify error handling (expecting failure with bad args)
    [Tags]    {req_id}    Negative
    Run Keyword And Expect Error    * {func_call}    {robot_bad_args}
""".lstrip()

def _find_req_id(func_name: str, design_text: Optional[str]) -> str:
    if not design_text:
        return "N/A"
    for line in design_text.splitlines():
        if func_name in line and "REQ-" in line:
            match = re.search(r"(REQ-\d+)", line)
            if match:
                return match.group(1)
    return "N/A"

def _generate_arg_values(arg_names: List[str], annotations: dict) -> List[str]:
    values = []
    for arg in arg_names:
        hint = annotations.get(arg, "").lower()
        if "int" in hint: val = "1"
        elif "float" in hint or "decimal" in hint: val = "0.5"
        elif "str" in hint: val = "'x'"
        elif "bool" in hint: val = "True"
        elif "list" in hint or "iterable" in hint: val = "[]"
        elif "dict" in hint or "mapping" in hint: val = "{}"
        else: val = "0"
        values.append(val)
    return values

def rule_based_skeleton(fn: FunctionInfo, rel_path: str, design_text: Optional[str], framework: str) -> str:
    req_id = _find_req_id(fn.name, design_text)
    
    explicit_args = fn.args
    is_method = "." in fn.qualname and explicit_args and explicit_args[0] == "self"
    if is_method:
        explicit_args = explicit_args[1:]
    
    val_list = _generate_arg_values(explicit_args, fn.annotations)
    argc = len(explicit_args)

    if framework == "robot":
        library_path = str(Path(rel_path) / f"{fn.module.split('.')[-1]}.py")
        func_call = fn.name
        robot_args = "    ".join(val_list)
        robot_bad_args = "    ".join(["${None}"] * argc)
        
        return SKELETON_ROBOT.format(
            module=fn.module,
            library_path=library_path,
            func=fn.name,
            func_call=func_call,
            robot_args=robot_args,
            robot_bad_args=robot_bad_args,
            req_id=req_id
        )

    else:
        path_block = PATH_SETUP_PY.format(rel_path=rel_path)
        call_args = ", ".join(val_list)
        
        if "." in fn.qualname:
            cls = fn.qualname.split(".", 1)[0]
            return SKELETON_PYTEST_METHOD.format(
                path_setup=path_block,
                module=fn.module, cls=cls, func=fn.name,
                call_args=call_args, argc=argc, req_id=req_id
            )
        return SKELETON_PYTEST_FUNC.format(
            path_setup=path_block,
            module=fn.module, func=fn.name,
            call_args=call_args, argc=argc, req_id=req_id
        )

def generate_for_function(fn: FunctionInfo, design_text: Optional[str], provider: LLMProvider, rel_path: str, framework: str) -> str:
    if provider.provider:
        prompt = build_prompt(fn, design_text, framework)
        code = provider.generate(prompt)
        
        if code:
            clean_code = sanitize(code)
            
            if framework == "pytest":
                if compiles(clean_code) and safe_content(clean_code):
                    # CRITICAL FIX: Prepend the sys.path setup to the AI-generated code
                    path_block = PATH_SETUP_PY.format(rel_path=rel_path)
                    return f"{path_block}\n\n{clean_code}"
            else:
                # Basic check for Robot
                if safe_content(clean_code):
                    return clean_code
    
    return rule_based_skeleton(fn, rel_path, design_text, framework)

def write_tests(funcs: List[FunctionInfo], out_dir: str, src_dir: str, design_text: Optional[str] = None, framework: str = "pytest") -> int:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    provider = LLMProvider()
    
    try:
        rel_path = os.path.relpath(Path(src_dir).resolve(), Path(out_dir).resolve())
    except Exception:
        rel_path = str(Path(src_dir).resolve())

    by_module = {}
    for fn in funcs:
        by_module.setdefault(fn.module, []).append(fn)
        
    count = 0
    ext = "robot" if framework == "robot" else "py"
    
    for module, fns in by_module.items():
        test_parts = []
        for fn in fns:
            test_parts.append(generate_for_function(fn, design_text, provider, rel_path, framework))
        
        test_src = "\n\n".join(test_parts)
        test_file = out / f"test_{module.replace('.', '_')}.{ext}"
        test_file.write_text(test_src, encoding="utf-8")
        count += 1
    
    return count