import os
import threading
import time
import re
import streamlit as st
from datetime import datetime
from threading import Thread
import shutil

from src.utils.event_logs import (
    add_jmeter_log,
    thread_safe_add_log,
    add_deepeval_log,
)
from src.tools.jmeter_executor import (
    run_jmeter_test_node,
    analyze_jmeter_test_node,
    stop_jmeter_test_node,
    analyze_llm_metrics_node
)
from src.tools.deepeval_assessment import (
    run_deepeval_assessment_node,
    analyze_deepeval_results_node
)
from src.utils.test_state import TestState, DeepEvalTestState
# Import configuration loader
from src.utils.config import load_config

# Load configurations
config = load_config()
deepeval_config = config.get("deepeval", {})
#  ========================= JMeter UI Handlers =========================
def __start_jmeter_thread(shared_data, state_snapshot):
    """Background thread target to run JMeter and update session state/logs."""
    try:
        # Update status to running in shared data
        shared_data['status'] = TestState.RUNNING
        shared_data['stop_requested'] = False  # Add stop flag
        
        result = run_jmeter_test_node(shared_data, state_snapshot)

        # Check if stop was requested before processing results
        if shared_data.get('stop_requested', False):
            thread_safe_add_log(shared_data['logs'], "🛑 JMeter test was stopped by user request.", agent_name="JMeterAgent")
            thread_safe_add_log(shared_data['logs'], "🔍 Skipping analysis - test was stopped.", agent_name="JMeterAgent")
            shared_data['status'] = TestState.STOPPED
            return  # Exit early, don't process results
        # If we reach here, it means the test ran successfully
        if result:
            thread_safe_add_log(shared_data['logs'], "✅ JMeter load test executed successfully.", agent_name="JMeterAgent")
            shared_data['status'] = TestState.COMPLETED
            shared_data['results'] = result
            shared_data['jmeter_jtl_path'] = result['jmeter_jtl_path']
            shared_data['jmeter_log_path'] = result['jmeter_log_path']
            shared_data['llm_kpis_path'] = result.get('llm_kpis_path', "")
            shared_data['llm_metrics_path'] = result.get('llm_metrics_path', "")
            shared_data['llm_responses_path'] = result.get('llm_responses_path', "")
            shared_data['run_timestamp'] = result.get('run_timestamp', 'NOT_FOUND')
            thread_safe_add_log(shared_data['logs'], f"📊🔥 Load test results saved to {result['jmeter_jtl_path']}", agent_name="JMeterAgent")
            thread_safe_add_log(shared_data['logs'], f"📊🔥 Load test log saved to {result['jmeter_log_path']}", agent_name="JMeterAgent")
            thread_safe_add_log(shared_data['logs'], f"📊🔥 LLM Metrics saved to {result['llm_metrics_path']}", agent_name="JMeterAgent")
            thread_safe_add_log(shared_data['logs'], f"📊🔥 LLM Responses saved to {result['llm_responses_path']}", agent_name="JMeterAgent")

            # Analyze results in background thread. Only analyze if not stopped
            if not shared_data.get('stop_requested', False):
                # --- JMeter Analysis ---
                thread_safe_add_log(shared_data['logs'], "🔍 Analyzing JMeter load test results...", agent_name="JMeterAgent")
                jmeter_analysis_result = analyze_jmeter_test_node(shared_data, state_snapshot)
                if not jmeter_analysis_result:
                    thread_safe_add_log(shared_data['logs'], "⚠️ No JMeter analysis results found. Check JTL file.", agent_name="AgentError")
                    shared_data['status'] = TestState.FAILED
                    return

                thread_safe_add_log(shared_data['logs'], "✅ JMeter load test analysis completed successfully.", agent_name="JMeterAgent")

                # --- LLM Metrics Analysis ---
                thread_safe_add_log(shared_data['logs'], "🔍 Analyzing LLM token metrics...", agent_name="JMeterAgent")
                llm_analysis_result = analyze_llm_metrics_node(shared_data, state_snapshot)

                if not llm_analysis_result:
                    thread_safe_add_log(shared_data['logs'], "⚠️ No LLM metrics found. Test will continue with JMeter results only.", agent_name="JMeterAgent")
                    # Don't fail the test - LLM metrics are optional
                    shared_data['analysis'] = jmeter_analysis_result
                else:
                    thread_safe_add_log(shared_data['logs'], "✅ LLM metrics analysis completed successfully.", agent_name="JMeterAgent")
                    # Combine both analysis results
                    combined_analysis = {**jmeter_analysis_result, **llm_analysis_result}
                    shared_data['analysis'] = combined_analysis

            else:
                thread_safe_add_log(shared_data['logs'], "🔍 Skipping analysis - test was stopped.", agent_name="JMeterAgent")

        else:
            thread_safe_add_log(shared_data['logs'], "❌ JMeter load test failed to execute.", agent_name="AgentError")
            shared_data['status'] = TestState.FAILED
            shared_data['results'] = None
    except Exception as e:
        thread_safe_add_log(shared_data['logs'], f"❌ JMeter load test execution failed: {str(e)}", agent_name="AgentError")
        shared_data['status'] = TestState.FAILED
        shared_data['results'] = None

def handle_start_jmeter_test():
    """Handler for starting the JMeter test."""
    # Add defensive check for duplicate starts
    if st.session_state.jmeter_test_state == TestState.RUNNING:
        add_jmeter_log("⚠️ Test is already running. Please wait for completion.", agent_name="JMeterAgent")
        return

    state = st.session_state.get("jmeter_state", {}).copy()
    shared_data = st.session_state.get("jmeter_thread_data", {})

    jmx_path = state.get("jmx_path")
    if not jmx_path or not os.path.exists(jmx_path):
        add_jmeter_log("❌ No valid JMX file found. Please select JMX first.", agent_name="AgentError")
        st.session_state.jmeter_test_state = TestState.FAILED
        return
    
    add_jmeter_log(f"Using JMX file at: {jmx_path}", agent_name="JMeterAgent")
    add_jmeter_log("🔧 Invoking JMeter load test tool...", agent_name="JMeterAgent")

    thread = threading.Thread(target=__start_jmeter_thread, args=(shared_data, state), daemon=True)
    thread.start()

def handle_stop_jmeter_test():
    """Handler for stopping the JMeter test."""
    # Defensive check: Only allow stopping if test is actually running
    if st.session_state.jmeter_test_state != TestState.RUNNING:
        add_jmeter_log("⚠️ Cannot stop test - no test is currently running.", agent_name="JMeterAgent")
        return

    state = st.session_state.get("jmeter_state", {}).copy()
    shared_data = st.session_state.get("jmeter_thread_data", {})

    # Set stop flag FIRST to signal the background thread
    shared_data['stop_requested'] = True
    shared_data['status'] = TestState.STOPPED
    add_jmeter_log("🛑 Stopping JMeter load test...", agent_name="JMeterAgent")

    try:
        # Call the JMeter stop test node
        result = stop_jmeter_test_node(shared_data, state)
        if result:
            state.update(result)
            st.session_state["jmeter_state"] = state
            add_jmeter_log("🛑 JMeter load test stopped successfully.", agent_name="JMeterAgent")
        else:
            add_jmeter_log("⚠️ Failed to stop JMeter test gracefully.", agent_name="JMeterAgent")
            # Still mark as stopped since we attempted to stop it
            st.session_state.jmeter_test_state = TestState.STOPPED
    except Exception as e:
        add_jmeter_log(f"❌ Error stopping JMeter test: {str(e)}", agent_name="AgentError")
        # Mark as stopped even on error to prevent stuck state
        st.session_state.jmeter_test_state = TestState.STOPPED

# ========================== DeepEval UI Handlers =========================
def __start_deepeval_thread(shared_data, state_snapshot):
    """
    Background thread to run DeepEval quality assessment and update session state/logs.
    """
    try:
        # 1. Start analysis
        shared_data['status'] = DeepEvalTestState.RUNNING
        shared_data['start_time'] = datetime.now()
        thread_safe_add_log(shared_data['logs'], "🔄 Running DeepEval assessment node...", agent_name="DeepEvalAgent")
        result = run_deepeval_assessment_node(shared_data, state_snapshot)

        if result:
            shared_data['status'] = DeepEvalTestState.COMPLETED
            shared_data['results'] = result
            shared_data['deepeval_output_file'] = result.get('deepeval_output_file', '')
            thread_safe_add_log(shared_data['logs'], "✅ DeepEval assessment node completed.", agent_name="DeepEvalAgent")

            # 2. Process analysis results
            thread_safe_add_log(shared_data['logs'], "🔍 Analyzing DeepEval results...", agent_name="DeepEvalAgent")
            analysis = analyze_deepeval_results_node(shared_data, state_snapshot)            
            if not analysis:
                thread_safe_add_log(shared_data['logs'], "⚠️ No DeepEval analysis results found. Check results file.", agent_name="AgentError")
                shared_data['status'] = DeepEvalTestState.FAILED
                shared_data['analysis'] = None
                shared_data['error_message'] = "No analysis results found."
                return

            # 3. Finalize
            thread_safe_add_log(shared_data['logs'], "🏁 DeepEval assessment completed successfully.", agent_name="DeepEvalAgent")
            shared_data['status'] = DeepEvalTestState.COMPLETED
            shared_data['analysis'] = analysis

        else:
            error = result.get('error', 'Unknown error')
            thread_safe_add_log(shared_data['logs'], f"❌ DeepEval assessment failed: {error}", agent_name="DeepEvalAgent")
            # Update shared_data instead of session state directly
            shared_data['status'] = DeepEvalTestState.FAILED
            shared_data['error_message'] = error
            shared_data['results'] = None
            return

    except Exception as e:
        # Unexpected error handling
        thread_safe_add_log(shared_data['logs'], f"💥 DeepEval thread error: {str(e)}", agent_name="DeepEvalAgent")
        shared_data['status'] = DeepEvalTestState.FAILED
        shared_data['error_message'] = str(e)
        shared_data['results'] = None

def handle_start_deepeval_assessment():
    """
    Handle the start of DeepEval assessment process.
    This function manages pre-assessment checks, file cleanup, and thread initialization.
    """
    try:
        # 1. Pre-assessment validation and logging
        add_deepeval_log("🔍 Performing pre-assessment validation...", agent_name="DeepEvalAgent")
        
        # Check if DeepEval is already running
        if str(st.session_state.deepeval_test_state) == str(DeepEvalTestState.RUNNING):
            add_deepeval_log("⚠️ DeepEval is already running. Please wait for completion.", agent_name="DeepEvalAgent")
            return
        
        # Validate JMeter test completion
        if str(st.session_state.jmeter_test_state) != str(TestState.COMPLETED):
            add_deepeval_log("❌ JMeter test must be completed before starting DeepEval.", agent_name="DeepEvalAgent")
            return
        
        # Validate metrics selection
        selected_metrics = st.session_state.deepeval_state.get('selected_metrics', [])
        if not selected_metrics:
            add_deepeval_log("❌ No metrics selected. Please select at least one quality metric.", agent_name="DeepEvalAgent")
            return
        
        # Validate LLM responses file exists
        llm_responses_path = st.session_state.jmeter_thread_data.get('llm_responses_path', '')
        if not llm_responses_path or not os.path.exists(llm_responses_path):
            add_deepeval_log("❌ LLM responses file not found. Please run JMeter test first.", agent_name="DeepEvalAgent")
            return
        
        add_deepeval_log("✅ Pre-assessment validation completed successfully.", agent_name="DeepEvalAgent")
        
        # 2. Create session state snapshot and shared data
        add_deepeval_log("📸 Creating session state snapshot...", agent_name="DeepEvalAgent")

        state = st.session_state.get("deepeval_state", {}).copy()
        shared_data = st.session_state.get("deepeval_thread_data", {})
        # Set initial shared data values
        shared_data['llm_responses_file'] = state.get('llm_responses_path', '')
        shared_data['selected_metrics'] = state.get('selected_metrics', [])
        shared_data['run_timestamp'] = state.get('run_timestamp', 'NOT_FOUND')
        add_deepeval_log(f"Loaded llm_responses_file: {shared_data['llm_responses_file']}", agent_name="DeepEvalAgent")
        add_deepeval_log(f"Loaded selected_metrics: {shared_data['selected_metrics']}", agent_name="DeepEvalAgent")
        add_deepeval_log(f"Loaded run_timestamp: {shared_data['run_timestamp']}", agent_name="DeepEvalAgent")
        add_deepeval_log("Session state snapshot created successfully.", agent_name="DeepEvalAgent")

        # 3. Update DeepEval test state to RUNNING
        st.session_state.deepeval_test_state = DeepEvalTestState.RUNNING
        add_deepeval_log("🔄 DeepEval state updated to RUNNING.", agent_name="DeepEvalAgent")

        # 4. File cleanup and backup operations
        add_deepeval_log("🧹 Performing file cleanup and backup operations...", agent_name="DeepEvalAgent")
        perform_deepeval_file_cleanup(shared_data)
        add_deepeval_log("✅ File cleanup completed successfully.", agent_name="DeepEvalAgent")

        # 5. Initialize thread data
        add_deepeval_log("⚙️ Initializing thread data...", agent_name="DeepEvalAgent")
        add_deepeval_log("✅ Thread data initialized successfully.", agent_name="DeepEvalAgent")

        # 6. Start background thread
        st.session_state.deepeval_shared_data = shared_data
        add_deepeval_log("🚀 Starting background thread for DeepEval execution...", agent_name="DeepEvalAgent")
        thread = threading.Thread(target=__start_deepeval_thread, args=(shared_data, state), daemon=True)
        thread.start()
        add_deepeval_log("✅ DeepEval background thread started successfully.", agent_name="DeepEvalAgent")
        
    except Exception as e:
        # Error handling and user notification
        error_msg = f"❌ Failed to start DeepEval assessment: {str(e)}"
        add_deepeval_log(error_msg, agent_name="DeepEvalAgent")
        st.session_state.deepeval_test_state = DeepEvalTestState.FAILED
        st.session_state.deepeval_errors['last_error'] = str(e)
        st.session_state.deepeval_errors['error_count'] += 1

def perform_deepeval_file_cleanup(shared_data):
    """Handle pre-assessment file cleanup and backup operations."""
    try:
        # Path to the DeepEval output directory
        deepeval_results_path = deepeval_config.get("deepeval_results_path", ".deepeval")
        latest_test_run_path = os.path.join(deepeval_results_path, ".latest_test_run.json")

        # Create .old subdirectory if it doesn't exist
        old_dir = os.path.join(deepeval_results_path, ".old")
        if not os.path.exists(old_dir):
            os.makedirs(old_dir)
            add_deepeval_log("📁 Created .old directory for backup files.", agent_name="DeepEvalAgent")
        
        # Check if .latest_test_run.json exists
        if os.path.exists(latest_test_run_path):
            # Generate backup filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"backup_{timestamp}_.latest_test_run.json"
            backup_path = os.path.join(old_dir, backup_filename)
            
            # Move existing file to backup
            shutil.move(latest_test_run_path, backup_path)
            add_deepeval_log(f"🗂️ Existing .latest_test_run.json backed up to: {backup_filename}", agent_name="DeepEvalAgent")
            
            # Track backup in session state
            st.session_state.deepeval_state['backup_files'][latest_test_run_path] = backup_path
        else:
            add_deepeval_log("📝 No existing .latest_test_run.json file found - no cleanup needed.", agent_name="DeepEvalAgent")
            
    except Exception as e:
        add_deepeval_log(f"⚠️ File cleanup warning: {str(e)}", agent_name="DeepEvalAgent")
        shared_data['error_details'] = f"File cleanup error: {str(e)}"
