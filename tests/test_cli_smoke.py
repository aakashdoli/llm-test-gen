from pathlib import Path
import subprocess


def test_generate_and_evaluate(tmp_path: Path):
    repo = Path(__file__).resolve().parents[1]
    src = repo / "examples" / "src_project"
    design = repo / "examples" / "design" / "requirements.md"
    out = tmp_path / "tests_gen"

    r = subprocess.run(
        ["llm-testgen", "generate", "--src", str(src), "--out", str(out), "--design", str(design)],
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0, r.stderr
