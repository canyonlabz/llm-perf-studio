# src/ui/page_styles.py

import streamlit as st

# --- Page Header Styles ---------------------------------------------------
def inject_page_header_styles():
    """
    Inject custom CSS styles for the page header in the Streamlit app.
    """
    st.markdown("""
        <style>
        /* Targets the button with key 'exit_app' */
        .st-key-exit_app button {
            border: 2px solid #c95000;
            color: #c95000;
            background: transparent;
            border-radius: 24px;
            padding: 8px 24px;
            font-weight: bold;
            font-size: 18px;
            float: right;
            margin-top: 0px;
            margin-bottom: 10px;
            transition: background 0.2s, color 0.2s;
            white-space: nowrap;  /* Prevent text wrapping */
        }
        .st-key-exit_app button:hover {
            background: #c95000;
            color: #fff;
        }
        .nav-link, .nav-link:link, .nav-link:visited, .nav-link:active {
            text-decoration: none;
            font-weight: bold;
            color: black;
            transition: color 0.2s;
            padding: 0 10px;
        }
        .nav-link:hover {
            color: #c95000; /* orange shade to match your buttons */
            text-decoration: none;
        }
        </style>
    """, unsafe_allow_html=True)

# --- Action Button Styles ---------------------------------------------------
def inject_action_button_styles():
    """
    Inject custom CSS styles for Action buttons (Upload Task File, Run Browser Task, etc) in the Streamlit app.
    """
    st.markdown("""
        <style>
        /* Shared pill style for all action buttons */
        .st-key-upload_task button,
        .st-key-run_browser_task button,
        .st-key-generate_jmx_file button,
        .st-key-run_smoke_test button {
            background-color: #2d5c7f !important; /* Darker blue */
            color: #fff;
            border: none;
            border-radius: 24px;
            padding: 10px 28px;
            font-size: 1.1rem;
            font-weight: bold;
            margin: 0 10px;
            transition: background 0.2s, color 0.2s;
            box-shadow: none;
            outline: none;
            white-space: nowrap;  /* Prevent text wrapping */
        }

        /* Hover: swap background and text color */
        .st-key-upload_task button:hover,
        .st-key-run_browser_task button:hover,
        .st-key-generate_jmx_file button:hover,
        .st-key-run_smoke_test button:hover {
            background-color: #1a3a4d !important;   /* Darker blue */
            color: #a3cae9; /* Lighter blue */
            border: 2px solid #c95000;
            cursor: pointer;
        }
    
        /* Disabled state */
        .st-key-upload_task button:disabled,
        .st-key-run_browser_task button:disabled,
        .st-key-generate_jmx_file button:disabled,
        .st-key-run_smoke_test button:disabled {
            background-color: #cccccc !important;
            color: #666666 !important;
            border: none !important;
            cursor: not-allowed !important;
        }
        .st-key-start_session button:disabled {
            background-color: #666666 !important;
            color: #cccccc !important;
            border: none !important;
        }
        </style>
    """, unsafe_allow_html=True)

# --- The Agent Viewer (Agent Log Activity) Styles ---------------------------------------------------
def inject_agent_viewer_styles():
    """
    Inject custom CSS styles for the Agent Viewer in the Streamlit app.
    """
    # Inject custom CSS for styling
    st.markdown("""
        <style>
        .agent-viewer-title {
            font-size: 1.2rem;
            font-weight: bold;
            margin-bottom: 0.5rem;
        }
        .agent-viewer-textarea {
            border: 2px solid #ddd;
            border-radius: 6px;
            background: #f8f8f8;
            font-family: monospace;
            padding: 10px;
            height: 100%;
        }
        .st-key-start_session button {
            background-color: #2d5c7f !important; /* Darker blue */
            color: #fff;
            border: none;
            border-radius: 24px;
            padding: 10px 28px;
            font-size: 1.1rem;
            font-weight: bold;
            float: right;
            margin: 0 10px;
            transition: background 0.2s, color 0.2s;
            box-shadow: none;
            outline: none;
            white-space: nowrap;
        }
        .st-key-start_session button:hover {
            background-color: #1a3a4d !important;   /* Darker blue */
            color: #a3cae9; /* Lighter blue */
            border: 2px solid #c95000;
            cursor: pointer;
        }
        .st-key-start_session button:disabled {
            background-color: #666666 !important;
            color: #cccccc !important;
            border: none !important;
        }
        .st-key-reset_session button {
            background-color: #2d5c7f !important; /* Darker blue */
            color: #fff;
            border: none;
            border-radius: 24px;
            padding: 10px 28px;
            font-size: 1.1rem;
            font-weight: bold;
            float: left;
            margin: 0 10px;
            transition: background 0.2s, color 0.2s;
            box-shadow: none;
            outline: none;
            white-space: nowrap;
        }
        .st-key-reset_session button:hover {
            background-color: #1a3a4d !important;   /* Darker blue */
            color: #a3cae9; /* Lighter blue */
            border: 2px solid #c95000;
            cursor: pointer;
        }
        .st-key-debug_app button {
            border: 2px solid #c95000;
            color: #c95000;
            background: transparent;
            border-radius: 24px;
            padding: 8px 24px;
            font-weight: bold;
            font-size: 18px;
            float: left;
            margin-top: 0px;
            margin-bottom: 10px;
            transition: background 0.2s, color 0.2s;
            white-space: nowrap;  /* Prevent text wrapping */
        }
        .st-key-debug_app button:hover {
            background: #c95000;
            color: #fff;
        }
        </style>
    """, unsafe_allow_html=True)

# --- Smoke Test Styles ---------------------------------------------------
def inject_report_viewer_styles():
    """
    Inject custom CSS styles for the Smoke Test section in the Streamlit app.
    """
    st.markdown("""
        <style>
        .report-viewer-title {
            font-size: 1.2rem;
            font-weight: bold;
            margin-bottom: 0.5rem;
        }
        .report-viewer-textarea {
            border: 2px solid #ddd;
            border-radius: 6px;
            background: #f8f8f8;
            font-family: monospace;
            padding: 10px;
            height: 100%;
        }
        .tab-subheader {
            color: #2d5c7f !important;  /* Darker blue for subheaders */
            font-weight: 700;
            margin-bottom: 0.5em;
        }
        .stDataFrame thead tr th {      /* Header background navy, text white and bold */
            background-color: #001f3f !important;   
            color: #fff !important;
            font-weight: bold !important;
        }
        .stDataFrame td, .stDataFrame th {
            padding: 12px 8px !important;
        }
        .stDataFrame tbody td, .stDataFrame thead th {  /* Set all borders to black and add padding */
            border: 1px solid #000 !important;
            padding: 10px 8px !important;
        }
        .overview-row {
            font-size: 1.1rem;
            margin-bottom: 0.5em;
        }
        .overview-label {
            font-weight: bold;
            color: #222;    /* Darker text for labels */
            margin-right: 0.5em;
            display: inline-block;
            min-width: 100px;
        }
        .overview-value {
            color: #687494; /* Cooler gray for values */
            font-weight: normal;
        }
        /* Make metric labels larger and bold */
        label[data-testid="stMetricLabel"] p {
            font-size: 1.15rem !important;
            font-weight: 700 !important;
            color: #222 !important;
            margin-bottom: 0.25em;
            letter-spacing: 0.5px;
        }
        /* Change the color of st.metric values */
        div[data-testid="stMetricValue"] {
            color: #687494 !important;
        }
        </style>
    """, unsafe_allow_html=True)
