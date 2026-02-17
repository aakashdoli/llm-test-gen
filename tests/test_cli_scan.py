import subprocess
from pathlib import Path


def run(cmd, cwd):
    # Determine the executable path based on the current environment.
    # If we are in a venv, 'llm-testgen' should be in the bin directory.
    # However, to be safe and environment-agnostic in tests, we rely on PATH
    # or assume 'llm-testgen' is available.
    return subprocess.run(
        cmd,
        cwd=cwd,
        text=True,
        capture_output=True,
        check=True,
    )


def test_scan_summary_output():
    repo_root = Path(__file__).resolve().parents[1]
    src_dir = repo_root / "tests" / "examples" / "sample_project"

    r = run(["llm-testgen", "scan", "--src", str(src_dir)], cwd=str(repo_root))
    assert "Functions found:" in r.stdout


def test_scan_verbose_output():
    repo_root = Path(__file__).resolve().parents[1]
    src_dir = repo_root / "tests" / "examples" / "sample_project"

    r = run(["llm-testgen", "scan", "--src", str(src_dir), "--verbose"], cwd=str(repo_root))
    assert "sample:add" in r.stdout or "sample_project.sample:add" in r.stdout
