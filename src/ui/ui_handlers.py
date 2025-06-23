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
    analyze_jmeter_test_node
)
# Import configuration loader
from src.utils.config import load_config

# Load configurations
config = load_config()

# ========================= JMeter UI Handlers =========================
def handle_start_jmeter_test():
    add_jmeter_log("🏃‍♂️ Run Load Test: Executing load test...", agent_name="JMeterAgent")
    add_jmeter_log("Running load test with selected JMX file.", agent_name="JMeterAgent")
    add_jmeter_log("🏃‍♂️ Running load test…", agent_name="JMeterAgent")

    state = st.session_state.get("jmeter_state", {}).copy()
    jmx_path = state.get("jmx_path")
    if not jmx_path or not os.path.exists(jmx_path):
        add_jmeter_log("❌ No valid JMX file found. Please select JMX first.", agent_name="AgentError")
        return
    add_jmeter_log(f"Using JMX file at: {jmx_path}", agent_name="JMeterAgent")

    # Call the JMeter test node
    add_jmeter_log("🔧 Invoking JMeter load test tool...", agent_name="JMeterAgent")
    result = run_jmeter_test_node(state)
    state.update(result)
    add_jmeter_log(f"📊🔥 Load test results saved to {result['jmeter_jtl_path']}", agent_name="JMeterAgent")
    add_jmeter_log(f"📊🔥 Load test log saved to {result['jmeter_log_path']}", agent_name="JMeterAgent")

    # Analyze the JMeter test results
    add_jmeter_log("🔍 Analyzing load test results...", agent_name="JMeterAgent")
    analysis_result = analyze_jmeter_test_node(state)
    state["jmeter_test_results"] = analysis_result  # Store analysis under this key
    st.session_state["jmeter_state"] = state        # Updates the full state

    add_jmeter_log("✅ Load test executed successfully.", agent_name="JMeterAgent")
