# Module to handle JMeter tasks
import os
import subprocess
from typing import Dict, Any
import pandas as pd
import numpy as np
from datetime import datetime
from src.utils.config import load_config
from src.utils.event_logs import add_jmeter_log

# Load configurations
config = load_config()

#--- JMeter Test Node ---
# This node runs a load test on the selected JMX file.
def run_jmeter_test_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Run a JMeter load test: Example - 1 thread, 1 loop, 5 minutes duration.
    Returns paths to the JTL results file and JMeter log file.
    """
    run_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")    # Define a unique timestamp for the load test.
    cli = config['jmeter']['jmeter_bin_path']
    jmeter_results_path = config['jmeter']['jmeter_results_path']
    jmx_path = state.get("jmx_path")
    if not jmx_path or not os.path.exists(jmx_path):
        add_jmeter_log("❌ No valid JMX file found. Please select JMX first.", agent_name="AgentError")
        return {}

    # Get the JMeter settings from the session state
    vusers = state.get("vusers", 1)
    duration = state.get("duration", 300)  # Default to 5 minutes if not set
    ramp_up = state.get("ramp_up", 60)  # Default to 60 seconds if not set
    iterations = state.get("iterations", 1)  # Default to 1 iteration if not set

    jmeter_jtl = os.path.join(jmeter_results_path, f"jmeter_test_{run_timestamp}.jtl")
    jmeter_log = os.path.join(jmeter_results_path, f"jmeter_test_{run_timestamp}.log")

    # Build the JMeter command to run the load test
    cmd = [
        cli,
        '-n',  # Non-GUI mode
        '-t', jmx_path,  # JMX test plan
        '-l', jmeter_jtl,  # JTL results file
        '-j', jmeter_log,  # JMeter log file
        '-Jduration={}'.format(duration),   # Ramp-up time in seconds
        '-Jthreads={}'.format(vusers),      # Number of threads (virtual users)
        '-Jrampup={}'.format(ramp_up),      # Ramp-up time in seconds
        '-Jloops={}'.format(iterations),    # Number of iterations
    ]

    try:
        add_jmeter_log(f"🏃‍♂️ Running JMeter: {' '.join(cmd)}", agent_name="JMeterAgent")
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        add_jmeter_log(f"❌ Load test failed: {e}", agent_name="AgentError")
        return {}

    return {
        "jmeter_jtl_path": jmeter_jtl,
        "jmeter_log_path": jmeter_log
    }

def analyze_jmeter_test_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyze the results of the load test.
    Returns a summary of the test results.
    """
    jtl_path = state.get("jmeter_jtl_path")
    if not jtl_path or not os.path.exists(jtl_path):
        add_jmeter_log("❌ No valid JTL file found. Please run load test first.", agent_name="AgentError")
        return {}

    # Load JTL as DataFrame
    df = pd.read_csv(jtl_path)
    if df.empty:
        add_jmeter_log("❌ JTL file is empty.", agent_name="AgentError")
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

    # Prepare data for 90th percentile line chart (aggregate over time)
    time_group = df.set_index('timeStamp').resample('10s')  # 10s buckets
    pct90_over_time = time_group['elapsed'].apply(lambda x: np.percentile(x, 90) if len(x) else np.nan)
    vusers_over_time = time_group['threadName'].nunique()

    # Human-readable times
    start_time_str = start_time.strftime('%Y-%m-%d %H:%M:%S')
    end_time_str = end_time.strftime('%Y-%m-%d %H:%M:%S')
    duration_str = str(duration)

    # Aggregate average response time
    avg_response_time = df['elapsed'].mean()

    # Overlay data for 90th percentile and virtual users
    df_overlay = pd.DataFrame({
        'time': pct90_over_time.index,
        'pct90_response': pct90_over_time.values,
        'vusers': vusers_over_time.values
    })

    summary = {
        "status": "success" if failed == 0 else "fail",
        "pass_pct": pass_pct,
        "fail_pct": fail_pct,
        "start_time": start_time_str,
        "end_time": end_time_str,
        "duration": duration,
        "avg_response_time": avg_response_time,
        "error_rate": error_rate,
        "agg_table": agg,
        "pct90_over_time": pct90_over_time,
        "vusers_over_time": vusers_over_time,
        "overlay_df": df_overlay,
    }
    add_jmeter_log(f"✅ Load test analysis complete: {summary['status']} ({passed}/{total_samples} passed)", agent_name="JMeterAgent")
    return summary 
