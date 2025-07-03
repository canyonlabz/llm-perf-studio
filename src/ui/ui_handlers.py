import os
import time
import re
import streamlit as st
from datetime import datetime

from src.utils.event_logs import (
    add_jmeter_log,
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

# ========================= JMeter UI Handlers =========================
def handle_start_jmeter_test():
    """Handler for starting the JMeter test."""
    state = st.session_state.get("jmeter_state", {}).copy()

    jmx_path = state.get("jmx_path")
    if not jmx_path or not os.path.exists(jmx_path):
        add_jmeter_log("❌ No valid JMX file found. Please select JMX first.", agent_name="AgentError")
        return
    add_jmeter_log(f"Using JMX file at: {jmx_path}", agent_name="JMeterAgent")
    add_jmeter_log("🔧 Invoking JMeter load test tool...", agent_name="JMeterAgent")

    try:
        # Call the JMeter test node
        result = run_jmeter_test_node(state)
        if result:  # Successful run
            add_jmeter_log("✅ JMeter load test executed successfully.", agent_name="JMeterAgent")
            st.session_state.jmeter_test_state = TestState.COMPLETED
        else:  # Failed run
            add_jmeter_log("❌ JMeter load test failed to execute.", agent_name="AgentError")
            st.session_state.jmeter_test_state = TestState.FAILED
            return
    except Exception as e:
        add_jmeter_log(f"❌ JMeter load test execution failed: {str(e)}", agent_name="AgentError")
        st.session_state.jmeter_test_state = TestState.FAILED
        return

    # Update the state with the results
    state.update(result)
    add_jmeter_log(f"📊🔥 Load test results saved to {result['jmeter_jtl_path']}", agent_name="JMeterAgent")
    add_jmeter_log(f"📊🔥 Load test log saved to {result['jmeter_log_path']}", agent_name="JMeterAgent")

    # Analyze the JMeter test results
    add_jmeter_log("🔍 Analyzing load test results...", agent_name="JMeterAgent")
    analysis_result = analyze_jmeter_test_node(state)
    state["jmeter_test_results"] = analysis_result  # Store analysis under this key
    st.session_state["jmeter_state"] = state        # Updates the full state

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
