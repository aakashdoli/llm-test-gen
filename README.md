# LLM Test Generator (llm-test-gen)

Generate pytest skeleton tests for Python projects using LLMs.
Includes a CLI and an optional Streamlit UI.

## Features
- Scan Python source for functions
- Generate pytest skeleton tests into an output folder
- Evaluate generated tests with simple metrics
- Optional Streamlit UI for ZIP uploads

## Quick start (CLI)

### Install
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip

pip install -e .