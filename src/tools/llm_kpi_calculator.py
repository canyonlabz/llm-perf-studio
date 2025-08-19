# Module to perform LLM KPI calculations
import pandas as pd
from typing import Optional, Union
from src.utils.event_logs import thread_safe_add_log

def read_llm_metrics_csv(csv_path: str, shared_data: dict, agent_name="LLMKPIAgent") -> pd.DataFrame:
    required_cols = [
        'timestamp', 'load_duration_ms', 'prompt_eval_duration_ms',
        'total_duration_ms', 'eval_count', 'eval_duration_ms'
    ]
    try:
        df = pd.read_csv(csv_path)
        if not all(col in df.columns for col in required_cols):
            missing = set(required_cols) - set(df.columns)
            msg = f"❌ Missing LLM metrics columns: {', '.join(missing)}"
            thread_safe_add_log(shared_data['logs'], msg, agent_name=agent_name)
            return pd.DataFrame()
        return df
    except Exception as e:
        msg = f"❌ Error reading LLM metrics CSV: {e}"
        thread_safe_add_log(shared_data['logs'], msg, agent_name=agent_name)
        return pd.DataFrame()

def calculate_ttft(load_duration_ms: Union[float, pd.Series], prompt_eval_duration_ms: Union[float, pd.Series]) -> Union[float, pd.Series]:
    """
    Calculate Time to First Token (TTFT) in milliseconds.
    TTFT = load_duration_ms + prompt_eval_duration_ms
    """
    return load_duration_ms + prompt_eval_duration_ms

def calculate_tps(eval_count: Union[int, pd.Series], total_duration_ms: Union[float, pd.Series]) -> Union[float, pd.Series]:
    """
    Calculate Tokens Per Second (TPS).
    TPS = eval_count / (total_duration_ms / 1000)
    Returns 0 if duration or eval_count is zero/invalid.
    """
    duration_sec = total_duration_ms / 1000
    if isinstance(eval_count, pd.Series):
        tps = eval_count.divide(duration_sec).replace([float('inf'), -float('inf')], 0)
        tps = tps.fillna(0)
    else:
        if eval_count != 0 and duration_sec > 0:
            tps = eval_count / duration_sec
        else:
            tps = 0
    return tps

def calculate_tpot(total_duration_ms: Union[float, pd.Series], ttft_ms: Union[float, pd.Series], eval_count: Union[int, pd.Series]) -> Union[float, pd.Series]:
    """
    Calculate Time Per Output Token (TPOT) in milliseconds per token.
    TPOT = (total_duration_ms - ttft_ms) / eval_count
    Returns 0 if eval_count is zero/invalid.
    """
    if isinstance(eval_count, pd.Series):
        valid_eval = eval_count != 0
        tpot = ((total_duration_ms - ttft_ms) / eval_count).where(valid_eval, 0).fillna(0)
    else:
        tpot = (total_duration_ms - ttft_ms) / eval_count if eval_count != 0 else 0
    return tpot

def compute_llm_kpis_from_metrics(metrics_df: pd.DataFrame) -> pd.DataFrame:
    """
    Given metrics DataFrame, compute TTFT, TPS, and TPOT per row.
    Returns DataFrame with new columns for each KPI.
    """
    metrics_df['TTFT'] = calculate_ttft(metrics_df['load_duration_ms'], metrics_df['prompt_eval_duration_ms'])
    metrics_df['TPS'] = calculate_tps(metrics_df['eval_count'], metrics_df['total_duration_ms'])
    metrics_df['TPOT'] = calculate_tpot(metrics_df['total_duration_ms'], metrics_df['TTFT'], metrics_df['eval_count'])
    return metrics_df

