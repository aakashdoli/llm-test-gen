# LLM Test Generator (llm-test-gen)

Generate pytest skeleton tests for Python projects using LLMs.
Includes a CLI and an optional Streamlit UI.

## Features

- **Scan**: Recursively scan Python source files for functions and methods.
- **Generate**: Create pytest skeleton tests using an LLM (requires API key).
- **Evaluate**: Run generated tests and report success/failure metrics.
- **UI**: Optional Streamlit interface for easy interaction.

## Installation

```bash
# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install package (editable mode recommended for development)
pip install -e .

# Install with UI dependencies if you plan to use the Streamlit app
pip install -e ".[ui]"

# Install dev dependencies for running tests
pip install -e ".[dev]"
```

## CLI Usage

The `llm-testgen` command is the main entry point.

### 1. Scan for functions

Scans the source directory and lists discovered functions.

```bash
llm-testgen scan --src <source_directory>
```

**Options:**
- `--ignore`: Comma-separated list of directories to exclude (default includes `.venv`, `venv`, `node_modules`, `dist`, `build`, `__pycache__`, `.git`).
- `--verbose`: Print every discovered function signature. Default is a summary view.

**Examples:**
```bash
# Default summary view
llm-testgen scan --src .

# Full list of functions
llm-testgen scan --src . --verbose

# Ignore specific folders
llm-testgen scan --src . --ignore "tests,legacy_code"
```

### 2. Generate tests

Generates pytest files based on the scanned functions and optional design documents.

```bash
llm-testgen generate --src <source_directory> --out <output_directory> --design <path_to_requirements.md>
```

**Options:**
- `--provider`: LLM provider to use (default: `google`).
- `--model`: Model name (default: `gemini-pro`).
- `--ignore`: Comma-separated list of directories to exclude.

**Note**: You must set the appropriate API key environment variable (e.g., `GOOGLE_API_KEY`) before running.

### 3. Evaluate tests

Runs the generated tests using `pytest` and reports the results.

```bash
llm-testgen evaluate --test-dir <output_directory>
```

## Streamlit UI

For a visual interface, use the Streamlit app:

```bash
streamlit run ui/app.py
```

The UI allows you to:
1.  Upload a ZIP file of your project.
2.  Scan for functions.
3.  Generate tests using an LLM.
4.  Download the generated test suite.