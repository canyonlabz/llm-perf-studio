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
            border: 1px solid #b0b8c1 !important;   /* light grey border */
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
            border: 1px solid #2b4fa1 !important;   /* darker border for active tab */
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
        .homepage-subtitle {
            font-size: 1.18rem;
            color: #133366; /* dark blue */
            font-weight: 700;
            margin-bottom: 0.2rem;
            letter-spacing: 0.2px;
        }
        .chatbot-title {
            color: #133366; /* dark blue */
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
        /* Shared pill style for all action buttons */
        .st-key-process_rag_btn button,
        .st-key-clear_rag_btn button {
            width: 170px;
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
        .st-key-process_rag_btn button:hover,
        .st-key-clear_rag_btn button:hover {
            background-color: #1a3a4d !important;   /* Darker blue */
            color: #a3cae9; /* Lighter blue */
            border: 2px solid #c95000;
            cursor: pointer;
        }
    
        /* Disabled state */
        .st-key-process_rag_btn button:disabled,
        .st-key-clear_rag_btn button:disabled {
            background-color: #cccccc !important;
            color: #666666 !important;
            border: none !important;
            cursor: not-allowed !important;
        }
        .rag-file-name {
            font-size: 1.05rem;
            font-weight: 600;
            color: #4c4e52; /* Dark grey */
            margin-bottom: 1.25rem;
        }
        </style>
    """, unsafe_allow_html=True)

# --- JMeter Configuration Area Styles ---------------------------------------------------
def inject_jmeter_config_styles():
    """
    Inject custom CSS styles for the JMeter configuration area in the Streamlit app.
    """
    st.markdown("""
        <style>
        .jmeter-config-subtitle {
            font-size: 1.18rem;
            color: #133366; /* dark blue */
            font-weight: 700;
            margin-bottom: 0.2rem;
            letter-spacing: 0.2px;
        }
        /* Number input and select box border styling */
        .stNumberInput input, .stSelectbox div[data-baseweb="select"] {
            border: 1.5px solid #cfd8dc !important;  /* light grey */
            border-radius: 7px !important;
            background-color: #f8fafc !important;
            padding: 0.35rem 0.75rem !important;
            font-size: 1.08rem !important;
        }
        .jmeter-config-label {
            color: #222;           /* Black or near-black for label */
            font-weight: 600;
            font-size: 1.08rem;
            letter-spacing: 0.2px;
        }
        .jmeter-config-value {
            font-size: 1.09rem;
            color: #1976d2;  /* blue-grey for modern look */
            font-weight: 500;
            margin-top: 0.18rem;
        }
        </style>
    """, unsafe_allow_html=True)

# --- JMeter Viewer Styles ---------------------------------------------------
def inject_jmeter_viewer_styles():
    """
    Inject custom CSS styles for the JMeter Viewer in the Streamlit app.
    """
    # Inject custom CSS for styling
    st.markdown("""
        <style>
        *, html {scroll-behavior: smooth !important;}
        .jmeter-viewer-title {
            font-size: 1.2rem;
            font-weight: bold;
            margin-bottom: 0.5rem;
        }
        .st-key-jmeter_viewer_text {
            border: 2px solid #ddd;
            border-radius: 6px;
            border-color: #4c4e52;  /* Dark grey border */
            height: 100%;
        }
        .stTextArea [data-baseweb=base-input] {
            background-color: #e8f4f8 !important;   /* Light blue background */
        }
        .stTextArea textarea {
			font-family: 'Courier New', monospace !important;
            font-size: 14px !important;
            line-height: 1.4 !important;
		}
        .stTextArea textarea[disabled] {
		    color: #000000 !important;
		}
        .test-status {
            padding: 0.5rem;
            border-radius: 4px;
            margin-top: 1rem;
            font-weight: 600;
        }
        .test-status-0 { color: #10B981; } /* NOT_STARTED */
        .test-status-1 { color: #F59E0B; } /* RUNNING */
        .test-status-2 { color: #3B82F6; } /* COMPLETED */
        .test-status-3 { color: #EF4444; } /* FAILED */
        .test-status-4 { color: #8B5CF6; } /* STOPPED */
        </style>
    """, unsafe_allow_html=True)

# --- JMeter Button Styles ---------------------------------------------------
def inject_jmeter_button_styles():
    """
    Inject custom CSS styles for JMeter buttons in the Streamlit app.
    """
    st.markdown("""
        <style>
        /* Base style for all JMeter buttons */
        .st-key-start_jmeter button,
        .st-key-stop_jmeter button,
        .st-key-clear_jmeter_logs button {
            width: 160px;
            height: 44px;
            font-size: 1.08rem;
            font-weight: 600;
            border: 1px solid transparent;
            border-color: #4c4e52;  /* Dark grey border */
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(25, 118, 210, 0.08);
            margin: 0.5rem 0.5rem 0.5rem 0;
            transition: background 0.2s, color 0.2s, box-shadow 0.2s;
            cursor: pointer;
            outline: none;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0.5rem;
        }

        /* Start JMeter button */
        .st-key-start_jmeter button {
            background: #e3f0fc;    /* Light blue background */
            color: #1976d2;         /* Dark blue text */
        }
        .st-key-start_jmeter button:hover {
            background: #1976d2;    /* Dark blue background on hover */
            color: #fff;            /* White text on hover */
            box-shadow: 0 4px 16px rgba(25, 118, 210, 0.16);
            border-color: #cfd8dc; /* Maintain light grey border */
        }

        /* Stop Test button */
        .st-key-stop_jmeter button {
            background: #fde8e8;    /* Light red background */
            color: #d32f2f;         /* Dark red text */
        }
        .st-key-stop_jmeter button:hover {
            background: #d32f2f;    /* Dark red background on hover */
            color: #fff;            /* White text on hover */
            box-shadow: 0 4px 16px rgba(211, 47, 47, 0.16);
        }
                
        /* Clear Logs button */
        .st-key-clear_jmeter_logs {
            margin-top: 20px;  /* Adjust this value as needed */
        }
        .st-key-clear_jmeter_logs button {
            background: #fff8e1;    /* Light orange background */
            color: #b26a00;         /* Dark orange text */
            border: 1px solid #4c4e52;  /* Dark grey border */
            box-shadow: 0 2px 8px rgba(255, 179, 0, 0.08);
        }
        .st-key-clear_jmeter_logs button:hover {
            background: #ffb300;    /* Dark orange background on hover */
            color: #fff;            /* White text on hover */
            box-shadow: 0 4px 16px rgba(255, 179, 0, 0.15);
            border-color: #4c4e52; /* Maintain dark grey border */
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

# --- Report Viewer Styles ---------------------------------------------------
def inject_report_viewer_styles():
    """
    Inject custom CSS styles for the Report Viewer section in the Streamlit app.
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
            font-weight: 100;
            font-size: 28px !important;
            margin-bottom: 0.3em;
        }
        /* Custom styles for tabs */
        .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
            font-size: 1.1rem !important;
        }
        /* Set equal width for all tabs and center content */
        .stTabs [data-baseweb="tab-list"] button {
            flex: 1 !important;                           /* Equal width distribution */
            min-width: 125px !important;                  /* Minimum width for smaller screens */
            max-width: 175px !important;                  /* Maximum width to prevent too wide tabs */
            text-align: center !important;                /* Center text horizontally */
            justify-content: center !important;           /* Center content */
            display: flex !important;                     /* Flex display for centering */
            align-items: center !important;               /* Center content vertically */
            border-radius: 8px 8px 0 0 !important;        /* Rounded top corners */
            margin-right: 1px !important;                 /* Small gap between tabs */
            transition: background-color 0.3s ease, color 0.3s ease !important;
            border: 1px solid #b0b8c1 !important;   /* light grey border */
        }

        /* Center the markdown container content */
        .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] {
            text-align: center !important;
            width: 100% !important;
            display: flex !important;
            justify-content: center !important;
            align-items: center !important;
        }

        /* Center the paragraph text */
        .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
            text-align: center !important;
            margin: 0 !important;                         /* Remove default margins */
            padding: 0 !important;                        /* Remove default padding */
        }                


        /* Inactive tab styling */
        .stTabs [data-baseweb="tab-list"] button[aria-selected="false"] {
            background-color: #f0f2f6 !important;        /* Light grey background */
            color: #666666 !important;                    /* Medium grey text */
            border-bottom: 2px solid transparent !important;
        }

        .stTabs [data-baseweb="tab-list"] button[aria-selected="false"] [data-testid="stMarkdownContainer"] p {
            color: #666666 !important;                    /* Medium grey text for content */
        }

        /* Active tab styling */
        .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
            background-color: #7e99b4 !important;        /* Darker blue grey background */
            color: #ffffff !important;                    /* White text */
            border-bottom: 2px solid #1565c0 !important; /* Darker blue bottom border */
        }

        .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] [data-testid="stMarkdownContainer"] p {
            color: #ffffff !important;                    /* White text for content */
            /* font-weight: bold !important;                  Bold text for active tab */
        }

        /* Hover effects for inactive tabs */
        .stTabs [data-baseweb="tab-list"] button[aria-selected="false"]:hover {
            background-color: #e3f2fd !important;        /* Light blue on hover */
            color: #1976d2 !important;                    /* Blue text on hover */
        }

        .stTabs [data-baseweb="tab-list"] button[aria-selected="false"]:hover [data-testid="stMarkdownContainer"] p {
            color: #1976d2 !important;                    /* Blue text for content on hover */
        }

        /* Optional: Add transition effects for smooth color changes */
        .stTabs [data-baseweb="tab-list"] button {
            transition: background-color 0.3s ease, color 0.3s ease !important;
        }

        /* Report table styles */
        .custom-table {
            width: 100%;
            border-collapse: collapse;
            font-family: 'Source Sans Pro', sans-serif;
            font-size: 14px;
        }
        .custom-table th {
            background-color: #2d5c7f; /* Darker blue */
            color: #ffffff;
            font-weight: bold;
            padding: 12px 8px;
            text-align: left;
            border: 1px solid #000000;
        }
        .custom-table td {
            padding: 10px 8px;
            border: 1px solid #000000;
            background-color: #ffffff;
        }
        .custom-table tr:nth-child(even) td {
            background-color: #f8f9fa;  /* Light gray */
        }
        .custom-table tr:hover td {
            background-color: #e3f2fd;
        }
        /* Report overview section styles */
        .metric_subtitle {
            font-size: 1.2rem;
            border-bottom: 1px solid #e0e0e0; /* Light gray border for separation */
            padding-bottom: 0.25em !important;
            margin-bottom: 0.75em !important;
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
