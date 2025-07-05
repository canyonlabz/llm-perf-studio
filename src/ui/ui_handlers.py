import os
import threading
import time
import re
import streamlit as st
from datetime import datetime
from threading import Thread

from src.utils.event_logs import (
    add_jmeter_log,
    thread_safe_add_log,
    add_deepeval_log,
)
from src.tools.jmeter_executor import (
    run_jmeter_test_node,
    analyze_jmeter_test_node,
    stop_jmeter_test_node,
)
from src.utils.test_state import TestState
# Import configuration loader
from src.utils.config import load_config

# Load configurations
config = load_config()

#  ========================= JMeter UI Handlers =========================
def __start_jmeter_thread(shared_data, state_snapshot):
    """Background thread target to run JMeter and update session state/logs."""
    try:
        # Update status to running in shared data
        shared_data['status'] = TestState.RUNNING
        
        result = run_jmeter_test_node(shared_data, state_snapshot)
        if result:
            thread_safe_add_log(shared_data['logs'], "✅ JMeter load test executed successfully.", agent_name="JMeterAgent")
            shared_data['status'] = TestState.COMPLETED
            shared_data['results'] = result
            shared_data['jmeter_jtl_path'] = result['jmeter_jtl_path']
            shared_data['jmeter_log_path'] = result['jmeter_log_path']
            thread_safe_add_log(shared_data['logs'], f"📊🔥 Load test results saved to {result['jmeter_jtl_path']}", agent_name="JMeterAgent")
            thread_safe_add_log(shared_data['logs'], f"📊🔥 Load test log saved to {result['jmeter_log_path']}", agent_name="JMeterAgent")
            
            # Analyze results in background thread
            thread_safe_add_log(shared_data['logs'], "🔍 Analyzing load test results...", agent_name="JMeterAgent")
            analysis_result = analyze_jmeter_test_node(shared_data, state_snapshot)
            if not analysis_result:
                thread_safe_add_log(shared_data['logs'], "⚠️ No analysis results found. Check JTL file.", agent_name="AgentError")
                shared_data['status'] = TestState.FAILED
            else:
                thread_safe_add_log(shared_data['logs'], "✅ Load test analysis completed successfully.", agent_name="JMeterAgent")
                #thread_safe_add_log(shared_data['logs'], f"📊 Analysis results: {analysis_result}", agent_name="JMeterAgent")
            shared_data['analysis'] = analysis_result
            
        else:
            thread_safe_add_log(shared_data['logs'], "❌ JMeter load test failed to execute.", agent_name="AgentError")
            shared_data['status'] = TestState.FAILED
            
    except Exception as e:
        thread_safe_add_log(shared_data['logs'], f"❌ JMeter load test execution failed: {str(e)}", agent_name="AgentError")
        shared_data['status'] = TestState.FAILED

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
    add_jmeter_log("🛑 Stopping JMeter load test...", agent_name="JMeterAgent")

    try:
        # Call the JMeter stop test node
        result = stop_jmeter_test_node(state)
        if result:
            state.update(result)
            st.session_state["jmeter_state"] = state        # Updates the full state
            add_jmeter_log("🛑 JMeter load test stopped successfully.", agent_name="JMeterAgent")
        else:
            add_jmeter_log("⚠️ Failed to stop JMeter test gracefully.", agent_name="JMeterAgent")
            # Still mark as stopped since we attempted to stop it
            st.session_state.jmeter_test_state = TestState.STOPPED
    except Exception as e:
        add_jmeter_log(f"❌ Error stopping JMeter test: {str(e)}", agent_name="AgentError")
        # Mark as stopped even on error to prevent stuck state
        st.session_state.jmeter_test_state = TestState.STOPPED
