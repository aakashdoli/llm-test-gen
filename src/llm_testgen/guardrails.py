from __future__ import annotations
import ast, re

BANNED_PATTERNS = [
    r"requests\.", r"httpx\.", r"urllib\.", r"os\.system", r"subprocess\.",
    r"open\(", r"Path\(", r"shutil\.", r"socket\."
]

def compiles(py_source: str) -> bool:
    try:
        ast.parse(py_source)
        return True
    except Exception:
        return False

def safe_content(py_source: str) -> bool:
    for pat in BANNED_PATTERNS:
        if re.search(pat, py_source):
            return False
    return True

def sanitize(py_source: str) -> str:
    # Basic strip of markers or weird fences
    return py_source.replace("```", "").strip()
