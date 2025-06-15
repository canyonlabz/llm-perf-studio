import sys
import asyncio
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
import os
from src.utils.config import load_config  # Importing configuration loader

# Initialize agent_logs FIRST before any other imports
#if "agent_logs" not in st.session_state:
#    st.session_state.agent_logs = []

from src.ui.page_header import render_page_header  # Importing page header
from src.ui.page_title import render_page_title  # Importing page body
from src.ui.page_body import (
    render_jmeter_config,  # Importing JMeter configuration
#    render_page_buttons,  # Importing page buttons
#    render_agent_viewer,  # Importing agent automation viewer
#    render_report_viewer  # Importing report viewer
)
from src.ui.page_chatbot_area import render_chatbot_area  # Importing interactive area
#from src.utils.agent_logs import add_agent_log

# --- Load Configuration -----------------------------------------------------
# This module loads the configuration from config.yaml and sets up the LLM model.

# Load the full configuration from config.yaml
module_config = load_config()
general_config = module_config.get("general", {})
# Load specific configurations for LLM and UI
jmeter_config = module_config.get("jmeter", {})
ui_config = module_config.get("user_interface", {})

jmeter_path = jmeter_config.get("jmeter_path", "jmeter")  # Default to 'jmeter' if not specified in config

# --- Render UI ---------------------------------------------------------------

def render_ui():
    """
    Render the main UI for the JMeter configuration page.
    This function sets up the Streamlit page configuration, initializes the navigation,
    and renders the header, title, and JMeter configuration.
    """
    # Set the page configuration for Streamlit
    render_page_header()    # Render the page header
    render_jmeter_config(jmeter_path)  # Render the JMeter configuration

# --- Main Function ---------------------------------------------------------

if __name__ == "__main__":
    render_ui()

