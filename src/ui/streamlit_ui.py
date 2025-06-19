import sys
import asyncio
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
import os
from src.utils.config import load_config  # Importing configuration loader

print("🔍 CWD:", os.getcwd())
# --- Load Configuration -----------------------------------------------------

# Load the full configuration from config.yaml
module_config = load_config()
general_config = module_config.get("general", {})
ui_config = module_config.get("user_interface", {})

# --- Render UI ---------------------------------------------------------------

def render_ui():
    """
    Render the main UI for the LLM Performance Test Studio.
    This function sets up the Streamlit page configuration, initializes the navigation,
    and renders the header, title, chatbot area, and buttons.
    """
    # Set the page configuration for Streamlit
    # This is the main entry point for the Streamlit app.
    st.set_page_config(page_title="LLM Performance Test Studio", layout="wide")

    # Set the page configuration for Streamlit
    page_homepage = st.Page("pages/page_homepage.py", title="Home", icon="🏠")
    page_jmeter = st.Page("pages/page_jmeter.py", title="JMeter", icon="📊")
    page_deepeval = st.Page("pages/page_deepeval.py", title="DeepEval", icon="📈")

    pg = st.navigation(
        pages=[page_homepage, page_jmeter, page_deepeval],
        position=True,
    )
    pg.run()

# --- Main Function ---------------------------------------------------------

if __name__ == "__main__":
    render_ui()

