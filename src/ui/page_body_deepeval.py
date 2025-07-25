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
    inject_deepeval_button_styles
)
from src.utils.event_logs import (
    add_deepeval_log,
)
from src.utils.test_state import TestState

config = load_config()      # Load the full configuration from config.yaml
initialize_session_state()  # Initialize session state for the application

# ============================================================================
# DeepEval Body: This section contains the main body of the DeepEval page.
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

def render_deepeval_configuration():
    """
    Render the DeepEval configuration area.
    This function sets up the Streamlit components for configuring the DeepEval parameters.
    """
    col_left, col_center, col_right = st.columns([2, 6, 2], border=False)

    with col_center:
        st.subheader("DeepEval Configuration")

        # Select metrics for evaluation
        selected_metrics = st.multiselect(
            "Select Quality Metrics",
            options=["correctness", "robustness", "relevance", "coherence"],
            default=None,  # Default selection
            help="Choose the quality metrics to evaluate the LLM responses.",
            key="deepeval_selected_metrics",
            placeholder="Select metrics to evaluate",
            label_visibility="collapsed",  # Hide the label for a cleaner look
        )

        # Update session state with selected metrics
        st.session_state.deepeval_state['selected_metrics'] = selected_metrics

        # Log metric selection changes to DeepEval Viewer (only when metrics change)
        previous_metrics = st.session_state.deepeval_state.get('previous_selected_metrics', [])
        if selected_metrics != previous_metrics:
            # Update the previous metrics to avoid duplicate logging
            st.session_state.deepeval_state['previous_selected_metrics'] = selected_metrics
            
            if selected_metrics:
                # Check for unsupported metrics
                unsupported_metrics = [metric for metric in selected_metrics if metric != "correctness"]
                supported_metrics = [metric for metric in selected_metrics if metric == "correctness"]
                
                # Log selected metrics
                add_deepeval_log(f"📋 Metrics selected: {', '.join(selected_metrics)}", agent_name="DeepEvalAgent")
                
                if supported_metrics:
                    add_deepeval_log(f"✅ Supported metrics ready: {', '.join(supported_metrics)}", agent_name="DeepEvalAgent")
                
                if unsupported_metrics:
                    add_deepeval_log(
                        f"⚠️ Unsupported metrics (will be skipped): {', '.join(unsupported_metrics)}", 
                        agent_name="DeepEvalAgent"
                    )
                    add_deepeval_log("💡 Note: Only 'correctness' metric is currently implemented.", agent_name="DeepEvalAgent")
            else:
                add_deepeval_log("📝 No metrics selected. Please select at least one metric to proceed.", agent_name="DeepEvalAgent")

def render_deepeval_viewer():
    """
    Render the DeepEval viewer area.
    This function sets up the Streamlit components for displaying the DeepEval results.
    """
    inject_deepeval_viewer_styles()  # Inject custom styles for the DeepEval viewer
    inject_deepeval_button_styles()  # Inject custom styles for the DeepEval buttons

    # Get current running state
    test_state = get_button_states()
    start_deepeval_disabled, clear_deepeval_logs_disabled = (
        test_state["start_deepeval_disabled"],   # True if test is completed (Start DeepEval button)
        test_state["clear_deepeval_logs_disabled"]  # True if test is completed (Clear Logs button)
    )

    # Centered column for the DeepEval viewer
    col_left, col_deepeval_viewer, col_right = st.columns([2, 6, 2], border=False)

    with col_left:
        # Button to start the DeepEval quality assessment
        if st.button("▶️ Start DeepEval", 
                disabled=start_deepeval_disabled,
                help="Start the DeepEval quality assessment with the selected configuration.",
                key="start_deepeval"
            ):
            # Only allow if the JMeter test state is COMPLETED
            if st.session_state.jmeter_test_state == TestState.COMPLETED:
                add_deepeval_log("🏃‍♂️ Starting DeepEval quality assessment...", agent_name="DeepEvalAgent")
                add_deepeval_log("Preparing to execute DeepEval with selected configuration.", agent_name="DeepEvalAgent")

    # Display the DeepEval results
    with col_deepeval_viewer:
        st.markdown("<div class='deepeval-results-subtitle'>📟 DeepEval Results Viewer</div>", unsafe_allow_html=True)

        # Join all log entries with newlines
        log_text = "\n".join(st.session_state.deepeval_logs) if st.session_state.deepeval_logs else ""
        st.text_area(
            label="DeepEval Activity Logs", 
            value=log_text, 
            height=350, 
            key="deepeval_viewer_text", 
            disabled=False,
            label_visibility="collapsed",  # Hides the label visually but keeps it for accessibility
            placeholder="🚀 No DeepEval activity yet. Please run a JMeter test first then click on an action button to start."  # Placeholder text when no logs are present
        )

    with col_right:
        # Button to clear DeepEval logs
        if st.button("🧹 Clear Logs", 
                disabled=clear_deepeval_logs_disabled,
                help="Clear all DeepEval logs and results.",
                key="clear_deepeval_logs"
            ):
            st.session_state.deepeval_logs = []  # Clear the logs
            add_deepeval_log("🧹 DeepEval logs cleared.", agent_name="DeepEvalAgent")

    # Auto-refresh every 2 seconds for live updates
    st_autorefresh(interval=2000, key="deepeval_autorefresh")