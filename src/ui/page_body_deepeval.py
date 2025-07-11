import altair as alt
import streamlit as st
import streamlit.components.v1 as components
from streamlit_autorefresh import st_autorefresh
from pathlib import Path
import os, sys
from datetime import datetime
import pandas as pd

# Import configuration loader
from src.utils.config import load_config
from src.ui.page_utils import initialize_session_state
from src.ui.page_styles import (
    inject_action_button_styles,
)
from src.utils.event_logs import (
    add_deepeval_log,
)
from src.utils.test_state import TestState

config = load_config()      # Load the full configuration from config.yaml
initialize_session_state()  # Initialize session state for the application

# --- Render UI ---------------------------------------------------------------

def render_page_buttons():
    """
    Render the buttons for the webpage.
    """
    inject_action_button_styles()  # Inject custom styles for action buttons

    # Use 6 columns: spacers + 4 button columns + spacers
    col_left, col1, col2, col3, col4, col_right = st.columns([0.2, 0.15, 0.15, 0.15, 0.15, 0.2], border=True) # Define six columns with specified widths and borders

    with col_left:
        # File uploader to select a task file
        upload_disabled = not st.session_state.session_started
        uploaded_file = st.file_uploader("Choose a file for RAG", type=["txt"], key="task_file_uploader", disabled=upload_disabled)
        
        # If a file is uploaded, store it in session state
        if uploaded_file is not None:
            st.session_state.selected_task_file = uploaded_file

    with col1:
        process_disabled = (
            not st.session_state.session_started or
            st.session_state.selected_task_file is None
        )
        if st.button("Process RAG File", key="upload_task", disabled=process_disabled):
            # Call the function to handle file upload
            ##handle_upload_task(st.session_state.selected_task_file)
            ...  # This is where you would handle the file upload logic

    with col2:
        # Only enabled once we have a formatted task file in state
        formatted = st.session_state.get("jmeter_state", {}).get("formatted_file_path")
        run_disabled = (
            not st.session_state.session_started or
            not formatted or
            not os.path.exists(formatted)
        )
        if st.button("Run Browser Task", key="run_browser_task", disabled=run_disabled):
            # Call the function to handle browser task
            ##handle_run_browser()
            ...

    with col3:
        json_path = st.session_state.get("jmeter_state", {}).get("json_path")
        json_valid = st.session_state.get("jmeter_state", {}).get("json_valid", False)
        jmx_disabled = (
            not st.session_state.session_started or
            not json_path or
            not json_valid
        )
        if st.button("Generate JMX File", key="generate_jmx_file", disabled=jmx_disabled):
            # Call the function to handle JMX file generation
            ##handle_generate_jmx()
            ...

    with col4:
        jmx_path = st.session_state.get("jmeter_state", {}).get("jmx_path")
        jmx_valid = st.session_state.get("jmeter_state", {}).get("jmx_valid", False)
        smoke_disabled = (
            not st.session_state.session_started or
            not jmx_path or
            not jmx_valid
        )
        if st.button("Run Smoke Test", key="run_smoke_test", disabled=smoke_disabled):
            # Call the function to handle smoke test
            ##handle_run_smoke_test()
            ...
