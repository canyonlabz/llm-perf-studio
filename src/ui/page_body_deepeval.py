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
from src.utils.test_state import TestState, DeepEvalTestState
# Import UI handlers for DeepEval actions
from src.ui.ui_handlers import handle_start_deepeval_assessment

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
    jmeter_state = st.session_state.jmeter_test_state
    deepeval_state = st.session_state.deepeval_test_state

    return {
        "start_deepeval_disabled": (
            str(jmeter_state) != str(TestState.COMPLETED) and 
            str(deepeval_state) != str(DeepEvalTestState.RUNNING)
        ),
        "clear_deepeval_logs_disabled": (
            str(jmeter_state) != str(TestState.COMPLETED) and 
            len(st.session_state.deepeval_logs) == 0
        )
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
        test_state["start_deepeval_disabled"],      # True if test is completed (Start DeepEval button)
        test_state["clear_deepeval_logs_disabled"]  # True if test is completed (Clear Logs button)
    )

    # === SYNC BACKGROUND THREAD DATA (ADD HERE) ===
    # Sync background thread data with UI
    shared_data = st.session_state.get("deepeval_thread_data", {})
    
    # Sync logs from background thread
    if shared_data.get('logs'):
        st.session_state['deepeval_logs'].extend(shared_data['logs'])
        shared_data['logs'].clear()

    # Sync status from background thread
    if shared_data.get('status') and st.session_state.deepeval_test_state != shared_data['status']:
        st.session_state.deepeval_test_state = shared_data['status']
        st.rerun()  # Force UI refresh when status changes

    # Sync results from background thread
    if shared_data.get('results'):
        st.session_state.deepeval_state['llm_responses_path'] = shared_data['results'].get('llm_responses_path', "")
        st.session_state.deepeval_state['deepeval_test_results'] = shared_data['results']
        shared_data['results'] = None  # Clear after syncing
        
    # Sync analysis results
    if shared_data.get('analysis'):
        st.session_state.deepeval_state['deepeval_test_results'] = shared_data['analysis']
        shared_data['analysis'] = None  # Clear after syncing
    # === END SYNC SECTION ===

    # Centered column for the DeepEval viewer
    col_left, col_deepeval_viewer, col_right = st.columns([2, 6, 2], border=False)

    with col_left:
        # Additional validation: Check if DeepEval is currently running
        deepeval_running = st.session_state.deepeval_test_state == DeepEvalTestState.RUNNING
        
        # Additional validation: Check if metrics are selected
        selected_metrics = st.session_state.deepeval_state.get('selected_metrics', [])
        no_metrics_selected = len(selected_metrics) == 0
        
        # Determine final button state
        button_disabled = start_deepeval_disabled or deepeval_running or no_metrics_selected

        # Capture the run timestamp from JMeter state
        run_timestamp = st.session_state.jmeter_state.get("run_timestamp", "")

        # DEBUG:
        #st.write(f"start_deepeval_disabled: {start_deepeval_disabled}")
        #st.write(f"deepeval_running: {deepeval_running}")
        #st.write(f"selected_metrics: {selected_metrics}")
        #st.write(f"no_metrics_selected: {no_metrics_selected}")
        #st.write(f"button_disabled: {button_disabled}")
        #st.write(f'run_timestamp: {st.session_state.jmeter_state.get("run_timestamp", "")}')
        #st.write(f"llm_responses_path: {st.session_state.jmeter_state.get('llm_responses_path', '')}")
        #st.write(f"JMeter test state: {st.session_state.jmeter_test_state}")
        #st.write(f"DeepEval test state: {st.session_state.deepeval_test_state}")
        #st.write(f"JMeter Test State != TestState.COMPLETED: {str(st.session_state.jmeter_test_state) != str(TestState.COMPLETED)}")
        #st.write(f"DeepEval Test Results: {st.session_state.deepeval_state.get('deepeval_test_results', {})}")

        # Button to start the DeepEval quality assessment
        if st.button("▶️ Start DeepEval", 
                disabled=button_disabled,
                help="Start the DeepEval quality assessment with the selected configuration.",
                key="start_deepeval"
            ):

            # Validate prerequisites and log status messages
            if str(st.session_state.jmeter_test_state) == str(TestState.COMPLETED):
                if selected_metrics:
                    # Check for running state
                    if str(st.session_state.deepeval_test_state) == str(DeepEvalTestState.RUNNING):
                        add_deepeval_log("⚠️ DeepEval is already running. Please wait for completion.", agent_name="DeepEvalAgent")
                    else:
                        # Filter to only supported metrics and log status
                        supported_metrics = [m for m in selected_metrics if m == "correctness"]
                        unsupported_metrics = [m for m in selected_metrics if m != "correctness"]
                        
                        if supported_metrics:
                            # Log start messages
                            add_deepeval_log("🏃♂️ Starting DeepEval quality assessment...", agent_name="DeepEvalAgent")
                            
                            if unsupported_metrics:
                                add_deepeval_log(f"⚠️ Skipping unsupported metrics: {', '.join(unsupported_metrics)}", agent_name="DeepEvalAgent")

                            add_deepeval_log(f"✅ Using supported metrics: {', '.join(supported_metrics)}", agent_name="DeepEvalAgent")
                            add_deepeval_log("Preparing to execute DeepEval with selected configuration.", agent_name="DeepEvalAgent")
                            
                            # Update session state with filtered metrics
                            st.session_state.deepeval_state['selected_metrics'] = supported_metrics
                            st.session_state.deepeval_state['run_timestamp'] = run_timestamp  # Capture the run timestamp
                            st.session_state.deepeval_state['llm_responses_path'] = st.session_state.jmeter_state.get('llm_responses_path', "")
                            
                            # Call the handler function
                            handle_start_deepeval_assessment()
                        else:
                            add_deepeval_log("❌ No supported metrics selected. Please select 'correctness' to proceed.", agent_name="DeepEvalAgent")
                else:
                    add_deepeval_log("❌ No metrics selected. Please select at least one quality metric.", agent_name="DeepEvalAgent")
            else:
                add_deepeval_log("❌ JMeter test must be completed before starting DeepEval.", agent_name="DeepEvalAgent")

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