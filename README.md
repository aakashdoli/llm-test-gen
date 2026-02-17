# llm-test-gen

CLI + Streamlit UI to scan Python code and generate pytest skeleton tests using LLMs (Gemini or OpenAI).

## What it does
- `scan`: find functions/classes in a source directory
- `generate`: create pytest skeleton tests for discovered functions
- `evaluate`: basic evaluation report for generated tests
- **Optional Streamlit UI**: upload a ZIP project and generate tests via a web interface

## Install (recommended)
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip

pip install -e .
```

## Configure LLM provider

**Gemini:**
```bash
export GEMINI_API_KEY="..."
export LLM_PROVIDER="gemini"
```

**OpenAI:**
```bash
export OPENAI_API_KEY="..."
export LLM_PROVIDER="openai"
```

## CLI usage

### Scan (summary by default)
```bash
llm-testgen scan --src path/to/project
```

**Ignore extra directories:**
```bash
llm-testgen scan --src path/to/project --ignore "tests,docs"
```

**Verbose mode (prints every discovered function):**
```bash
llm-testgen scan --src path/to/project --verbose
```

### Generate tests
```bash
llm-testgen generate --src path/to/project --out generated_tests
```

**With design/requirements context:**
```bash
llm-testgen generate --src path/to/project --out generated_tests --design examples/design/requirements.md
```

**Ignore directories during generation:**
```bash
llm-testgen generate --src path/to/project --out generated_tests --ignore "tests,docs"
```

### Evaluate
```bash
llm-testgen evaluate --tests generated_tests --out metrics.json
```

## Streamlit UI (optional)

**Install UI dependencies:**
```bash
pip install -e ".[ui]"
```

**Run:**
```bash
streamlit run ui/app.py
```

## Project structure

- `src/llm_testgen/`: core library + CLI
- `ui/app.py`: Streamlit UI
- `tests/`: automated tests
- `examples/`: small demo inputs and design docs
- `examples/_playground/`: experimental sandbox code (not required)

## Development

**Run tests:**
```bash
pip install -e ".[dev]"
pytest -q
```