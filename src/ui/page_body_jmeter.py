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
from src.ui.ui_handlers import (
    handle_start_jmeter_test,
    handle_stop_jmeter_test,
)
from src.ui.page_styles import (
    inject_jmeter_config_styles,     # JMeter configuration styles
    inject_jmeter_viewer_styles,     # JMeter viewer styles
    inject_jmeter_button_styles
)
from src.ui.page_utils import (
    file_selector
)
from src.utils.event_logs import (
    add_jmeter_log,
)
from src.utils.test_state import TestState

config = load_config()  # Load the full configuration from config.yaml
initialize_session_state()  # Initialize all session state variables used across the application

# ============================================================================
# JMeter Page Body: This section contains the main body of the JMeter page.
# It includes the JMeter configuration area, viewer area, and buttons.
# ============================================================================
def get_button_states():
    """
    Get the current states of the JMeter buttons based on the test state.
    Returns a dictionary with the states of the buttons.
    """
    state = st.session_state.jmeter_test_state
    return {
        "start_disabled": state == TestState.RUNNING,
        "stop_disabled": state != TestState.RUNNING,
        "rag_disabled": state == TestState.RUNNING,
        "clear_logs_disabled": state == TestState.RUNNING
    }

def render_jmeter_config_area():
    """
    Render the JMeter configuration area for the webpage.
    """
    inject_jmeter_config_styles()  # Inject custom styles for JMeter configuration

    # Use 6 columns: spacers + 4 button columns + spacers
    col1, col2, col3, col4 = st.columns([0.25, 0.25, 0.25, 0.25], vertical_alignment="top", border=False) # Define six columns with specified widths and borders

    with col1:
        # Top: Subtitle
        st.markdown('<div class="jmeter-config-subtitle">Number of Virtual Users</div>', unsafe_allow_html=True)

        # Middle: Number input for virtual users
        vusers = st.number_input(
            "Number of Virtual Users", 
            key="vusers_input", 
            value=st.session_state.jmeter_state.get("vusers", None), 
            step=1, 
            min_value=None, 
            format="%d",
            help="Enter the number of virtual users for the JMeter test.", 
            placeholder="Enter number...",
            label_visibility="collapsed"
        )
        # Bottom: Virtual user value display
        st.markdown(
            f'<span class="jmeter-config-label">Virtual Users:</span> '
            f'<span class="jmeter-config-value">{vusers if vusers is not None else "None"}</span>',
            unsafe_allow_html=True
        )
        st.session_state.jmeter_state["vusers"] = vusers

    with col2:
        # Top: Subtitle
        st.markdown('<div class="jmeter-config-subtitle">Ramp-Up Period</div>', unsafe_allow_html=True) 

        # Middle: Number input for ramp-up period
        ramp_up = st.number_input(
            "Ramp-Up Period (seconds)", 
            key="ramp_up_input", 
            value=st.session_state.jmeter_state.get("ramp_up", None), 
            step=1, 
            min_value=None, 
            format="%d",
            help="Enter the ramp-up period in seconds for the JMeter test.", 
            placeholder="Enter seconds...",
            label_visibility="collapsed"
        )
        # Bottom: Ramp-Up value display
        st.markdown(
            f'<span class="jmeter-config-label">Ramp-Up Period (sec):</span> '
            f'<span class="jmeter-config-value">{ramp_up if ramp_up is not None else "None"}</span>',
            unsafe_allow_html=True
        )
        st.session_state.jmeter_state["ramp_up"] = ramp_up

    with col3:
        # Top: Subtitle
        st.markdown('<div class="jmeter-config-subtitle">Test Duration</div>', unsafe_allow_html=True)

        # Middle: Number input for test duration
        duration = st.number_input(
            "Test Duration (seconds)", 
            key="duration_input", 
            value=st.session_state.jmeter_state.get("duration", None), 
            step=1, 
            min_value=None, 
            format="%d", 
            help="Enter the test duration in seconds for the JMeter test.",
            placeholder="Enter seconds...",
            label_visibility="collapsed"
        )
        # Bottom: Test duration value display
        st.markdown(
            f'<span class="jmeter-config-label">Test Duration (sec):</span> '
            f'<span class="jmeter-config-value">{duration if duration is not None else "None"}</span>',
            unsafe_allow_html=True
        )
        st.session_state.jmeter_state["duration"] = duration

    with col4:
        # Top: Subtitle
        st.markdown('<div class="jmeter-config-subtitle">Number of Iterations</div>', unsafe_allow_html=True)

        # Middle: Number input for number of iterations
        iterations = st.number_input(
            "Number of Iterations", 
            key="iterations_input", 
            value=st.session_state.jmeter_state.get("iterations", None), 
            step=1, 
            min_value=None, 
            format="%d",
            help="Enter the number of iterations for the JMeter test.", 
            placeholder="Enter iterations...",
            label_visibility="collapsed"
        )
        # Bottom: Number of Iterations value display
        st.markdown(
            f'<span class="jmeter-config-label">Number of Iterations:</span> '
            f'<span class="jmeter-config-value">{iterations if iterations is not None else "None"}</span>',
            unsafe_allow_html=True
        )
        st.session_state.jmeter_state["iterations"] = iterations

def render_jmeter_viewer_area(jmeter_path):
    """
    Render the JMeter test viewer and buttons on the webpage.
    """
    inject_jmeter_viewer_styles()  # Inject custom styles for JMeter viewer
    inject_jmeter_button_styles()  # Inject custom styles for JMeter buttons

    # Get current running state
    test_state = get_button_states()
    start_disabled, stop_disabled, rag_disabled, clear_logs_disabled = (
        test_state["start_disabled"],   # True if test is running (prevents duplicate starts)
        test_state["stop_disabled"],    # Only enabled if test is running
        test_state["rag_disabled"],     # Disabled if test is running (RAG mode toggle)
        test_state["clear_logs_disabled"]  # Disabled if test is running (Clear Logs button)
    )

    # === SYNC BACKGROUND THREAD DATA (ADD HERE) ===
    # Sync background thread data with UI
    shared_data = st.session_state.get("jmeter_thread_data", {})
    
    # Sync logs from background thread
    if shared_data.get('logs'):
        st.session_state['jmeter_logs'].extend(shared_data['logs'])
        shared_data['logs'].clear()

    # Sync status from background thread
    if shared_data.get('status') and st.session_state.jmeter_test_state != shared_data['status']:
        st.session_state.jmeter_test_state = shared_data['status']
        st.rerun()  # Force UI refresh when status changes

    # Sync results from background thread
    if shared_data.get('results'):
        st.session_state.jmeter_state['jmeter_jtl_path'] = shared_data['results'].get('jmeter_jtl_path', "")
        st.session_state.jmeter_state['jmeter_log_path'] = shared_data['results'].get('jmeter_log_path', "")
        shared_data['results'] = None  # Clear after syncing
        
    # Sync analysis results
    if shared_data.get('analysis'):
        st.session_state.jmeter_state['jmeter_test_results'] = shared_data['analysis']
        shared_data['analysis'] = None  # Clear after syncing
    # === END SYNC SECTION ===

    # Centered column for the JMeter page
    col_left, col_viewer, col_right = st.columns([2, 6, 2], border=False)  # Define three columns with specified widths and borders

    with col_left:
        # Select box to select a JMX file
        jmx_filename = file_selector(jmeter_path)   # Call the file selector function to get the JMX file path

        # If a file is uploaded, store it in session state
        if jmx_filename is not None:
            st.session_state.jmeter_state["jmx_path"] = jmx_filename

    with col_viewer:
        # Create the JMeter section
        st.markdown('<div class="jmeter-viewer-title">📊 JMeter Performance Test Viewer</div>', unsafe_allow_html=True)

        # Join all log entries with newlines
        log_text = "\n".join(st.session_state.jmeter_logs) if st.session_state.jmeter_logs else ""
        st.text_area(
            label="JMeter Activity Logs", 
            value=log_text, 
            height=350, 
            key="jmeter_viewer_text", 
            disabled=False,
            label_visibility="collapsed",  # Hides the label visually but keeps it for accessibility
            placeholder="🚀 No JMeter activity yet. Click on an action button to start."  # Placeholder text when no logs are present
        )

    with col_right:
        # Get the number of prompts from the config.yaml file and set it in session state
        if 'jmeter' in config and 'prompt_num' in config['jmeter']:
            st.session_state.jmeter_state["prompt_num"] = config['jmeter']['prompt_num']
        else:
            st.session_state.jmeter_state["prompt_num"] = 1  # Default to 1 if not specified

        # Set the run timestamp in session state (will overwrite on each run)
        st.session_state.jmeter_state["run_timestamp"] = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Button to start the JMeter test
        if st.button("▶️ Start JMeter", 
                disabled=start_disabled,
                help="Start the JMeter performance test with the selected configuration.",
                key="start_jmeter"
            ):
            # Only allow if not already running
            if st.session_state.jmeter_test_state != TestState.RUNNING:
                add_jmeter_log("🏃‍♂️ Starting JMeter load test...", agent_name="JMeterAgent")
                add_jmeter_log("Preparing to execute load test with selected JMX file.", agent_name="JMeterAgent")
                handle_start_jmeter_test()

        # Button to stop the JMeter test
        if st.button("🛑 Stop Test",
                disabled=stop_disabled, 
                help="Stop the currently running JMeter performance test.",
                key="stop_jmeter" 
            ):
            # Only allow if currently running
            if st.session_state.jmeter_test_state == TestState.RUNNING:
                add_jmeter_log("Preparing to stop JMeter load test...", agent_name="JMeterAgent")
                handle_stop_jmeter_test()

        on = st.toggle(
            "RAG Mode",
            value=st.session_state.jmeter_state.get("use_rag", False),  # Default to False if not set
            disabled=rag_disabled,  # Disable if test is running
            key="enable_rag_mode",
            help="Toggle Retrieval Augmented Generation (RAG) mode on or off.",)
        if on:
            st.markdown('<div class="toggle-button-title">🟢 RAG Mode Enabled</div>', unsafe_allow_html=True)
            st.session_state.jmeter_state["use_rag"] = True
        else:
            st.markdown('<div class="toggle-button-title">🔴 RAG Mode Disabled</div>', unsafe_allow_html=True)
            st.session_state.jmeter_state["use_rag"] = False

        # Button to clear JMeter logs
        if st.button("🧹 Clear Logs", 
                disabled=clear_logs_disabled,
                help="Clear all JMeter logs from the viewer.",
                key="clear_jmeter_logs"
            ):
            st.session_state.jmeter_logs = []  # Clear the logs
            add_jmeter_log("🧹 JMeter logs cleared.", agent_name="JMeterAgent")

    # Auto-refresh every 2 seconds for live updates
    st_autorefresh(interval=2000, key="jmeter_autorefresh")
