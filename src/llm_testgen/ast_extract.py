from __future__ import annotations
import ast
from dataclasses import dataclass
from pathlib import Path
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

def scan_python_functions(src_dir: str) -> List[FunctionInfo]:
    base = Path(src_dir)
    results: List[FunctionInfo] = []
    for path in base.rglob("*.py"):
        if any(seg.startswith(".") for seg in path.parts):
            continue
        rel = str(path.relative_to(base))
        module_name = rel.replace("/", ".").removesuffix(".py")
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        results.extend(_collect_functions(tree, module_name, rel))
    return results
