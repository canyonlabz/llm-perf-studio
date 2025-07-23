import altair as alt
import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
import os, sys
from datetime import datetime
import pandas as pd

# Import configuration loader
from src.utils.config import load_config
from src.ui.page_utils import initialize_session_state
from src.ui.page_styles import (
    inject_deepeval_viewer_styles,
    inject_deepeval_button_styles
)
from src.utils.event_logs import (
    add_deepeval_log,
)
from src.utils.test_state import TestState

config = load_config()      # Load the full configuration from config.yaml
initialize_session_state()  # Initialize session state for the application

# ============================================================================
# GEval Body: This section contains the main body of the GEval report page.
# ============================================================================