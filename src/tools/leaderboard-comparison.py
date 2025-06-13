'''
**Performance Reporting:**
- Create dual-axis charts showing:
  - Token throughput vs response quality
  - Latency distribution across question types
  - Resource utilization correlation with model accuracy

### 2. Leaderboard Integration Strategy

**Recommended Leaderboards:**
| Leaderboard               | Key Metrics       | Integration Method           |
|---------------------------|-------------------|------------------------------|
| Hugging Face Open LLM     | MMLU, TruthfulQA  | Replicate benchmarks locally |
| SEAL Humanity's Last Exam | Complex reasoning | API submission               |
| LMSYS Chatbot Arena       | Elo ratings       | Docker deployment            |

1. https://www.deeplearning.ai/the-batch/hugging-face-introduces-leaderboards-to-evaluate-model-performance-and-trustworthiness/
2. https://huggingface.co/collections/open-llm-leaderboard/the-big-benchmarks-collection-64faca6335a7fc7d4ffe974a
3. https://scale.com/leaderboard
4. https://datasciencedojo.com/blog/understanding-llm-leaderboards/
5. https://www.reddit.com/r/machinelearningnews/comments/1dptx9n/hugging_face_releases_open_llm_leaderboard_2_a/
'''
# Hugging Face Open LLM Leaderboard Token KPI Comparison Script
# This script fetches token KPIs from the Hugging Face Open LLM Leaderboard
import requests
class HuggingFaceLeaderboard:
    """
    Class to interact with Hugging Face Open LLM Leaderboard for token KPIs.
    """
    def __init__(self):
        self.base_url = "https://huggingface.co/api/leaderboards/open-llm"

    def get_token_kpis(self, model_name):
        """
        Fetch token KPIs for a given model from Hugging Face leaderboard.

        Args:
            model_name (str): Name of the model to fetch KPIs for

        Returns:
            dict: Token KPIs including TTFT, TPS, TPOT
        """
        response = requests.get(f"{self.base_url}/{model_name}/token-kpis")
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to fetch KPIs for {model_name}: {response.status_code} {response.text}")

# Compare local LLM token KPIs against Hugging Face leaderboard metrics
def compare_token_kpis(local_kpis, model_name):
    """
    Compare local LLM token KPIs against Hugging Face leaderboard metrics.

    Args:
        local_kpis (dict): Local KPIs, e.g. {"TTFT": 0.8, "TPS": 45.2, "TPOT": 0.022}
        model_name (str): Name of the model to compare on the leaderboard

    Returns:
        dict: Comparison results for each KPI
    """
    hf_leaderboard = HuggingFaceLeaderboard()
    leaderboard_kpis = hf_leaderboard.get_token_kpis(model_name)

    comparison = {}
    for kpi in ["TTFT", "TPS", "TPOT"]:
        local_value = local_kpis.get(kpi)
        leaderboard_value = leaderboard_kpis.get(kpi)
        if local_value is not None and leaderboard_value is not None:
            comparison[kpi] = {
                "local": local_value,
                "leaderboard": leaderboard_value,
                "delta": local_value - leaderboard_value
            }
        else:
            comparison[kpi] = {
                "local": local_value,
                "leaderboard": leaderboard_value,
                "delta": None
            }
    return comparison

# Example usage
if __name__ == "__main__":
    # Example local KPI metrics
    local_kpis = {
        "TTFT": 0.75,    # seconds
        "TPS": 50.0,     # tokens per second
        "TPOT": 0.02     # seconds per token
    }
    model_name = "meta-llama/Llama-3-8b-chat-hf"
    results = compare_token_kpis(local_kpis, model_name)
    print("Token KPI Comparison:")
    for kpi, values in results.items():
        print(f"{kpi}: Local={values['local']}, Leaderboard={values['leaderboard']}, Delta={values['delta']}")
