import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
import os

from src.ui.page_styles import inject_page_title_styles

#--- Page Titles and Sub-Titles -------------------------------------------------------
def render_homepage_title():
    """
    Render the title and subtitle of the webpage.
    """
    # Inject custom CSS for centering and font styling
    inject_page_title_styles()

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

def render_jmeter_title():
    """
    Render the title and subtitle for the JMeter configuration page.
    """
    # Inject custom CSS for centering and font styling
    inject_page_title_styles()

    # Main title (centered, bold)
    st.markdown('<div class="centered-title">JMeter Configuration</div>', unsafe_allow_html=True)

    # Subtitle/description (centered)
    st.markdown(
        '<div class="centered-subtitle">'
        'Configure JMeter for performance testing.<br>'
        'Set up your JMeter environment and run tests seamlessly.'
        '</div>',
        unsafe_allow_html=True
    )

def render_report_title():
    """ Render the title and subtitle for the report page. """
    # Inject custom CSS for centering and font styling
    inject_page_title_styles()

    # Main title (centered, bold)
    st.markdown('<div class="centered-title">LLM Performance Test Report</div>', unsafe_allow_html=True)

    # Subtitle/description (centered)
    st.markdown(
        '<div class="centered-subtitle">'
        'View and analyze the results of your LLM performance tests.<br>'
        'Gain insights into LLM system behavior and identify bottlenecks or quality issues in your models.'
        '</div>',
        unsafe_allow_html=True
    )

def render_deepeval_title():
    """
    Render the title and subtitle for the DeepEval page.
    """
    # Inject custom CSS for centering and font styling
    inject_page_title_styles()

    # Main title (centered, bold)
    st.markdown('<div class="centered-title">DeepEval Configuration</div>', unsafe_allow_html=True)

    # Subtitle/description (centered)
    st.markdown(
        '<div class="centered-subtitle">'
        'Configure DeepEval for model evaluation.<br>'
        'Set up your evaluation parameters and analyze LLM output with ease.'
        '</div>',
        unsafe_allow_html=True
    )

def render_geval_title():
    """
    Render the title and subtitle for the DeepEval report page based upon the GEval metric.
    """
    # Inject custom CSS for centering and font styling
    inject_page_title_styles()

    # Main title (centered, bold)
    st.markdown('<div class="centered-title">DeepEval Quality Report (GEval)</div>', unsafe_allow_html=True)

    # Subtitle/description (centered)
    st.markdown(
        '<div class="centered-subtitle">'
        'View and analyze the quality of your LLM responses using the GEval metric.<br>'
        'Gain insights into the quality of LLM responses under various load conditions.'
        '</div>',
        unsafe_allow_html=True
    )