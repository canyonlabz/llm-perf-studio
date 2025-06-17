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
        /* Main container for horizontal tabs */
        div[data-testid="stVerticalBlockBorderWrapper"] {
            display: flex !important;
            gap: 0 !important;
            padding-left: 2rem !important;
        }
        /* Base tab style */
        a[data-testid="stPageLink-NavLink"] {
            background: #f5f7fa !important;
            border: 1px solid #b0b8c1 !important;
            color: #333 !important;
            text-decoration: none !important;
            border-radius: 8px 8px 0 0 !important;
            margin: 0 -5px !important;
            padding: 1rem 2rem !important;
            position: relative !important;
            z-index: 1 !important;
            transition: all 0.3s ease !important;
            box-shadow: 2px 0 3px rgba(0,0,0,0.1) !important;
        }
        /* Active tab (current page) */
        a[data-testid="stPageLink-NavLink"][aria-current="page"] {
            background: #426cc4 !important; /* darker blue for current tab */
            color: #fff !important;
            border: 1px solid #2b4fa1 !important;
            z-index: 3 !important;
            border-bottom-color: transparent !important;
            box-shadow: 0 -3px 5px rgba(0,0,0,0.1) !important;
        }
        /* Hover state (non-active only) */
        a[data-testid="stPageLink-NavLink"]:not([aria-current="page"]):hover {
            background: #d0e3ff !important;
            border: 1px solid #1976d2;
            box-shadow: 2px 0 3px rgba(0,0,0,0.2) !important;
            transform: translateY(-2px);
        }
        /* Folded corner base effect */
        a[data-testid="stPageLink-NavLink"]::before,
        a[data-testid="stPageLink-NavLink"]::after {
            content: '';
            position: absolute;
            bottom: -1px;
            width: 15px;
            height: 15px;
            background: transparent;
            z-index: 2;
        }
        /* Left corner */
        a[data-testid="stPageLink-NavLink"]::before {
            left: -15px;
            border-bottom-right-radius: 10px;
        }
        /* Right corner */
        a[data-testid="stPageLink-NavLink"]::after {
            right: -15px;
            border-bottom-left-radius: 10px;
        }
        /* Active tab corner overrides */
        a[data-testid="stPageLink-NavLink"][aria-current="page"]::before {
            border-bottom-right-radius: 0;
        }
        a[data-testid="stPageLink-NavLink"][aria-current="page"]::after {
            border-bottom-left-radius: 0;
        }
        /* Text inside nav */
        a[data-testid="stPageLink-NavLink"] p {
            color: #2d5c7f !important;
            font-family: Verdana, Geneva, sans-serif !important;
            font-weight: 600 !important;
            margin: 0 !important;
        }
        </style>
    """, unsafe_allow_html=True)

# --- Page Title Styles ---------------------------------------------------
def inject_page_title_styles():
    """
    Inject custom CSS styles for the page title in the Streamlit app.
    """
    st.markdown("""
        <style>
        .centered-title {
            text-align: center;
            font-size: 3rem;
            font-weight: 800;
            font-family: 'Georgia', serif;
            margin-top: 2rem;
            margin-bottom: 0.5rem;
        }
        .centered-subtitle {
            text-align: center;
            font-size: 1.25rem;
            font-weight: 400;
            color: #3d2b1f;
            margin-bottom: 2rem;
        }
        </style>
    """, unsafe_allow_html=True)

# --- Chatbot Area Styles ---------------------------------------------------
def inject_chatbot_area_styles():
    """
    Inject custom CSS styles for the chatbot area in the Streamlit app.
    """
    st.markdown("""
        <style>
        .chatbot-title {
            font-size: 1.2rem;
            font-weight: bold;
            margin-bottom: 0.5rem;
        }
        .stChatInput {
            border: 2px solid #c95000 !important;
            border-radius: 6px !important;
            background: #f8f6f2 !important;
            margin-top: 0.5rem;
        }
        .st-key-clear_chat button {
            border: 2px solid #c95000;
            color: #c95000;
            background: transparent;
            border-radius: 24px;
            padding: 8px 24px;
            font-weight: bold;
            font-size: 18px;
            float: left;
            margin-top: 10px;
            margin-bottom: 10px;
            transition: background 0.2s, color 0.2s;
        }
        .st-key-clear_chat button:hover {
            background: #c95000;
            color: #fff;
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
