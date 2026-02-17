import os
import tempfile
import zipfile
from pathlib import Path

import streamlit as st

from llm_testgen.ast_extract import scan_python_functions
from llm_testgen.generator import write_tests
from llm_testgen.evaluator import evaluate_dir


st.set_page_config(page_title="LLM Test Generator", layout="wide")
st.title("LLM Test Generator")
st.caption("Upload a Python project ZIP → scan functions → generate pytest tests → evaluate outputs.")


def extract_zip(zip_bytes: bytes, dest: Path) -> Path:
    zip_path = dest / "upload.zip"
    zip_path.write_bytes(zip_bytes)

    with zipfile.ZipFile(zip_path, "r") as zf:
        zf.extractall(dest)

    zip_path.unlink(missing_ok=True)

    dirs = [p for p in dest.iterdir() if p.is_dir()]
    return dirs[0] if len(dirs) == 1 else dest


with st.sidebar:
    st.header("Settings")
    provider = st.selectbox("LLM provider", ["gemini", "openai"], index=0)
    framework = st.selectbox("Framework", ["pytest"], index=0)

    st.markdown("### API keys")
    st.markdown("- Gemini: `GEMINI_API_KEY`")
    st.markdown("- OpenAI: `OPENAI_API_KEY`")
    st.markdown("Provider is selected via `LLM_PROVIDER`.")

uploaded = st.file_uploader("Upload ZIP of a Python project", type=["zip"])

if uploaded is None:
    st.info("Upload a ZIP to start.")
    st.stop()

zip_bytes = uploaded.getvalue()
if not zip_bytes:
    st.error("Uploaded ZIP is empty.")
    st.stop()

ignore_dirs_text = st.text_input(
    "Ignore directories (comma-separated)",
    value="venv,.venv,build,dist,__pycache__,.git,.github",
)
include_tests = st.checkbox("Include existing tests when scanning", value=False)

col1, col2 = st.columns(2)

with tempfile.TemporaryDirectory() as tmp:
    tmp_path = Path(tmp)
    extracted = tmp_path / "extracted"
    extracted.mkdir(parents=True, exist_ok=True)

    project_root = extract_zip(zip_bytes, extracted)

    with col1:
        st.subheader("Scan")
        st.write("Detected project root:", str(project_root))

        if st.button("Scan functions"):
            ignore_dirs = [x.strip() for x in ignore_dirs_text.split(",") if x.strip()]
            funcs = scan_python_functions(
                str(project_root),
                include_tests=include_tests,
                ignore_dirs=ignore_dirs,
            )
            st.session_state["funcs"] = funcs
            st.success(f"Found {len(funcs)} functions.")
            if funcs:
                st.json(funcs[: min(10, len(funcs))])

    with col2:
        st.subheader("Generate")
        max_items = st.number_input("Max functions to generate", min_value=1, max_value=200, value=30)
        do_eval = st.checkbox("Evaluate generated tests", value=True)

        if st.button("Generate tests"):
            funcs = st.session_state.get("funcs", [])
            if not funcs:
                st.error("Scan first, then generate.")
                st.stop()

            os.environ["LLM_PROVIDER"] = provider

            out_dir = tmp_path / "generated_tests"
            out_dir.mkdir(parents=True, exist_ok=True)

            write_tests(
                funcs[: int(max_items)],
                str(project_root),
                str(out_dir),
                framework=framework,
            )

            st.success("Generated tests.")
            st.code(str(out_dir), language="text")

            if do_eval:
                metrics = evaluate_dir(str(out_dir))
                st.markdown("### Evaluation")
                st.json(metrics)

        st.markdown("### Tip")
        st.markdown("Set your API key in the terminal before running Streamlit.")