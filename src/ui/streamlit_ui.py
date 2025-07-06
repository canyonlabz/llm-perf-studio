import sys
import asyncio
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
import os

# Importing necessary modules
from src.utils.config import load_config  # Importing configuration loader
from src.utils.test_state import TestState

# --- Load Configuration -----------------------------------------------------

# Load the full configuration from config.yaml
module_config = load_config()
general_config = module_config.get("general", {})
ui_config = module_config.get("user_interface", {})

# --- Initialize Session State ------------------------------------------------

# Initialize session state
if "session_started" not in st.session_state:
    st.session_state.session_started = False
# Initialize the LLM mode in session state if not already present
if "llm_mode" not in st.session_state:
    st.session_state.llm_mode = "ollama"  # Default LLM model ("ollama" or "openai")
# Initialize the agent logs in session state if not already present
if "jmeter_logs" not in st.session_state:
    st.session_state.jmeter_logs = []
# initialize the JMeter state in session state if not already present
if "jmeter_state" not in st.session_state:
    # Mirror the same shape your pipeline expects
    st.session_state.jmeter_state = {
        "jmx_path": "",
        "jmx_valid": False,
        "vusers": None,
        "ramp_up": None,
        "duration": None,
        "iterations": None,
        "jmeter_test_results": {},
        "jmeter_jtl_path": "",
        "jmeter_log_path": "",
        "run_counts": {},
        "use_rag": False,  # Whether to use RAG mode
        "prompt_num": 1,  # Number of prompts to use from input JSON file
        "run_timestamp": "",
    }
# Initialize the selected RAG file in session state if not already present
if "selected_rag_file" not in st.session_state:
    st.session_state.selected_rag_file = None
# Initialize the RAG mode in session state if not already present
if "rag_mode" not in st.session_state:
    st.session_state.rag_mode = False  # Default RAG mode (False or True)
# Initialize the selected JMeter JMX file in session state if not already present
if "selected_jmx_file" not in st.session_state:
    st.session_state.selected_jmx_file = None
if "jmeter_test_state" not in st.session_state:
    st.session_state.jmeter_test_state = TestState.NOT_STARTED
if 'jmeter_thread_data' not in st.session_state:
    st.session_state['jmeter_thread_data'] = {
        'logs': [],
        'status': None,
        'results': None,
        'jmeter_jtl_path': "",
        'jmeter_log_path': "",
        'analysis': None,
        'stop_requested': False,
    }

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
    page_homepage = st.Page("nav_pages/page_homepage.py", title="Home", icon="🏠")
    page_jmeter = st.Page("nav_pages/page_jmeter.py", title="JMeter", icon="📊")
    page_deepeval = st.Page("nav_pages/page_deepeval.py", title="DeepEval", icon="📈")

    pg = st.navigation(
        pages=[page_homepage, page_jmeter, page_deepeval],
        position="sidebar",
    )
    pg.run()

# --- Main Function ---------------------------------------------------------

if __name__ == "__main__":
    render_ui()

