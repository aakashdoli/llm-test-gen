from pathlib import Path
import subprocess, sys

def test_generate_and_evaluate(tmp_path: Path):
    repo = Path(__file__).resolve().parents[1]
    src = repo / "examples" / "src_project"
    design = repo / "examples" / "design" / "requirements.md"
    out = tmp_path / "tests_gen"
    # Generate
    r = subprocess.run([sys.executable, "-m", "llm_testgen.cli", "generate", "--src", str(src), "--out", str(out), "--design", str(design)])
    assert r.returncode == 0
    # Evaluate
    r2 = subprocess.run([sys.executable, "-m", "llm_testgen.cli", "evaluate", "--tests", str(out), "--out", str(tmp_path / "metrics.json")])
    assert r2.returncode == 0
    assert (tmp_path / "metrics.json").exists()
