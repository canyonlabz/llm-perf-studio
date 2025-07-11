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
from src.ui.page_title import render_homepage_title  # Importing page body
from src.ui.page_body_homepage import render_chatbot_area  # Importing interactive area

# --- Load Configuration -----------------------------------------------------
# This module loads the configuration from config.yaml
module_config = load_config()
general_config = module_config.get("general", {})
llm_config = module_config.get("llm", {})
ui_config = module_config.get("user_interface", {})

# --- Render UI ---------------------------------------------------------------

def render_ui():
    """
    Render the main UI for the homepage.
    This function sets up the Streamlit page configuration, initializes the navigation,
    and renders the header, title, and interactive area.
    """
    # Set the page configuration for Streamlit
    render_page_header()        # Render the page header
    render_homepage_title()     # Render the page body (title, subtitle, etc.)
    render_chatbot_area()  # Render the chatbot area

# --- Main Function ---------------------------------------------------------

if __name__ == "__main__":
    render_ui()

