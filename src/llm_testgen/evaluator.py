from __future__ import annotations
from pathlib import Path
import ast, json
from typing import Dict

def evaluate_dir(tests_dir: str) -> Dict[str, int]:
    p = Path(tests_dir)
    files = list(p.rglob("test_*.py"))
    compiles = 0
    for f in files:
        try:
            ast.parse(f.read_text(encoding="utf-8"))
            compiles += 1
        except Exception:
            pass
    return {"files": len(files), "compile_success": compiles}

def write_report(tests_dir: str, out_path: str):
    metrics = evaluate_dir(tests_dir)
    Path(out_path).write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    return metrics
