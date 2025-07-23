import sys
import asyncio
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
import os
from src.utils.config import load_config  # Importing configuration loader
from src.ui.page_header import render_page_header  # Importing page header
from src.ui.page_title import render_geval_title  # Importing page body
from src.ui.page_body_geval import (
    render_geval_report_viewer,  # Importing the GEval report viewer
)

# --- Load Configuration -----------------------------------------------------
# This module loads the configuration from config.yaml
module_config = load_config()
general_config = module_config.get("general", {})
ui_config = module_config.get("user_interface", {})

# --- Render UI ---------------------------------------------------------------

def render_ui():
    """
    Render the main UI for the GEval report page.
    This function sets up the Streamlit page configuration, initializes the navigation,
    and renders the header, title, and GEval configuration.
    """
    # Set the page configuration for Streamlit
    render_page_header()        # Render the page header
    render_geval_title()        # Render the page body (title, subtitle, etc.)
    render_geval_report_viewer()  # Render the GEval report viewer

# --- Main Function ---------------------------------------------------------

if __name__ == "__main__":
    render_ui()

