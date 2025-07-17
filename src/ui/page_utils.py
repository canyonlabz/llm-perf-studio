'''
Module for utility functions related to UI pages.
'''
import os
from datetime import datetime
import streamlit as st

from src.ui.page_styles import inject_jmeter_config_styles
from src.utils.test_state import TestState

def initialize_session_state():
    """
    Initialize all Streamlit session state variables used across the application.
    This function should be called once at the beginning of each page to ensure
    all required session state variables are properly initialized.
    """
    # Initialize session state
    if "session_started" not in st.session_state:
        st.session_state.session_started = False
    
    # Initialize the LLM mode in session state if not already present
    if "llm_mode" not in st.session_state:
        st.session_state.llm_mode = "ollama"  # Default LLM model ("ollama" or "openai")
    
    # Initialize the JMeter logs in session state if not already present
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
            "llm_kpis_path": "",        # Path to LLM KPIs file
            "llm_responses_path": "",   # Path to LLM responses file
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
    
    # Initialize JMeter test state
    if "jmeter_test_state" not in st.session_state:
        st.session_state.jmeter_test_state = TestState.NOT_STARTED
    
    # Initialize JMeter thread data for background processing
    if 'jmeter_thread_data' not in st.session_state:
        st.session_state['jmeter_thread_data'] = {
            'logs': [],
            'status': None,
            'results': None,
            'jmeter_jtl_path': "",
            'jmeter_log_path': "",
            "llm_kpis_path": "",        # Path to LLM KPIs file
            "llm_responses_path": "",   # Path to LLM responses file
            'analysis': None,
            'stop_requested': False,
        }

    # Initialize the DeepEval logs in session state if not already present
    if "deepeval_logs" not in st.session_state:
        st.session_state.deepeval_logs = []

def format_duration(duration):
    """
    Function to format a duration into a human-readable string
    Example: timedelta(minutes=5, seconds=30) -> "5 minutes, 30 seconds"
    Assume duration is a timedelta, start_time and end_time are datetime objects
    """
    total_seconds = int(duration.total_seconds())
    minutes, seconds = divmod(total_seconds, 60)
    parts = []
    if minutes > 0:
        parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
    parts.append(f"{seconds} second{'s' if seconds != 1 else ''}")
    return ", ".join(parts)

def format_datetime(dt):
    """
    Function to format a datetime object into a readable string
    Example: datetime(2023, 10, 5, 14, 30) -> "October 5, 2023 14:30:00 UTC"
    """
    # Use '%-d' on Unix, '%#d' on Windows for day without leading zero
    day_format = "%#d" if os.name == "nt" else "%-d"
    return dt.strftime(f"%B {day_format}, %Y %H:%M:%S UTC")

def file_selector(folder_path='.'):
    """
    Function to select a file from a given folder path
    This function lists all files with a .jmx extension in the specified folder
    """
    inject_jmeter_config_styles()  # Inject custom styles for JMeter configuration

    # Get list of JMX files
    filenames = [f for f in os.listdir(folder_path) if f.lower().endswith('.jmx')]
    if not filenames:
        st.warning("No JMX files found in the specified folder.")
        return None

    # Get current selection from session state or if not set set to None
    if 'selected_jmx_file' not in st.session_state:
        st.session_state.selected_jmx_file = None

    # Set default index to the previously selected file if it exists in the list
    default_index = None
    if st.session_state.selected_jmx_file and st.session_state.selected_jmx_file in filenames:
        default_index = filenames.index(st.session_state.selected_jmx_file)

    # Top: Subtitle
    st.markdown('<div class="jmeter-config-subtitle">Select JMX File</div>', unsafe_allow_html=True)

    # Create selectbox with persisted state
    selected_filename = st.selectbox(
        'Select a JMeter JMX file', 
        filenames,
        key='jmx_file_selector',  # Unique key for the selectbox
        index=default_index,
        help="Select a JMX file to load. If no files are found, please ensure you have JMX files in the specified folder.",
        placeholder="Select a JMX file" if filenames else "No JMX files found",
        label_visibility="collapsed"
    )

    # Update session state when selection changes
    if selected_filename and selected_filename != st.session_state.selected_jmx_file:
        st.session_state.selected_jmx_file = selected_filename

    if st.session_state.selected_jmx_file:
        full_path = os.path.join(folder_path, st.session_state.selected_jmx_file)
        st.session_state.jmeter_state.update({
            "jmx_path": full_path,
            "jmx_valid": os.path.exists(full_path)
        })
        st.info(f"Selected file: {selected_filename}")

        # Return the full path of the selected file
        return full_path
    else:
        st.warning("No JMX file selected.")
        return None

