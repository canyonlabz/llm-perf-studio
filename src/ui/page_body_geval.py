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
# GEval Report Body: This section contains the main body of the GEval report page.
# ============================================================================

def render_geval_report_viewer():
    """
    Render the DeepEval Report Viewer area that displays GEval quality assessment metrics and score.
    """
    ##inject_geval_report_viewer_styles()  # Inject custom styles for report viewer

    # Centered column for the report viewer
    col_left, col_report_viewer, col_right = st.columns([0.10, 0.80, 0.10], border=False)  # Define three columns with specified widths and borders

    with col_report_viewer:
        # Create the report viewer section
        if st.session_state.get('deepeval_state', {}).get('deepeval_test_results'):
            ## TODO: Add variable definitions as needed...

            # Create the report viewer section
            st.markdown('<div class="report-viewer-title">📊 DeepEval Quality Assessment:</div>', unsafe_allow_html=True)
            tab1, tab2, tab3, tab4, tab5 = st.tabs([
                "📋 DeepEval Summary", 
                "📉 DeepEval Results",  
                "📈 Score Chart", 
                "🛠️📈 Quality Analysis", 
                "🛠️📈 Test Cases"])

            with tab1:
                tab1.markdown('<h2 class="tab-subheader">DeepEval Summary</h2>', unsafe_allow_html=True)

            with tab2:
                tab2.markdown('<h2 class="tab-subheader">DeepEval Results</h2>', unsafe_allow_html=True)

            with tab3:
                tab4.markdown('<h2 class="tab-subheader">Score Chart</h2>', unsafe_allow_html=True)

            with tab4:
                tab5.markdown('<h2 class="tab-subheader">Quality Assessment</h2>', unsafe_allow_html=True)

            with tab5:
                tab5.markdown('<h2 class="tab-subheader">Test Cases</h2>', unsafe_allow_html=True)

        else:
            st.info("No DeepEval quality assessment yet. Please run DeepEval first.")

