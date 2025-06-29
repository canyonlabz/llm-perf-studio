import altair as alt
import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
import os, sys
from datetime import datetime
import pandas as pd

# Import configuration loader
from src.utils.config import load_config
##from src.utils.agent_logs import add_agent_log
from src.ui.ui_handlers import (
    handle_start_jmeter_test,
    handle_stop_jmeter_test,
)
from src.ui.page_styles import (
    inject_action_button_styles,
    inject_agent_viewer_styles,
    inject_report_viewer_styles,
    inject_jmeter_config_styles,    # JMeter configuration styles
    inject_jmeter_viewer_styles,     # JMeter viewer styles
    inject_jmeter_button_styles
)
from src.ui.page_utils import (
    format_duration, 
    format_datetime,
    file_selector
)

config = load_config()  # Load the full configuration from config.yaml
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
        "use_rag": False,   # Whether to use RAG mode
        "prompt_num": 1,    # Number of prompts to use from input JSON file
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

# ============================================================================
# JMeter Page Body: This section contains the main body of the JMeter page.
# It includes the JMeter configuration area, viewer area, and buttons.
# ============================================================================
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

        # Create a container with fixed height for real-time logs
        jmeter_container = st.container(height=300, border=True)
        
        # Display all JMeter logs inside the container
        with jmeter_container:
            # Join all log entries with newlines
            if st.session_state.jmeter_logs:
                log_text = "\n".join(st.session_state.jmeter_logs) if st.session_state.jmeter_logs else ""
                st.text_area(
                    label="JMeter Activity Logs", 
                    value=log_text, 
                    height=280, 
                    key="jmeter_viewer_text", 
                    disabled=True,
                    label_visibility="collapsed"  # Hides the label visually but keeps it for accessibility
                )
            else:
                st.info("No JMeter activity yet. Click on an action button to start.")

    with col_right:
        # Get the number of prompts from the config.yaml file and set it in session state
        if 'jmeter' in config and 'prompt_num' in config['jmeter']:
            st.session_state.jmeter_state["prompt_num"] = config['jmeter']['prompt_num']
        else:
            st.session_state.jmeter_state["prompt_num"] = 1  # Default to 1 if not specified

        # Set the run timestamp in session state (will overwrite on each run)
        st.session_state.jmeter_state["run_timestamp"] = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Button to start the JMeter test
        if st.button("▶️ Start JMeter", key="start_jmeter"):
            # Call the function to handle start JMeter test
            handle_start_jmeter_test()

        # Button to stop the JMeter test
        if st.button("🛑 Stop Test", key="stop_jmeter"):
            # Call the function to handle stop JMeter test
            handle_stop_jmeter_test()

        on = st.toggle(
            "RAG Mode",
            value=False,
            key="enable_rag_mode",
            help="Toggle Retrieval Augmented Generation (RAG) mode on or off.",)
        if on:
            st.markdown('<div class="toggle-button-title">🟢 RAG Mode Enabled</div>', unsafe_allow_html=True)
            st.session_state.jmeter_state["use_rag"] = True
        else:
            st.markdown('<div class="toggle-button-title">🔴 RAG Mode Disabled</div>', unsafe_allow_html=True)
            st.session_state.jmeter_state["use_rag"] = False

def render_agent_viewer(ui_config):
    """
    Render the Agent Automation Viewer area that displays agent logs and activities.
    """
    inject_agent_viewer_styles()  # Inject custom styles for agent viewer

    # Enable/disable debug button
    debug_mode = ui_config.get("enable_debug_button", False)  # Default to False if not specified in config

    # Centered column for the chatbot
    col_left, col_viewer, col_right = st.columns([2, 6, 2], border=True)  # Define three columns with specified widths and borders

    with col_viewer:
        # Create the viewer section
        st.markdown('<div class="agent-viewer-title">🤖 Agent Automation Viewer</div>', unsafe_allow_html=True)
        
        # Create a container with fixed height for agent logs
        agent_container = st.container(height=300, border=True)
        
        # Display all agent logs inside the container
        with agent_container:
            # Join all log entries with newlines
            if st.session_state.agent_logs:
                log_text = "\n".join(st.session_state.agent_logs) if st.session_state.agent_logs else ""
                st.text_area(
                    label="Agent Activity Logs", 
                    value=log_text, 
                    height=280, 
                    key="agent_viewer_text", 
                    disabled=True,
                    label_visibility="collapsed"  # Hides the label visually but keeps it for accessibility
                )
            else:
                st.info("No agent activity yet. Click on an action button to start.")

    with col_left:
        # Use a button to start the session
        if st.button("🚀 Start Session", key="start_session", disabled=st.session_state.session_started):
            # Call the function to handle start session
            ##handle_start_session()
            ...  # This is where you would handle the session start logic

    with col_right:
        if st.button("🔄 New Session", key="reset_session"):
            # Call the function to handle reset session
            ##handle_reset_session()
            ...            # Reset the session state

        if debug_mode:
            # Debug button with custom CSS class
            debug_clicked = st.button("🛠️ Debug App", key="debug_app")
            if debug_clicked:
                # Call the function to handle debug test
                ##handle_debug_test()
                ...  # This is where you would handle the debug test logic

# ============================================================================
# JMeter Report Body: This section contains the main body of the JMeter report page.
# ============================================================================
def render_report_viewer():
    """
    Render the JMeter Report Viewer area that displays JMeter test results.
    """
    inject_report_viewer_styles()  # Inject custom styles for report viewer

    # Centered column for the report viewer
    col_left, col_report_viewer, col_right = st.columns([2, 6, 2], border=True)  # Define three columns with specified widths and borders

    with col_report_viewer:
        # Create the report viewer section
        if (
            "jmeter_state" in st.session_state
            and "jmeter_test_results" in st.session_state["jmeter_state"]
            and st.session_state["jmeter_state"]["jmeter_test_results"]
        ):
            results = st.session_state["jmeter_state"]["jmeter_test_results"]
            overlay_df = results['overlay_df']  # DataFrame with time, pct90_response, and vusers columns
            duration = results['duration']  # timedelta
            start_time = results['start_time']  # datetime
            end_time = results['end_time']  # datetime

            # If already string, parse to datetime
            if isinstance(start_time, str):
                start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
            if isinstance(end_time, str):
                end_time = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")

            # Format the duration and timestamps
            duration_str = format_duration(duration)
            start_time_str = format_datetime(start_time)
            end_time_str = format_datetime(end_time)

            with st.expander("Expand to see JMeter test results", expanded=False):

                # Create the report viewer section
                st.markdown('<div class="report-viewer-title">📊 JMeter Test Results</div>', unsafe_allow_html=True)
                tab1, tab2, tab3 = st.tabs(["📋 Results Summary", "🗃 Results Table", "📈 Results Chart"])

                with tab1:
                    tab1.markdown('<h2 class="tab-subheader">Results Summary</h2>', unsafe_allow_html=True)
                    # Display the summary of results into 3 sections: 1) Overview, 2) Key Metrics, 3) Pass/Fail Summary
                    # Section 1: Overview
                    st.markdown("### Overview")
                    st.markdown(
                        f'<div class="overview-row"><span class="overview-label">Duration:</span> <span class="overview-value">{duration_str}</span></div>',
                        unsafe_allow_html=True,
                    )
                    st.markdown(
                        f'<div class="overview-row"><span class="overview-label">Start Time:</span> <span class="overview-value">{start_time_str}</span></div>',
                        unsafe_allow_html=True,
                    )
                    st.markdown(
                        f'<div class="overview-row"><span class="overview-label">End Time:</span> <span class="overview-value">{end_time_str}</span></div>',
                        unsafe_allow_html=True,
                    )

                    # Section 2: Key Metrics
                    st.markdown("### Key Metrics")
                    col1, col2, col3, col4 = st.columns(4, border=True)  # Define four columns with borders
                    col1.metric("Max Virtual Users", int(results['vusers_over_time'].max()))
                    col2.metric("Avg. Response Time (ms)", f"{results['avg_response_time']:.2f}")
                    col3.metric("90th % Response Time (ms)", f"{results['pct90_over_time'].max():.2f}")
                    col4.metric("Error Rate (%)", f"{results['error_rate']:.2f}")

                    # Section 3: Pass/Fail Summary
                    st.markdown("### Pass/Fail Summary")
                    pie_data = pd.DataFrame({
                        'Result': ['Pass', 'Fail'],
                        'Percentage': [results['pass_pct'], results['fail_pct']]
                    })

                    pie_chart = alt.Chart(pie_data).mark_arc(innerRadius=40).encode(
                        theta=alt.Theta(field="Percentage", type="quantitative"),
                        color=alt.Color(field="Result", type="nominal",
                                        scale=alt.Scale(domain=['Pass', 'Fail'], range=['#2ecc40', '#ff4136'])),
                        tooltip=['Result', 'Percentage']
                    ).properties(width=250, height=250)
                    st.altair_chart(pie_chart, use_container_width=False)

                with tab2:
                    tab2.markdown('<h2 class="tab-subheader">Results Table</h2>', unsafe_allow_html=True)
                    tab2.dataframe(results['agg_table'][['label', 'samples', 'errors', 'error_rate', 'avg', 'min', 'max', 'pct90']],use_container_width=True)

                with tab3:
                    tab3.markdown('<h2 class="tab-subheader">Results Chart</h2>', unsafe_allow_html=True)
                    # Create the base chart with time on the x-axis
                    base = alt.Chart(overlay_df).encode(
                        x=alt.X('time:T', axis=alt.Axis(
                            title='Elapsed Time (hh:mm:ss) UTC', titleColor='black', titleFontWeight='bold',
                            grid=True, gridColor='gray', 
                            ticks=True, labelColor='black', labelAngle=45,  # Horizontal labels
                            format='%H:%M:%S'  # <-- This sets military time format
                        ))
                    )

                    # 90th percentile response time line (left Y axis) with points
                    line1 = base.mark_line(color='#5276A7', point=True).encode(
                        y=alt.Y('pct90_response:Q', axis=alt.Axis(
                            title='90th Percentile Response Time (ms)', titleColor='#5276A7', titleFontWeight='bold',
                            grid=True, gridColor='gray',
                            ticks=True, labelColor='#5276A7'
                        ))
                    )

                    # Virtual users line (right Y axis) with points
                    line2 = base.mark_line(color='#F18727', point=True).encode(
                        y=alt.Y('vusers:Q', axis=alt.Axis(
                            title='Virtual Users', titleColor='#F18727', titleFontWeight='bold',
                            grid=False, ticks=True, labelColor='#F18727'
                        ))
                    )

                    # Layer the two lines with independent Y axes
                    layered_chart = alt.layer(line1, line2).resolve_scale(y='independent')

                    st.altair_chart(layered_chart, use_container_width=True)
