import altair as alt
import streamlit as st
import streamlit.components.v1 as components
from streamlit_autorefresh import st_autorefresh
from pathlib import Path
import os, sys
from datetime import datetime
import pandas as pd

# Import configuration loader
from src.utils.config import load_config
from src.ui.page_utils import initialize_session_state
from src.ui.page_styles import (
    inject_report_viewer_styles,
)
from src.ui.page_utils import (
    format_duration, 
    format_datetime,
)
from src.utils.event_logs import (
    add_jmeter_log,
    add_deepeval_log,
)
from src.utils.test_state import TestState

config = load_config()      # Load the full configuration from config.yaml
initialize_session_state()  # Initialize all session state variables used across the application

# ============================================================================
# JMeter Report Body: This section contains the main body of the JMeter report page.
# ============================================================================
def render_report_viewer():
    """
    Render the JMeter Report Viewer area that displays JMeter test results.
    """
    inject_report_viewer_styles()  # Inject custom styles for report viewer

    # Centered column for the report viewer
    col_left, col_report_viewer, col_right = st.columns([0.10, 0.80, 0.10], border=False)  # Define three columns with specified widths and borders

    with col_report_viewer:
        # Create the report viewer section
        if st.session_state.get('jmeter_state', {}).get('jmeter_test_results'):
            results = st.session_state["jmeter_state"]["jmeter_test_results"]
            overlay_df = results['overlay_df']  # DataFrame with time, pct90_response, and vusers columns
            duration = results['duration']      # timedelta
            start_time = results['start_time']  # datetime
            end_time = results['end_time']      # datetime

            # If already string, parse to datetime
            if isinstance(start_time, str):
                start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
            if isinstance(end_time, str):
                end_time = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")

            # Format the duration and timestamps
            duration_str = format_duration(duration)
            start_time_str = format_datetime(start_time)
            end_time_str = format_datetime(end_time)

            with st.expander("Expand to see JMeter test results", expanded=False):

                # Create the report viewer section
                st.markdown('<div class="report-viewer-title">📊 JMeter Test Results</div>', unsafe_allow_html=True)
                tab1, tab2, tab3 = st.tabs(["📋 Results Summary", "🗃 Results Table", "📈 Results Chart"])

                with tab1:
                    tab1.markdown('<h2 class="tab-subheader">Results Summary</h2>', unsafe_allow_html=True)
                    # Display the summary of results into 3 sections: 1) Overview, 2) Key Metrics, 3) Pass/Fail Summary
                    # Section 1: Overview
                    st.markdown("### Overview")
                    st.markdown(
                        f'<div class="overview-row"><span class="overview-label">Duration:</span> <span class="overview-value">{duration_str}</span></div>',
                        unsafe_allow_html=True,
                    )
                    st.markdown(
                        f'<div class="overview-row"><span class="overview-label">Start Time:</span> <span class="overview-value">{start_time_str}</span></div>',
                        unsafe_allow_html=True,
                    )
                    st.markdown(
                        f'<div class="overview-row"><span class="overview-label">End Time:</span> <span class="overview-value">{end_time_str}</span></div>',
                        unsafe_allow_html=True,
                    )

                    # Section 2: Key Metrics
                    st.markdown("### Key Metrics")
                    col1, col2, col3, col4 = st.columns(4, border=True)  # Define four columns with borders
                    col1.metric("Max Virtual Users", int(results['vusers_over_time'].max()))
                    col2.metric("Avg. Response Time (ms)", f"{results['avg_response_time']:.2f}")
                    col3.metric("90th % Response Time (ms)", f"{results['pct90_response_time']:.2f}")
                    col4.metric("Error Rate (%)", f"{results['error_rate']:.2f}")

                    # Section 3: Pass/Fail Summary
                    st.markdown("### Pass/Fail Summary")
                    pie_data = pd.DataFrame({
                        'Result': ['Pass', 'Fail'],
                        'Percentage': [results['pass_pct'], results['fail_pct']]
                    })

                    pie_chart = alt.Chart(pie_data).mark_arc(innerRadius=40).encode(
                        theta=alt.Theta(field="Percentage", type="quantitative"),
                        color=alt.Color(field="Result", type="nominal",
                                        scale=alt.Scale(domain=['Pass', 'Fail'], range=['#2ecc40', '#ff4136'])),
                        tooltip=['Result', 'Percentage']
                    ).properties(width=250, height=250)
                    st.altair_chart(pie_chart, use_container_width=False)

                with tab2:
                    tab2.markdown('<h2 class="tab-subheader">Results Table</h2>', unsafe_allow_html=True)
                    tab2.dataframe(results['agg_table'][['label', 'samples', 'errors', 'error_rate', 'avg', 'min', 'max', 'pct90']],use_container_width=True)

                with tab3:
                    tab3.markdown('<h2 class="tab-subheader">Results Chart</h2>', unsafe_allow_html=True)
                    # Create the base chart with time on the x-axis
                    base = alt.Chart(overlay_df).encode(
                        x=alt.X('time:T', axis=alt.Axis(
                            title='Elapsed Time (hh:mm:ss) UTC', titleColor='black', titleFontWeight='bold',
                            grid=True, gridColor='gray', 
                            ticks=True, labelColor='black', labelAngle=45,  # Horizontal labels
                            format='%H:%M:%S'  # <-- This sets military time format
                        ))
                    )

                    # 90th percentile response time line (left Y axis) with points
                    line1 = base.mark_line(color='#5276A7', point=True).encode(
                        y=alt.Y('pct90_response:Q', axis=alt.Axis(
                            title='90th Percentile Response Time (ms)', titleColor='#5276A7', titleFontWeight='bold',
                            grid=True, gridColor='gray',
                            ticks=True, labelColor='#5276A7'
                        ))
                    )

                    # Virtual users line (right Y axis) with points
                    line2 = base.mark_line(color='#F18727', point=True).encode(
                        y=alt.Y('vusers:Q', axis=alt.Axis(
                            title='Virtual Users', titleColor='#F18727', titleFontWeight='bold',
                            grid=False, ticks=True, labelColor='#F18727'
                        ))
                    )

                    # Layer the two lines with independent Y axes
                    layered_chart = alt.layer(line1, line2).resolve_scale(y='independent')

                    st.altair_chart(layered_chart, use_container_width=True)
    
        else:
            st.info("No JMeter test results yet. Please run a JMeter test first.")
