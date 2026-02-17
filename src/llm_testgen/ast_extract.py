from __future__ import annotations
import ast
from dataclasses import dataclass
from pathlib import Path
import sys
from typing import List, Optional

@dataclass
class FunctionInfo:
    module: str
    qualname: str
    name: str
    args: List[str]
    annotations: dict
    returns: Optional[str]
    docstring: Optional[str]
    rel_path: str

def _annotation_str(node):
    try:
        return ast.unparse(node)
    except Exception:
        return None

def _collect_functions(tree: ast.AST, module_name: str, rel_path: str) -> List[FunctionInfo]:
    found = []
    class Visitor(ast.NodeVisitor):
        def __init__(self):
            self.stack = []
        def visit_FunctionDef(self, node: ast.FunctionDef):
            qual = ".".join(self.stack + [node.name])
            args = [a.arg for a in node.args.args]
            annotations = {}
            for a in node.args.args:
                if a.annotation is not None:
                    annotations[a.arg] = _annotation_str(a.annotation)
            returns = _annotation_str(node.returns) if node.returns is not None else None
            doc = ast.get_docstring(node)
            found.append(FunctionInfo(
                module=module_name, qualname=qual, name=node.name,
                args=args, annotations=annotations, returns=returns,
                docstring=doc, rel_path=rel_path
            ))
            self.generic_visit(node)
        def visit_ClassDef(self, node: ast.ClassDef):
            self.stack.append(node.name)
            self.generic_visit(node)
            self.stack.pop()
    Visitor().visit(tree)
    return found

DEFAULT_IGNORE_DIRS = {
    "venv", ".venv", "env", ".env",
    "node_modules", "dist", "build",
    "__pycache__", ".git", ".github",
    ".idea", ".vscode", "site-packages"
}

def scan_python_functions(src_dir: str, ignore_patterns: Optional[List[str]] = None) -> List[FunctionInfo]:
    base = Path(src_dir)
    results: List[FunctionInfo] = []
    
    # Merge defaults with user-provided ignores
    ignores = set(DEFAULT_IGNORE_DIRS)
    if ignore_patterns:
        ignores.update(ignore_patterns)

    for path in base.rglob("*.py"):
        # Check if any part of the path is in the ignore list
        if any(part in ignores for part in path.parts):
            continue
            
        if any(seg.startswith(".") and seg not in ignores for seg in path.parts):
            continue
            
        rel = str(path.relative_to(base))
        module_name = rel.replace("/", ".").removesuffix(".py")
        
        try:
            content = path.read_text(encoding="utf-8")
            tree = ast.parse(content)
            results.extend(_collect_functions(tree, module_name, rel))
        except RecursionError:
            print(f"Warning: Skipped {rel} due to recursion depth (file too complex)", file=sys.stderr)
            continue
        except Exception:
            continue
            
    return results
