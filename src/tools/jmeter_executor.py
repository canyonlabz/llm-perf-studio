# Module to handle JMeter tasks
import os
import subprocess
from typing import Dict, Any
import pandas as pd
import numpy as np
import platform
import threading
from datetime import datetime
from src.utils.config import load_config
from src.utils.event_logs import add_jmeter_log, thread_safe_add_log

# Load configurations
config = load_config()

#--- JMeter Test Nodes ---
# This node runs a load test on the selected JMX file.
def run_jmeter_test_node(shared_data: Dict[str, Any], state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Run a JMeter load test: Example - 1 thread, 1 loop, 5 minutes duration.
    Returns paths to the JTL results file and JMeter log file.
    """
    run_timestamp = state.get("run_timestamp", datetime.now().strftime("%Y%m%d_%H%M%S"))

    # Define the JMeter command to run the load test which supports both Windows and Mac/Linux.
    cli = config['jmeter']['jmeter_bin_path']
    is_windows = platform.system().lower().startswith("win")
    start_script = "jmeter.bat" if is_windows else "jmeter"
    start_cmd = os.path.join(cli, start_script)

    # Define the JMeter results path and JMX path
    jmeter_results_path = config['jmeter']['jmeter_results_path']
    jmx_path = state.get("jmx_path")
    if not jmx_path or not os.path.exists(jmx_path):
        thread_safe_add_log(shared_data['logs'], "❌ No valid JMX file found. Please select JMX first.", agent_name="AgentError")
        return {}

    # Get the JMeter settings from the session state
    vusers = state.get("vusers", 1)
    ramp_up = state.get("ramp_up", 60)  # Default to 60 seconds if not set
    iterations = state.get("iterations", 1)  # Default to 1 iteration if not set
    duration = state.get("duration", 300)  # Default to 5 minutes if not set
    use_rag = state.get("use_rag", False)  # Whether to use RAG mode
    prompt_num = state.get("prompt_num", 5)  # Number of prompts to use from input JSON file

    jmeter_jtl = os.path.join(jmeter_results_path, f"{run_timestamp}_jmeter_test.jtl")
    jmeter_log = os.path.join(jmeter_results_path, f"{run_timestamp}_jmeter_test.log")

    # Build the JMeter command to run the load test
    cmd = [
        start_cmd,
        '-n',  # Non-GUI mode
        '-t', jmx_path,  # JMX test plan
        '-l', jmeter_jtl,  # JTL results file
        '-j', jmeter_log,  # JMeter log file
        '-Jvusers={}'.format(vusers),           # Number of threads (virtual users)
        '-Jramp_up={}'.format(ramp_up),         # Ramp-up time in seconds
        '-Jiterations={}'.format(iterations),   # Number of iterations
        '-Jduration={}'.format(duration),       # Ramp-up time in seconds
        '-Juse_rag={}'.format(use_rag),         # Use RAG mode
        '-Jprompt_num={}'.format(prompt_num),   # Number of prompts to use
        '-Jrun_timestamp={}'.format(run_timestamp)  # Run timestamp for unique file names
    ]

    try:
        thread_safe_add_log(shared_data['logs'], f"🏃‍♂️ Running JMeter: {' '.join(cmd)}", agent_name="JMeterAgent")
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        thread_safe_add_log(shared_data['logs'], f"❌ Load test failed: {e}", agent_name="AgentError")
        return {}

    return {
        "jmeter_jtl_path": jmeter_jtl,
        "jmeter_log_path": jmeter_log,
        "llm_kpis_path": os.path.join(jmeter_results_path, f"{run_timestamp}_llm_kpis.csv"),
        "llm_responses_path": os.path.join(jmeter_results_path, f"{run_timestamp}_llm_responses.json"),
        "run_timestamp": run_timestamp,
    }

def analyze_jmeter_test_node(shared_data: Dict[str, Any], state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyze the results of the load test.
    Returns a summary of the test results.
    """
    jtl_path = shared_data.get('jmeter_jtl_path', None)
    if not jtl_path or not os.path.exists(jtl_path):
        thread_safe_add_log(shared_data['logs'], "❌ No valid JTL file found. Please run load test first.", agent_name="AgentError")
        return {}

    # Load JTL as DataFrame
    df = pd.read_csv(jtl_path)
    if df.empty:
        thread_safe_add_log(shared_data['logs'], "❌ JTL file is empty.", agent_name="AgentError")
        return {}

    # Convert timestamps
    df['timeStamp'] = pd.to_datetime(df['timeStamp'], unit='ms')
    start_time = df['timeStamp'].min()
    end_time = df['timeStamp'].max()
    duration = end_time - start_time

    # Calculate pass/fail
    total_samples = len(df)
    passed = df['success'].sum() if df['success'].dtype == bool else (df['success'] == 'true').sum()
    failed = total_samples - passed
    pass_pct = (passed / total_samples) * 100 if total_samples else 0
    fail_pct = (failed / total_samples) * 100 if total_samples else 0
    error_rate = fail_pct

    # Aggregate response times per label
    def pct90(x): return np.percentile(x, 90)
    agg = df.groupby('label').agg(
        samples=('elapsed', 'count'),
        errors=('success', lambda x: (~x if x.dtype == bool else x != 'true').sum()),
        avg=('elapsed', 'mean'),
        min=('elapsed', 'min'),
        max=('elapsed', 'max'),
        pct90=('elapsed', pct90)
    ).reset_index()
    agg['error_rate'] = (agg['errors'] / agg['samples']) * 100

    # Calculate test duration in minutes and determine dynamic interval
    test_duration_minutes = duration.total_seconds() / 60
    dynamic_interval = calculate_dynamic_interval(test_duration_minutes)
    
    # Log the interval being used for transparency
    thread_safe_add_log(shared_data['logs'], f"📊 Using {dynamic_interval} sampling interval for {test_duration_minutes:.1f} minute test", agent_name="JMeterAgent")

    # Prepare data for 90th percentile line chart (aggregate over time)
    time_group = df.set_index('timeStamp').resample(dynamic_interval)  # Resample based on dynamic interval

    # Calculate 90th percentile over time with forward fill for continuity
    pct90_over_time = time_group['elapsed'].apply(lambda x: np.percentile(x, 90) if len(x) else np.nan)
    pct90_over_time = pct90_over_time.ffill()  # Forward fill missing values

    # Calculate virtual users over time with forward fill for alignment
    # Use grpThreads (group threads) or allThreads (all threads) for accurate concurrency
    # grpThreads represents the active threads in the thread group at request time
    vusers_over_time = time_group['grpThreads'].min()  # Use min to get concurrency per interval
    vusers_over_time = vusers_over_time.ffill()  # Forward fill missing values

    # Human-readable times
    start_time_str = start_time.strftime('%Y-%m-%d %H:%M:%S')
    end_time_str = end_time.strftime('%Y-%m-%d %H:%M:%S')
    duration_str = str(duration)

    # Aggregate average response time
    avg_response_time = df['elapsed'].mean()

    # Aggregate 90th percentile response time
    pct90_response_time = np.percentile(df['elapsed'], 90)

    # Overlay data for 90th percentile and virtual users
    df_overlay = pd.DataFrame({
        'time': pct90_over_time.index,
        'pct90_response': pct90_over_time.values,
        'vusers': vusers_over_time.reindex(pct90_over_time.index, method='ffill').values
    })

    # Remove any remaining NaN values that might cause chart issues
    df_overlay = df_overlay.dropna()

    summary = {
        "status": "success" if failed == 0 else "fail",
        "pass_pct": pass_pct,
        "fail_pct": fail_pct,
        "start_time": start_time_str,
        "end_time": end_time_str,
        "duration": duration,
        "avg_response_time": avg_response_time,
        "pct90_response_time": pct90_response_time,
        "error_rate": error_rate,
        "agg_table": agg,
        "pct90_over_time": pct90_over_time,
        "vusers_over_time": vusers_over_time,
        "overlay_df": df_overlay,
        "sampling_interval": dynamic_interval,
        "test_duration_minutes": test_duration_minutes
    }
    thread_safe_add_log(shared_data['logs'], f"✅ Load test analysis complete: {summary['status']} ({passed}/{total_samples} passed)", agent_name="JMeterAgent")
    return summary

def stop_jmeter_test_node(shared_data: Dict[str, Any], state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Stop the currently running JMeter test.
    This is a placeholder function as stopping JMeter tests programmatically is complex.
    """
    cli = config['jmeter']['jmeter_bin_path']
    is_windows = platform.system().lower().startswith("win")
    stop_script = "stoptest.cmd" if is_windows else "stoptest.sh"
    stop_cmd = os.path.join(cli, stop_script)

    thread_safe_add_log(shared_data['logs'], f"Attempting to stop JMeter test with command: {stop_cmd}", agent_name="JMeterAgent")

    try:
        subprocess.run(stop_cmd, shell=True, check=True)
        thread_safe_add_log(shared_data['logs'], "🛑 JMeter stop command sent successfully.", agent_name="JMeterAgent")
    except subprocess.CalledProcessError as e:
        thread_safe_add_log(shared_data['logs'], f"❗Failed to stop JMeter: {e}", agent_name="AgentError")

    # In practice, you would need to implement a way to stop the JMeter process gracefully.
    # This could involve sending a shutdown command or killing the process.
    thread_safe_add_log(shared_data['logs'], "🛑 Stopping JMeter test!", agent_name="JMeterAgent")
    return {}

#--- Utility Functions ---
def calculate_dynamic_interval(test_duration_minutes):
    """
    Calculate appropriate sampling interval based on test duration
    Target: 50-100 data points for optimal visualization
    """
    if test_duration_minutes <= 5:
        return '5s'    # 5-second intervals for short tests
    elif test_duration_minutes <= 15:
        return '10s'   # 10-second intervals for medium tests
    elif test_duration_minutes <= 30:
        return '30s'   # 30-second intervals for longer tests
    else:
        return '1min'  # 1-minute intervals for tests up to 1 hour

