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
    inject_report_viewer_styles,
)
from src.utils.event_logs import (
    add_deepeval_log,
)
from src.utils.test_state import TestState, DeepEvalTestState

config = load_config()      # Load the full configuration from config.yaml
initialize_session_state()  # Initialize session state for the application

# ============================================================================
# GEval Report Body: This section contains the main body of the GEval report page.
# ============================================================================

def render_geval_report_viewer():
    """
    Render the DeepEval Report Viewer area that displays GEval quality assessment metrics and score.
    """
    inject_report_viewer_styles()  # Inject custom styles for report viewer

    # Centered column for the report viewer
    col_left, col_report_viewer, col_right = st.columns([0.10, 0.80, 0.10], border=False)  # Define three columns with specified widths and borders

    with col_report_viewer:
        # Create the report viewer section
        if st.session_state.get('deepeval_state', {}).get('deepeval_test_results'):
            # Extract latest DeepEval analysis dict  and unpack all needed analysis keys once
            analysis = st.session_state.get('deepeval_state', {}).get('deepeval_test_results', {})
            summary = analysis.get('summary', {})
            detailed = analysis.get('detailed_results', [])
            distribution = analysis.get('score_distribution', {})
            insights = analysis.get('quality_insights', {})
            cases = analysis.get('individual_cases', [])
            execm = insights.get('execution_metrics', {})

            # Create the report viewer section
            st.markdown('<div class="report-viewer-title">📊 DeepEval Quality Assessment:</div>', unsafe_allow_html=True)
            tab1, tab2, tab3, tab4, tab5 = st.tabs([
                "📋 DeepEval Summary", 
                "📉 DeepEval Results",  
                "📈 Score Chart", 
                "🛠️📈 Quality Analysis", 
                "🛠️📈 Test Cases"])

            with tab1:
                tab1.markdown('<h2 class="tab-subheader">DeepEval Results Summary</h2>', unsafe_allow_html=True)
                # Display the summary of results into 3 sections: 1) Overview, 2) Key Metrics, 3) Pass/Fail Summary
                # Section 1: Overview
                st.markdown('<h4 class="metric_subtitle">Overview</h4>', unsafe_allow_html=True)
                st.markdown(
                    f'<div class="overview-row"><span class="overview-label">Total Questions:</span> <span class="overview-value">{summary.get("total_questions", 0)}</span></div>',
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f'<div class="overview-row"><span class="overview-label">Passes:</span> <span class="overview-value">{summary.get("pass_count", 0)}</span></div>',
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f'<div class="overview-row"><span class="overview-label">Fails:</span> <span class="overview-value">{summary.get("fail_count", 0)}</span></div>',
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f'<div class="overview-row"><span class="overview-label">Mean G-Eval Score:</span> <span class="overview-value">{summary.get("average_score", 0):.2f}</span></div>',
                    unsafe_allow_html=True,
                )

                # Section 2: Key Metrics
                st.markdown('<h4 class="metric_subtitle">Key Metrics</h4>', unsafe_allow_html=True)
                col1, col2, col3, col4 = st.columns(4, border=True)  # Define four columns with borders
                col1.metric("Pass Rate (%)", f"{summary['overall_pass_rate']:.2f}")
                col2.metric("Assessment Duration (sec)", f"{execm.get('total_duration', 0):.1f}")
                col3.metric("Avg Duration per Case (sec)", f"{execm.get('average_duration_per_case', 0):.2f}")
                col4.metric("Total Cost", f"${execm.get('total_cost', 0):.2f}")

                # Section 3: Pass/Fail Summary
                st.markdown('<h4 class="pass-fail-summary">Pass/Fail Summary</h4>', unsafe_allow_html=True)
                pie_data = pd.DataFrame({
                    'Analysis': ['Pass', 'Fail'],
                    'Percentage': [summary['overall_pass_rate'], summary['overall_fail_rate']]
                })

                pie_chart = alt.Chart(pie_data).mark_arc(innerRadius=40).encode(
                    theta=alt.Theta(field="Percentage", type="quantitative"),
                    color=alt.Color(field="Analysis", type="nominal",
                                    scale=alt.Scale(domain=['Pass', 'Fail'], range=['#2ecc40', '#ff4136'])),
                    tooltip=['Analysis', 'Percentage']
                ).properties(width=250, height=250)
                st.altair_chart(pie_chart, use_container_width=False)

            with tab2:
                tab2.markdown('<h2 class="tab-subheader">DeepEval Results</h2>', unsafe_allow_html=True)

                # Prepare the DataFrame, truncating fields for readability
                df = pd.DataFrame(detailed)
                if 'input_prompt' in df.columns:
                    # Optionally rename for clarity
                    df.rename(columns={'input_prompt': 'Question'}, inplace=True)
                    # Truncate long questions for display
                    df['Question'] = df['Question'].apply(lambda q: (q[:80] + '…') if q and len(q) > 80 else q)

                if 'reasoning' in df.columns:
                    # Truncate long reasoning for display
                    df['reasoning'] = df['reasoning'].apply(lambda r: (r[:100] + '…') if r and len(r) > 100 else r)

                # Optional: Add a human-friendly Pass/Fail column
                if 'success' in df.columns:
                    df['Result'] = df['success'].apply(lambda x: "✅ Pass" if x else "❌ Fail")

                columns = [
                    'question_number', 'Question', 'expected_output', 'actual_output', 'score', 'Result', 'reasoning'
                ]
                # Only keep the columns that exist in the DataFrame
                df = df[[col for col in columns if col in df.columns]]

                # Style: highlight rows based on pass/fail if using Styler (for st.dataframe)
                def highlight_fail(row):
                    return ['background-color: #FEE' if row['Result']=='❌ Fail' else '' for _ in row]

                styled_df = df.style.apply(highlight_fail, axis=1) if 'Result' in df.columns else df

                # Show with Streamlit
                st.dataframe(
                    styled_df,
                    use_container_width=True,
                    height=min(40*len(df)+40, 600)  # auto-size for number of questions, capped at 600px
                )

            with tab3:
                tab3.markdown('<h2 class="tab-subheader">Score Chart</h2>', unsafe_allow_html=True)

                # Prepare data for bar/column chart
                bins = distribution['bins']
                counts = distribution['counts']
                bin_labels = [f"{bins[i]:.1f}–{bins[i+1]:.1f}" for i in range(len(bins)-1)]
                df = pd.DataFrame({'Score Bin': bin_labels, 'Test Cases': counts})

                st.bar_chart(df.set_index("Score Bin"))

                # Display high-level stats
                stats = distribution.get('statistics', {})
                stats_display = f"""
                - **Mean:** {stats.get('mean', 0):.2f}  
                - **Min:** {stats.get('min', 0):.2f}  
                - **Max:** {stats.get('max', 0):.2f}  
                - **Std Dev:** {stats.get('std', 0):.2f}
                """
                st.markdown("#### Score Summary Statistics")
                st.markdown(stats_display)

                # Optionally: List table
                st.markdown("#### Tests per Score Range")
                st.table(df.set_index('Score Bin'))

            with tab4:
                tab4.markdown('<h2 class="tab-subheader">Quality Analysis</h2>', unsafe_allow_html=True)

                # Performance bands
                perf = insights.get('performance_by_score', {})
                st.subheader("Performance by Score Band")
                st.markdown(
                    f"- **Excellent (≥0.9):** {perf.get('excellent', 0)} cases  \n"
                    f"- **Good (0.7–0.89):** {perf.get('good', 0)} cases  \n"
                    f"- **Fair (0.5–0.69):** {perf.get('fair', 0)} cases  \n"
                    f"- **Poor (<0.5):** {perf.get('poor', 0)} cases"
                )

                # Common failure patterns
                patterns = (insights.get('common_failure_patterns', {}).get('common_issues')
                            if isinstance(insights.get('common_failure_patterns', {}), dict)
                            else insights.get('common_failure_patterns', []))

                st.subheader("Common Failure Patterns")
                if patterns:
                    for p in patterns:
                        st.markdown(f"- {p}")
                else:
                    st.write("No common failure patterns identified.")

                # Failure rate if present
                fail_rate = insights.get('common_failure_patterns', {}).get('failure_rate')
                if fail_rate is not None:
                    st.markdown(f"**Failure Rate:** {fail_rate:.1f}%")

            with tab5:
                tab5.markdown('<h2 class="tab-subheader">Test Cases</h2>', unsafe_allow_html=True)

        else:
            st.info("No DeepEval quality assessment yet. Please run DeepEval first.")

