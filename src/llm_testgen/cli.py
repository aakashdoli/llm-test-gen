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
    p_scan.add_argument("--ignore", help="Comma-separated list of directories to ignore", default="")
    p_scan.add_argument("--verbose", action="store_true", help="Print every discovered function (default: summary only)")

    p_gen = sub.add_parser("generate", help="Generate pytest files")
    p_gen.add_argument("--src", required=True, help="Source directory to analyze")
    p_gen.add_argument("--out", required=True, help="Output directory for tests")
    p_gen.add_argument("--design", help="Optional design/requirements markdown file")
    # Added framework argument back if it was missing in your version
    p_gen.add_argument("--framework", choices=["pytest", "robot"], default="pytest", help="Target test framework (default: pytest)")
    p_gen.add_argument("--ignore", help="Comma-separated list of directories to ignore", default="")

    p_eval = sub.add_parser("evaluate", help="Evaluate compile success of generated tests")
    p_eval.add_argument("--tests", required=True, help="Directory containing generated tests")
    p_eval.add_argument("--out", default="metrics.json", help="Path to write JSON metrics")

    args = parser.parse_args()

    if args.cmd == "scan":
        ignore_list = [x.strip() for x in args.ignore.split(",") if x.strip()]
        funcs = scan_python_functions(args.src, ignore_patterns=ignore_list)

        if args.verbose:
            for f in funcs:
                print(f"{f.module}:{f.qualname} args={f.args} returns={f.returns}")
        else:
            print(f"Scanned: {args.src}")
            if ignore_list:
                print(f"Ignored: {', '.join(ignore_list)}")
            print(f"Functions found: {len(funcs)}")
            # Optional: show first 20 only, to give a preview
            preview = funcs[:20]
            if preview:
                print("Preview (first 20):")
                for f in preview:
                    print(f"- {f.module}:{f.qualname}")

        return

    if args.cmd == "generate":
        design_text = None
        if args.design and Path(args.design).exists():
            design_text = Path(args.design).read_text(encoding="utf-8")
        
        ignore_list = [x.strip() for x in args.ignore.split(",") if x.strip()]
        funcs = scan_python_functions(args.src, ignore_patterns=ignore_list)
        
        # Ensure we capture the framework argument safely
        framework = getattr(args, 'framework', 'pytest')
        
        count = write_tests(funcs, args.out, args.src, design_text, framework=framework)
        print(f"Generated {count} {framework} file(s) in {args.out}")
        return

    if args.cmd == "evaluate":
        metrics = write_report(args.tests, args.out)
        print(f"Wrote metrics to {args.out}: {metrics}")
        return

# --- THIS WAS MISSING ---
if __name__ == "__main__":
    main()