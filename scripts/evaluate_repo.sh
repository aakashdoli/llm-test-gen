#!/usr/bin/env bash
set -euo pipefail
if [ $# -lt 1 ]; then
  echo "Usage: $0 <tests_dir>"
  exit 1
fi

TESTS_DIR="$1"
python - <<'PY'
import json, sys, pathlib, ast
p = pathlib.Path(sys.argv[1])
files = list(p.rglob("test_*.py"))
compiles = 0
for f in files:
    try:
        ast.parse(f.read_text())
        compiles += 1
    except Exception as e:
        pass
print(json.dumps({"files": len(files), "compile_success": compiles}))
PY
