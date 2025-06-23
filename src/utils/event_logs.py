from datetime import datetime
import streamlit as st
from langchain_core.callbacks import BaseCallbackHandler

# --- JMeter Logs ------------------------------------------------
# This module handles logging to the JMeter viewer.
def add_jmeter_log(message: str, agent_name: str = "JMeterAgent"):
    """Add a log entry to the JMeter Viewer."""
    # Check if the session state for agent logs exists, if not, create it
    if "jmeter_logs" not in st.session_state:
        st.session_state.jmeter_logs = []
    
    timestamp = datetime.now().strftime("%H:%M:%S")
    log_entry = f"[{timestamp}] {agent_name}: {message}"
    
    st.session_state.jmeter_logs.append(log_entry)
    
    # Optional: Limit log size
    if len(st.session_state.jmeter_logs) > 1000:
        st.session_state.jmeter_logs = st.session_state.jmeter_logs[-1000:]

# --- DeepEval Logs ------------------------------------------------
# This module handles logging to the DeepEval viewer.
def add_deepeval_log(message: str, agent_name: str = "DeepEvalAgent"):
    """Add a log entry to the DeepEval Viewer."""
    # Check if the session state for agent logs exists, if not, create it
    if "deepeval_logs" not in st.session_state:
        st.session_state.deepeval_logs = []
    
    timestamp = datetime.now().strftime("%H:%M:%S")
    log_entry = f"[{timestamp}] {agent_name}: {message}"
    
    st.session_state.deepeval_logs.append(log_entry)
    
    # Optional: Limit log size
    if len(st.session_state.deepeval_logs) > 1000:
        st.session_state.deepeval_logs = st.session_state.deepeval_logs[-1000:]

