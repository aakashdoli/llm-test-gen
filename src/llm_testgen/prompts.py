from __future__ import annotations
from dataclasses import asdict
from typing import Optional
from .ast_extract import FunctionInfo

def build_prompt(fn: FunctionInfo, design_text: Optional[str], framework: str = "pytest") -> str:
    meta = asdict(fn)
    design_snip = design_text[:2000] if design_text else ""
    
    if framework == "robot":
        syntax_guide = """
- Output Format: Robot Framework 
- Use '*** Settings ***' for library imports.
- Use '*** Test Cases ***' for tests.
- Use Tags to link Requirements IDs (e.g. [Tags] REQ-123).
"""
    else:
        syntax_guide = """
- Output Format: Python (pytest)
- Use # REQ-ID: <id> comments to link Requirements.
- Use only 'pytest' and Python stdlib.
"""

    return f"""You are an expert software test engineer.
Generate a concise, runnable test file for the target function.

Target:
- module: {meta['module']}
- function: {meta['name']}
- args: {meta['args']}
- types: {meta['annotations']}
- returns: {meta['returns']}
- docstring: {meta['docstring']}

Design context (Requirements):
{design_snip}

Instructions:
1. {syntax_guide}
2. Look for a Requirement ID (e.g., REQ-101) in the design context that relates to this function.
3. If found, explicitly include it (via comment or Tag). If not found, mark as REQ-N/A.
4. Do NOT do any network or file I/O.
5. Prefer small, deterministic inputs.

Return ONLY the test code content. Do not wrap in markdown.
"""