import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
import os

# -- Web Page Header Definitions -----------------------------------------------------------

def render_page_header():
    """
    Render the header of the webpage, including the logo and title.
    """
    # Inject CSS to right-align the button in col3
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
        </style>
    """, unsafe_allow_html=True) 

    col1, col2, col3 = st.columns([0.15, 0.7, 0.15], border=True) # Define three columns with specified widths and borders

    with col1:
        st.image("https://img.freepik.com/free-vector/floating-robot_78370-3669.jpg?t=st=1746392177~exp=1746395777~hmac=b087b344ffeaf82d1a5856d4cc4232c2742c20703b0b4f1bb571c580f0aff3b2&w=740", width=75) # Logo
    
    with col2:
        st.markdown(
            "<div style='display: flex; gap: 40px; align-items: center; margin-top: 0px;'>"
            "<a href='#quickstart' class='nav-link'>Quick Start</a>"
            "<a href='#docs' class='nav-link'>Documentation</a>"
            "<a href='#demo' class='nav-link'>Watch Demo</a>"
            "</div>",
            unsafe_allow_html=True
        ) # Navigation links

    with col3:
        # Exit button with custom CSS class
        exit_clicked = st.button("🚪 Exit App", key="exit_app")
        if exit_clicked:
            print("👋 Goodbye!")
            os._exit(0)
