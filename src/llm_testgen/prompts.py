from __future__ import annotations
from dataclasses import asdict
from typing import Optional, List
from .ast_extract import FunctionInfo

def build_prompt(fn: FunctionInfo, design_text: Optional[str]) -> str:
    meta = asdict(fn)
    design_snip = design_text[:1500] if design_text else ""
    return f"""You are an expert software test engineer.
Generate a concise, runnable pytest file that tests the target function thoroughly.

Target:
- module: {meta['module']}
- qualname: {meta['qualname']}
- args: {meta['args']}
- types: {meta['annotations']}
- returns: {meta['returns']}
- docstring: {meta['docstring']}

Design context (optional, may be empty):
{design_snip}

Constraints:
- Use only 'pytest' and Python stdlib.
- Do NOT do any network or file I/O.
- Include boundary, negative, and at least one property-like test if possible.
- Prefer small, deterministic inputs.
- If behavior is ambiguous, insert clear TODOs.

Return ONLY the test file content. Do not wrap in markdown.
"""
