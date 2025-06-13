import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
import os

#--- Page Title and Sub-Title -------------------------------------------------------
def render_page_title():
    """
    Render the title and subtitle of the webpage.
    """
    # Inject custom CSS for centering and font styling
    st.markdown("""
    <style>
    .centered-title {
        text-align: center;
        font-size: 3rem;
        font-weight: 800;
        font-family: 'Georgia', serif;
        margin-top: 2rem;
        margin-bottom: 0.5rem;
    }
    .centered-subtitle {
        text-align: center;
        font-size: 1.25rem;
        font-weight: 400;
        color: #3d2b1f;
        margin-bottom: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

    # Main title (centered, bold)
    st.markdown('<div class="centered-title">JMeter AI Agent Framework</div>', unsafe_allow_html=True)

    # Subtitle/description (centered)
    st.markdown(
        '<div class="centered-subtitle">'
        'Experience the power of AI-driven performance testing with our user-friendly interface. '
        'Build your scripts with ease and efficiency.'
        '</div>',
        unsafe_allow_html=True
    )
