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
from src.ui.page_title import render_jmeter_title  # Importing page body
from src.ui.page_body import (
    render_jmeter_config_area,     # Importing JMeter configuration settings area
    render_jmeter_viewer_area,     # Importing JMeter viewer area and buttons
)

#from src.utils.agent_logs import add_agent_log

# --- Load Configuration -----------------------------------------------------
# This module loads the configuration from config.yaml

module_config = load_config()
general_config = module_config.get("general", {})
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
    render_jmeter_title()   # Render the page body (title, subtitle, etc.)
    render_jmeter_config_area()             # Render the JMeter configuration settings area
    render_jmeter_viewer_area(jmeter_path)  # Render the JMeter viewer and buttons

# --- Main Function ---------------------------------------------------------

if __name__ == "__main__":
    render_ui()

