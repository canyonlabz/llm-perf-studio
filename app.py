# test.py
import os
import subprocess
import sys
from pathlib import Path
import asyncio
import logging
import warnings

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

# Suppress Streamlit thread warnings
logging.getLogger("streamlit.runtime.scriptrunner.script_runner").setLevel(logging.ERROR)
warnings.filterwarnings("ignore", message=".*missing ScriptRunContext.*")

# Disable Streamlit's file watcher to avoid issues with file changes (production use case)
#os.environ["STREAMLIT_SERVER_ENABLE_WATCHER"] = "false"
os.environ["STREAMLIT_SERVER_FILE_WATCHER_TYPE"] = "poll"

# 1. Ensure the API key is set (either via .env or in your shell env)
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError(
        "Please set OPENAI_API_KEY in your environment or .env file before running this test."
    )

# 2. Locate the Streamlit UI script
here = Path(__file__).parent
ui_app = here / "src" / "ui" / "streamlit_ui.py"
if not ui_app.exists():
    print(f"❌ Could not find Streamlit UI at {ui_app}", file=sys.stderr)
    sys.exit(1)

# Add the project root to PYTHONPATH
project_root = str(here)
env = os.environ.copy()
env["PYTHONPATH"] = f"{project_root}{os.pathsep}{env.get('PYTHONPATH', '')}"

# 3. Launch Streamlit
print(f"🚀 Launching Streamlit UI: {ui_app}")
try:
    subprocess.run(
        ["streamlit", "run", str(ui_app)],
        check=True,
        env=env
    )
except subprocess.CalledProcessError as e:
    print("❌ Failed to launch Streamlit:", e, file=sys.stderr)
    sys.exit(e.returncode)
