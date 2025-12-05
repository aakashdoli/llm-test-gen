from __future__ import annotations
from pathlib import Path
import ast
import re
import json
from typing import Dict, Any

def evaluate_dir(tests_dir: str) -> Dict[str, Any]:
    p = Path(tests_dir)
    # Gather both python and robot files
    py_files = list(p.rglob("test_*.py"))
    robot_files = list(p.rglob("*.robot"))
    all_files = py_files + robot_files
    
    compiles = 0
    req_ids_found = set()
    
    # Check Python Syntax
    for f in py_files:
        content = f.read_text(encoding="utf-8")
        try:
            ast.parse(content)
            compiles += 1
        except Exception:
            pass
        
        # Scan for REQ-ID comments
        ids = re.findall(r"REQ-ID:\s*(REQ-\d+)", content)
        req_ids_found.update(ids)

    # Check Robot "Syntax" (Basic check) and Traceability
    for f in robot_files:
        content = f.read_text(encoding="utf-8")
        # We assume robot files "compile" if they are non-empty for this tool
        if len(content.strip()) > 0:
            compiles += 1
            
        # Scan for Robot Tags [Tags] REQ-123
        ids = re.findall(r"REQ-\d+", content)
        req_ids_found.update(ids)

    return {
        "files_total": len(all_files),
        "files_python": len(py_files),
        "files_robot": len(robot_files),
        "compile_success": compiles,
        "traceability_unique_reqs": len(req_ids_found),
        "req_ids": list(req_ids_found)
    }

def write_report(tests_dir: str, out_path: str):
    metrics = evaluate_dir(tests_dir)
    Path(out_path).write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    return metrics