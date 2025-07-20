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
    inject_deepeval_viewer_styles,
)
from src.utils.event_logs import (
    add_deepeval_log,
)
from src.utils.test_state import TestState

config = load_config()      # Load the full configuration from config.yaml
initialize_session_state()  # Initialize session state for the application

# ============================================================================
# DeepEval Body: This section contains the main body of the DeepEval report page.
# ============================================================================
def get_button_states():
    """
    Get the current states of the DeepEval buttons based on the JMeter test state.
    Returns a dictionary with the states of the buttons.
    """
    state = st.session_state.jmeter_test_state
    return {
        "start_deepeval_disabled": state != TestState.COMPLETED,
        "clear_deepeval_logs_disabled": state != TestState.COMPLETED
    }

def render_deepeval_viewer():
    """
    Render the DeepEval viewer area.
    This function sets up the Streamlit components for displaying the DeepEval results.
    """
    inject_deepeval_viewer_styles()  # Inject custom styles for the DeepEval viewer

    # Get current running state
    test_state = get_button_states()
    start_deepeval_disabled, clear_deepeval_logs_disabled = (
        test_state["start_deepeval_disabled"],   # True if test is running (prevents duplicate starts)
        test_state["clear_deepeval_logs_disabled"]  # Disabled if test is running (Clear Logs button)
    )

    # Centered column for the DeepEval viewer
    col_left, col_deepeval_viewer, col_right = st.columns([0.10, 0.80, 0.10], border=False)

    with col_left:
        # Button to start the DeepEval quality assessment
        if st.button("▶️ Start DeepEval", 
                disabled=start_deepeval_disabled,
                help="Start the DeepEval quality assessment with the selected configuration.",
                key="start_deepeval"
            ):
            # Only allow if not already running
            if st.session_state.jmeter_test_state != TestState.RUNNING:
                add_deepeval_log("🏃‍♂️ Starting DeepEval quality assessment...", agent_name="DeepEvalAgent")
                add_deepeval_log("Preparing to execute DeepEval with selected configuration.", agent_name="DeepEvalAgent")

    # Display the DeepEval results
    with col_deepeval_viewer:
        st.subheader("DeepEval Results Viewer")
        
        # Check if DeepEval results are available in session state
        if 'deepeval_results' in st.session_state:
            deepeval_results = st.session_state.deepeval_results
            
            if deepeval_results:
                # Display the results in a table format
                df = pd.DataFrame(deepeval_results)
                st.dataframe(df, use_container_width=True)
            else:
                st.warning("No DeepEval results available. Please run a JMeter test first.")
        else:
            st.info("No DeepEval results found. Please run a JMeter test first.")
