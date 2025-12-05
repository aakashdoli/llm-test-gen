import streamlit as st
import os
import subprocess
import zipfile
import shutil
import sys
import re
from pathlib import Path

# --- Configuration ---
st.set_page_config(page_title="AI Test Generator", page_icon="🤖", layout="wide")

st.title("🤖 Universal AI Test Generator")
st.markdown("Upload any Python project. I will auto-detect dependencies, install them, and generate tests.")

# --- Helper 1: Fix Bad Folder Names ---
def sanitize_folder_name(extract_path):
    """
    Renames the extracted folder to ensure it's a valid Python module name.
    """
    extract_path_str = str(extract_path)
    subdirs = [d for d in os.listdir(extract_path_str) if os.path.isdir(os.path.join(extract_path_str, d))]
    
    if not subdirs:
        return None

    original_name = subdirs[0]
    # Replace hyphens/spaces with underscores
    safe_name = re.sub(r'[^a-zA-Z0-9_]', '_', original_name)
    
    if original_name != safe_name:
        old_path = os.path.join(extract_path_str, original_name)
        new_path = os.path.join(extract_path_str, safe_name)
        
        if os.path.exists(new_path):
            shutil.rmtree(new_path)
            
        os.rename(old_path, new_path)
        print(f"Renamed '{original_name}' to '{safe_name}'")
        return safe_name
        
    return original_name

# --- Helper 2: Auto-Install Dependencies (NEW!) ---
def install_dependencies(project_path):
    """
    Scans the project for dependency files and installs them using pip.
    """
    req_file = project_path / "requirements.txt"
    setup_file = project_path / "setup.py"
    
    installed_any = False

    try:
        # Strategy A: requirements.txt
        if req_file.exists():
            with st.spinner("📦 Found requirements.txt! Installing dependencies..."):
                subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", str(req_file)])
            st.toast("✅ Dependencies installed from requirements.txt", icon="📦")
            installed_any = True
            
        # Strategy B: setup.py
        if setup_file.exists():
            with st.spinner("📦 Found setup.py! Installing project in editable mode..."):
                subprocess.check_call([sys.executable, "-m", "pip", "install", "-e", str(project_path)])
            st.toast("✅ Project installed via setup.py", icon="🛠️")
            installed_any = True
            
        if not installed_any:
            st.info("ℹ️ No requirements.txt or setup.py found. Assuming standard library only.")
            
    except subprocess.CalledProcessError as e:
        st.error(f"❌ Failed to install dependencies. Error: {e}")

# ---------------------------------------------

# --- Sidebar ---
with st.sidebar:
    st.header("⚙️ Settings")
    api_key = st.text_input("Google Gemini API Key", type="password")
    if api_key:
        os.environ["GEMINI_API_KEY"] = api_key

# --- Main Interface ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Upload Project")
    uploaded_file = st.file_uploader("Upload .zip file", type="zip")
    
    st.subheader("2. Requirements")
    requirements = st.text_area("What should the code do?", height=150, value="Handle valid inputs correctly. Raise ValueError for invalid inputs.")

# --- Logic ---
if st.button("🚀 Generate & Run Tests", type="primary"):
    if not api_key:
        st.error("❌ Need API Key")
    elif not uploaded_file:
        st.error("❌ Need ZIP file")
    else:
        # Setup Workspace
        workspace = Path("temp_workspace")
        if workspace.exists():
            shutil.rmtree(workspace)
        workspace.mkdir()
        
        # 1. Extract
        zip_path = workspace / "project.zip"
        with open(zip_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
            
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(workspace)

        # 2. Sanitize Folder Name
        project_name = sanitize_folder_name(workspace)
        
        if project_name:
            src_path = workspace / project_name
        else:
            src_path = workspace
            
        st.info(f"📂 Project loaded: {project_name}")

        # 3. AUTO-INSTALL DEPENDENCIES (The Magic Step)
        install_dependencies(src_path)

        # 4. Generate Tests
        req_path = workspace / "requirements.md"
        req_path.write_text(requirements, encoding="utf-8")
        out_path = workspace / "tests_gen"
        out_path.mkdir(exist_ok=True)
        
        st.text("⏳ AI is analyzing code and writing tests...")
        
        # Environment Setup
        current_env = os.environ.copy()
        current_env["PYTHONPATH"] = f"{os.getcwd()}/src:{current_env.get('PYTHONPATH', '')}"
        
        cmd = [
            sys.executable, "-m", "llm_testgen.cli", "generate",
            "--src", str(src_path),
            "--out", str(out_path),
            "--design", str(req_path)
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, env=current_env)
            
            # Show logs for debugging
            with st.expander("Show AI Logs"):
                st.code(result.stdout)
                if result.stderr: st.code(result.stderr)

            # 5. Check & Run Tests
            test_files = list(out_path.glob("test_*.py"))
            if not test_files:
                st.warning("⚠️ No tests generated.")
            else:
                st.success(f"✅ Generated {len(test_files)} test files!")
                
                # Display Code
                tabs = st.tabs([f.name for f in test_files])
                for i, f in enumerate(test_files):
                    with tabs[i]:
                        st.code(f.read_text(), language="python")
                
                # Run Pytest
                st.subheader("🧪 Auto-Running Tests")
                pytest_env = current_env.copy()
                pytest_env["PYTHONPATH"] = f"{str(workspace)}:{pytest_env['PYTHONPATH']}"
                
                test_cmd = [sys.executable, "-m", "pytest", str(out_path)]
                test_result = subprocess.run(test_cmd, capture_output=True, text=True, env=pytest_env)
                
                if test_result.returncode == 0:
                    st.success("🎉 All tests passed!")
                    st.code(test_result.stdout)
                else:
                    st.warning("⚠️ Tests failed (Fix manually below)")
                    st.code(test_result.stdout)
                    st.code(test_result.stderr)

        except Exception as e:
            st.error(f"Critical Error: {e}")

# --- Manual Test Runner ---
st.divider()
st.subheader("🛠️ Fix & Re-Run")
st.markdown("Did tests fail? Edit the files in `temp_workspace/tests_gen` and click below.")

if st.button("🧪 Run Existing Tests Only"):
    workspace = Path("temp_workspace")
    out_path = workspace / "tests_gen"
    
    if not out_path.exists():
        st.error("⚠️ No generated tests found.")
    else:
        st.text("Running pytest...")
        current_env = os.environ.copy()
        current_env["PYTHONPATH"] = f"{str(workspace.resolve())}:{current_env.get('PYTHONPATH', '')}"
        
        cmd = [sys.executable, "-m", "pytest", str(out_path)]
        result = subprocess.run(cmd, capture_output=True, text=True, env=current_env)
        
        if result.returncode == 0:
            st.success("🎉 All tests passed!")
            st.code(result.stdout)
        else:
            st.warning("⚠️ Tests still failing.")
            st.code(result.stdout)
            st.code(result.stderr)