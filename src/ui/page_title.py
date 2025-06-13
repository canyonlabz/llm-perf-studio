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
    st.markdown('<div class="centered-title">LLM Performance Testing Studio</div>', unsafe_allow_html=True)

    # Subtitle/description (centered)
    st.markdown(
        '<div class="centered-subtitle">'
        'A unified interface for benchmarking Large Language Models.<br>'
        'Upload RAG datasets, run automated JMeter tests, and analyze quality—all in one place.'
        '</div>',
        unsafe_allow_html=True
    )
