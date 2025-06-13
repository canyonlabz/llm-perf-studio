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
if "agent_logs" not in st.session_state:
    st.session_state.agent_logs = []

from src.ui.page_header import render_page_header  # Importing page header
from src.ui.page_title import render_page_title  # Importing page body
from src.ui.page_body import (
    render_page_buttons,  # Importing page buttons
    render_agent_viewer,  # Importing agent automation viewer
    render_report_viewer  # Importing report viewer
)
from src.ui.page_chatbot_area import render_chatbot_area  # Importing interactive area
from src.utils.agent_logs import add_agent_log

# Load the full configuration from config.yaml
module_config = load_config()
config = module_config.get("general", {})
ui_config = module_config.get("user_interface", {})

# Define the LLM model to use.
model = config.get("model", "gpt-4o-mini")  # Default to gpt-4o-mini if not specified in config

# --- Render UI ---------------------------------------------------------------

def render_ui():
    st.set_page_config(page_title="JMeter AI-Agent Framework", layout="wide")
    render_page_header()  # Render the page header
    render_page_title()  # Render the page body (title, subtitle, etc.)
    render_page_buttons()  # Render the page buttons
    render_agent_viewer(ui_config)  # Render the agent automation viewer
    render_report_viewer()  # Render the report viewer
    if ui_config.get("enable_chatbot", False):
        render_chatbot_area(llm_model=model)  # Render the chatbot area

# --- Main Function ---------------------------------------------------------

if __name__ == "__main__":
    render_ui()

