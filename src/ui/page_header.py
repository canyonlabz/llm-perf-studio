import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
import os

# Importing custom styles for the page header
from src.ui.page_styles import inject_page_header_styles 

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
        tab_col1, tab_col2, tab_col3, tab_col4, tab_col5 = st.columns([0.13, 0.14, 0.15, 0.15, 0.43], border=False) # Define four columns for navigation tabs
        with tab_col1:
            st.page_link("nav_pages/page_homepage.py", label="Home", icon="🏠")
        with tab_col2:
            st.page_link("nav_pages/page_jmeter.py", label="JMeter", icon="📊")
        with tab_col3:
            st.page_link("nav_pages/page_deepeval.py", label="DeepEval", icon="📈")
        with tab_col4:
            st.page_link("nav_pages/page_report.py", label="Report", icon="📋")
        
    with col3:
        # Exit button with custom CSS class
        exit_clicked = st.button("🚪 Exit App", key="exit_app")
        if exit_clicked:
            print("👋 Goodbye!")
            os._exit(0)

    st.divider()
