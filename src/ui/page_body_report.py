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
from src.utils.test_state import TestState, DeepEvalTestState

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

            # Create the report viewer section
            st.markdown('<div class="report-viewer-title">📊 Performance Test Results</div>', unsafe_allow_html=True)
            tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
                "📋 Results Summary", 
                "📉 Results Table",  
                "📈 Results Chart", 
                "🛠️📈 TTFT", 
                "🛠️📈 TPOT", 
                "🛠️📈 TPS"])

            with tab1:
                tab1.markdown('<h2 class="tab-subheader">Results Summary</h2>', unsafe_allow_html=True)
                # Display the summary of results into 3 sections: 1) Overview, 2) Key Metrics, 3) Pass/Fail Summary
                # Section 1: Overview
                st.markdown('<h4 class="metric_subtitle">Overview</h4>', unsafe_allow_html=True)
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
                st.markdown('<h4 class="metric_subtitle">Key Metrics</h4>', unsafe_allow_html=True)
                col1, col2, col3, col4 = st.columns(4, border=True)  # Define four columns with borders
                col1.metric("Max Virtual Users", int(results['vusers_over_time'].max()))
                col2.metric("Avg. Response Time (ms)", f"{results['avg_response_time']:.2f}")
                col3.metric("90th % Response Time (ms)", f"{results['pct90_response_time']:.2f}")
                col4.metric("Error Rate (%)", f"{results['error_rate']:.2f}")

                # Section 3: Pass/Fail Summary
                st.markdown('<h4 class="pass-fail-summary">Pass/Fail Summary</h4>', unsafe_allow_html=True)
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

                # Convert DataFrame to HTML with custom styling
                df_subset = results['agg_table'][['label', 'samples', 'errors', 'error_rate', 'avg', 'min', 'max', 'pct90']].copy()
                
                # Rename columns for display
                df_subset.columns = [
                    'API Endpoint', 'Total Requests', 'Failed Requests', 'Error Rate (%)', 
                    'Avg Response Time (ms)', 'Min Response Time (ms)', 
                    'Max Response Time (ms)', '90th Percentile (ms)'
                ]

                # Format numeric columns
                df_subset['Error Rate (%)'] = df_subset['Error Rate (%)'].apply(lambda x: f"{x:.2f}%")
                df_subset['Avg Response Time (ms)'] = df_subset['Avg Response Time (ms)'].apply(lambda x: f"{x:.2f}")
                df_subset['Min Response Time (ms)'] = df_subset['Min Response Time (ms)'].apply(lambda x: f"{x:.2f}")
                df_subset['Max Response Time (ms)'] = df_subset['Max Response Time (ms)'].apply(lambda x: f"{x:.2f}")
                df_subset['90th Percentile (ms)'] = df_subset['90th Percentile (ms)'].apply(lambda x: f"{x:.2f}")
                
                # Convert to HTML with custom CSS
                html_table = df_subset.to_html(index=False, escape=False, classes='custom-table')
                st.markdown(html_table, unsafe_allow_html=True)

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

            with tab4:
                tab4.markdown('<h2 class="tab-subheader">Time To First Token (TTFT)</h2>', unsafe_allow_html=True)
                # Display the summary of LLM results
                if results.get('has_llm_data', False):
                    try:
                        ttft_data = results['llm_kpi_data']['ttft_overlay_df']
                        
                        if ttft_data is not None and not ttft_data.empty:
                            # Create individual charts first
                            # Create the base chart with time on the x-axis (matching Tab 3)
                            base = alt.Chart(ttft_data).encode(
                                x=alt.X('time:T', axis=alt.Axis(
                                    title='Elapsed Time (hh:mm:ss) UTC', titleColor='black', titleFontWeight='bold',
                                    grid=True, gridColor='gray', 
                                    ticks=True, labelColor='black', labelAngle=45,
                                    format='%H:%M:%S'  # Military time format matching Tab 3
                                ))
                            )

                            # TTFT line (left Y axis) with points - using blue color
                            line1 = base.mark_line(color='#1f77b4', point=True).encode(  # Sea Green for TTFT
                                y=alt.Y('ttft:Q', axis=alt.Axis(
                                    title='Time to First Token (ms)', titleColor='#1f77b4', titleFontWeight='bold',
                                    grid=True, gridColor='gray',
                                    ticks=True, labelColor='#1f77b4'
                                ))
                            )

                            # Virtual users line (right Y axis) with points - matching Tab 3 orange
                            line2 = base.mark_line(color='#F18727', point=True).encode(
                                y=alt.Y('vusers:Q', axis=alt.Axis(
                                    title='Virtual Users', titleColor='#F18727', titleFontWeight='bold',
                                    grid=False, ticks=True, labelColor='#F18727'
                                ))
                            )
                            
                            # Layer the charts with proper dual Y-axis configuration
                            combined_chart = alt.layer(line1, line2).resolve_scale(
                                y='independent'
                            )
                            
                            st.altair_chart(combined_chart, use_container_width=True)
                            
                            # Add summary statistics
                            st.markdown("<h4 class='metric_subtitle'>TTFT Summary Statistics:</h4>", unsafe_allow_html=True)
                            col1, col2, col3, col4 = st.columns(4, border=True)
                            with col1:
                                st.metric("Avg TTFT", f"{results.get('llm_ttft_avg', 0):.0f} ms")
                            with col2:
                                st.metric("Min TTFT", f"{results.get('llm_ttft_min', 0):.0f} ms")
                            with col3:
                                st.metric("Max TTFT", f"{results.get('llm_ttft_max', 0):.0f} ms")
                            with col4:
                                st.metric("90th % TTFT", f"{results.get('llm_ttft_90th', 0):.0f} ms")
                        else:
                            st.warning("TTFT data is empty or unavailable")
                            
                    except KeyError as e:
                        st.error(f"Missing data key: {e}")
                        st.info("Ensure LLM metrics analysis completed successfully")
                    except Exception as e:
                        st.error(f"Error rendering TTFT chart: {str(e)}")
                        
                else:
                    st.info("🤖 LLM performance metrics not available.")

            with tab5:
                tab5.markdown('<h2 class="tab-subheader">Time Per Output Token (TPOT)</h2>', unsafe_allow_html=True)
                # Display the LLM results table if available
                if results.get('has_llm_data', False):
                    try:
                        tpot_data = results['llm_kpi_data']['tpot_overlay_df']
                        
                        if tpot_data is not None and not tpot_data.empty:
                            # Create the base chart with time on the x-axis (matching Tab 3)
                            base = alt.Chart(tpot_data).encode(
                                x=alt.X('time:T', axis=alt.Axis(
                                    title='Elapsed Time (hh:mm:ss) UTC', titleColor='black', titleFontWeight='bold',
                                    grid=True, gridColor='gray', 
                                    ticks=True, labelColor='black', labelAngle=45,
                                    format='%H:%M:%S'  # Military time format matching Tab 3
                                ))
                            )

                            # TPOT line (left Y axis) with points - using deep blue color
                            line1 = base.mark_line(color='#1f77b4', point=True).encode(  # Deep Blue for TPOT
                                y=alt.Y('tpot:Q', axis=alt.Axis(
                                    title='Time per Output Token (ms)', titleColor='#1f77b4', titleFontWeight='bold',
                                    grid=True, gridColor='gray',
                                    ticks=True, labelColor='#1f77b4'
                                ))
                            )

                            # Virtual users line (right Y axis) with points - matching Tab 3 orange
                            line2 = base.mark_line(color='#F18727', point=True).encode(
                                y=alt.Y('vusers:Q', axis=alt.Axis(
                                    title='Virtual Users', titleColor='#F18727', titleFontWeight='bold',
                                    grid=False, ticks=True, labelColor='#F18727'
                                ))
                            )

                            # Layer the two lines with independent Y axes
                            layered_chart = alt.layer(line1, line2).resolve_scale(y='independent')

                            st.altair_chart(layered_chart, use_container_width=True)
                            
                            # Summary statistics
                            st.markdown("<h4 class='metric_subtitle'>TPOT Summary Statistics:</h4>", unsafe_allow_html=True)
                            col1, col2, col3, col4 = st.columns(4, border=True)
                            with col1:
                                st.metric("Avg TPOT", f"{results.get('llm_tpot_avg', 0):.0f} ms")
                            with col2:
                                st.metric("Min TPOT", f"{results.get('llm_tpot_min', 0):.0f} ms")
                            with col3:
                                st.metric("Max TPOT", f"{results.get('llm_tpot_max', 0):.0f} ms")
                            with col4:
                                st.metric("90th % TPOT", f"{results.get('llm_tpot_90th', 0):.0f} ms")
                        else:
                            st.warning("TPOT data is empty or unavailable")
                    except Exception as e:
                        st.error(f"Error rendering TPOT chart: {str(e)}")
                else:
                    st.info("🤖 LLM performance metrics not available.")

            with tab6:
                    tab6.markdown('<h2 class="tab-subheader">Tokens Per Second (TPS)</h2>', unsafe_allow_html=True)
                    # Create a chart for LLM results if available
                    if results.get('has_llm_data', False):
                        try:
                            tps_data = results['llm_kpi_data']['tps_overlay_df']
                            
                            if tps_data is not None and not tps_data.empty:
                                # Create the base chart with time on the x-axis (matching Tab 3)
                                base = alt.Chart(tps_data).encode(
                                    x=alt.X('time:T', axis=alt.Axis(
                                        title='Elapsed Time (hh:mm:ss) UTC', titleColor='black', titleFontWeight='bold',
                                        grid=True, gridColor='gray', 
                                        ticks=True, labelColor='black', labelAngle=45,
                                        format='%H:%M:%S'  # Military time format matching Tab 3
                                    ))
                                )

                                # TPS line (left Y axis) with points - using crimson color
                                line1 = base.mark_line(color='#1f77b4', point=True).encode(  # Crimson for TPS
                                    y=alt.Y('tps:Q', axis=alt.Axis(
                                        title='Tokens Per Second', titleColor='#1f77b4', titleFontWeight='bold',
                                        grid=True, gridColor='gray',
                                        ticks=True, labelColor='#1f77b4'
                                    ))
                                )

                                # Virtual users line (right Y axis) with points - matching Tab 3 orange
                                line2 = base.mark_line(color='#F18727', point=True).encode(
                                    y=alt.Y('vusers:Q', axis=alt.Axis(
                                        title='Virtual Users', titleColor='#F18727', titleFontWeight='bold',
                                        grid=False, ticks=True, labelColor='#F18727'
                                    ))
                                )

                                # Layer the two lines with independent Y axes
                                layered_chart = alt.layer(line1, line2).resolve_scale(y='independent')

                                st.altair_chart(layered_chart, use_container_width=True)
                                
                                # Summary statistics
                                st.markdown("<h4 class='metric_subtitle'>TPS Summary Statistics:</h4>", unsafe_allow_html=True)
                                col1, col2, col3, col4 = st.columns(4, border=True)
                                with col1:
                                    st.metric("Avg TPS", f"{results.get('llm_tps_avg', 0):.1f}")
                                with col2:
                                    st.metric("Min TPS", f"{results.get('llm_tps_min', 0):.1f}")
                                with col3:
                                    st.metric("Max TPS", f"{results.get('llm_tps_max', 0):.1f}")
                                with col4:
                                    st.metric("90th % TPS", f"{results.get('llm_tps_90th', 0):.1f}")
                            else:
                                st.warning("TPS data is empty or unavailable")
                        except Exception as e:
                            st.error(f"Error rendering TPS chart: {str(e)}")
                    else:
                        st.info("🤖 LLM performance metrics not available.")

        else:
            st.info("No JMeter test results yet. Please run a JMeter test first.")
