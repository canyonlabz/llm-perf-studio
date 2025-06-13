import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
import os

from src.ui.page_styles import (
    inject_page_header_styles # Importing custom styles for the page header
)

# -- Web Page Header Definitions -----------------------------------------------------------

def render_page_header():
    """
    Render the header of the webpage, including the logo and title.
    """
    # Inject custom styles for the page header
    inject_page_header_styles()  # Apply custom styles for the header

    # Define the header layout with three columns
    col1, col2, col3 = st.columns([0.15, 0.7, 0.15]) # Define three columns with specified widths and borders

    with col1:
        st.image("https://img.freepik.com/free-vector/floating-robot_78370-3669.jpg?t=st=1746392177~exp=1746395777~hmac=b087b344ffeaf82d1a5856d4cc4232c2742c20703b0b4f1bb571c580f0aff3b2&w=740", width=75) # Logo
    
    with col2:
        st.markdown(
            "<div style='display: flex; gap: 40px; align-items: center; margin-top: 0px;'>"
            "<a href='#quickstart' class='nav-link'>Home</a>"
            "<a href='#docs' class='nav-link'>JMeter</a>"
            "<a href='#demo' class='nav-link'>DeepEval</a>"
            "</div>",
            unsafe_allow_html=True
        ) # Navigation links

    with col3:
        # Exit button with custom CSS class
        exit_clicked = st.button("🚪 Exit App", key="exit_app")
        if exit_clicked:
            print("👋 Goodbye!")
            os._exit(0)

    st.divider()
