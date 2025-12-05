from __future__ import annotations
import argparse
from pathlib import Path
from .ast_extract import scan_python_functions
from .generator import write_tests
from .evaluator import write_report

def main():
    parser = argparse.ArgumentParser(prog="llm-testgen", description="Generate tests from code + design docs (LLM optional)")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_scan = sub.add_parser("scan", help="Scan for functions")
    p_scan.add_argument("--src", required=True, help="Source directory")

    p_gen = sub.add_parser("generate", help="Generate test files")
    p_gen.add_argument("--src", required=True, help="Source directory to analyze")
    p_gen.add_argument("--out", required=True, help="Output directory for tests")
    p_gen.add_argument("--design", help="Optional design/requirements markdown file")
    p_gen.add_argument("--framework", choices=["pytest", "robot"], default="pytest", help="Target test framework (default: pytest)")

    p_eval = sub.add_parser("evaluate", help="Evaluate generated tests and traceability")
    p_eval.add_argument("--tests", required=True, help="Directory containing generated tests")
    p_eval.add_argument("--out", default="metrics.json", help="Path to write JSON metrics")

    args = parser.parse_args()

    if args.cmd == "scan":
        funcs = scan_python_functions(args.src)
        for f in funcs:
            print(f"{f.module}:{f.qualname} args={f.args} returns={f.returns}")
        return

    if args.cmd == "generate":
        design_text = None
        if args.design and Path(args.design).exists():
            design_text = Path(args.design).read_text(encoding="utf-8")
        funcs = scan_python_functions(args.src)
        # Pass src_dir and framework preference
        count = write_tests(funcs, args.out, args.src, design_text, framework=args.framework)
        print(f"Generated {count} {args.framework} file(s) in {args.out}")
        return

    if args.cmd == "evaluate":
        metrics = write_report(args.tests, args.out)
        print(f"Wrote metrics to {args.out}: {metrics}")
        return