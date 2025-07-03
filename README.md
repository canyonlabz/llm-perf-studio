## 🧪 LLM Performance Testing Framework

A modern, extensible proof-of-concept for performance and quality assessment of Large Language Models (LLMs) using automated load testing, token-level metrics, and advanced response evaluation. Easily benchmark your LLMs, compare results to industry leaderboards, and visualize performance trends—all in a Dockerized, open, and reproducible environment.

---

### 🚀 Features

- **Automated Load Testing:** JMeter-driven tests send curated prompts to your LLM, simulating real-world usage at scale.
- **Live, Responsive UI:** Streamlit-based dashboard with real-time JMeter logs and test status updates, powered by background threading and auto-refresh.
- **Token Utilization Metrics:** Capture Time to First Token (TTFT), Tokens per Second (TPS), and Time per Output Token (TPOT) for deep performance insights.
- **Quality Assessment:** Analyze LLM responses against ground truth using DeepEval for objective scoring.
- **RAG Support:** Integrate ChromaDB for Retrieval-Augmented Generation with your own PDF-based Q&A datasets.
- **Leaderboard Comparison:** (Planned) Benchmark your local LLM’s quality scores against Hugging Face and other public leaderboards.
- **Modern UI:** Manage and interact with your LLM stack via OpenWebUI.
- **Fully Containerized:** One-command setup with Docker Compose for rapid deployment and reproducibility.
- **BSD 2-Clause Licensed:** Open source, permissive, and ready for community contributions.

---

### 📦 Technology Stack

| Component                 | Purpose                                                   |
|---------------------------|-----------------------------------------------------------|
| Streamlit                 | Custom UI for live logs, test control, and dashboards     |
| streamlit-autorefresh     | Enables real-time log and status updates in the UI        |
| Ollama                    | LLM backend & API interface                               |
| llama3.2:1b               | Default LLM model (swap for any Ollama-supported model)   |
| ChromaDB                  | Vector database for RAG, PDF ingestion                    |
| OpenWebUI                 | Web-based LLM management UI                               |
| JMeter                    | Load generation, metrics capture, and test orchestration  |
| DeepEval                  | Python-based quality assessment framework                 |
| Docker Compose            | Orchestration and persistent environment setup            |
| Threading (Python)        | Background task execution for non-blocking UI             |

---

### 🗂️ Project Structure

```plaintext
LLM-PERF-TESTING/
│   demo-llm-llama3-2-1b.jmx
│   LICENSE
│   README.md
│
├───docker-compose/
│       docker-compose.yml
│
├───testdata_csv/
│       environment.csv
│       README.md
│
├───testdata_files/
│       ISTQB_CT-AI_SampleExam-Answers_v1.0.pdf
│       ISTQB_CT-AI_SampleExam-Questions_v1.0.pdf
│
├───testdata_json/
│       ISTQB_Final_Questions_Answers.json
│
├───test_results/
│       _llm-test-results.csv
│       _llm-test-results.jtl
│       _llm_responses.json
│
└───tools/
        deepeval_assessment.py
```

---

### ⚡ Quick Start

#### **Prerequisites**

- [Docker](https://www.docker.com/get-started) and [Docker Compose](https://docs.docker.com/compose/) installed
- Python 3.10+ (for running Streamlit UI and analysis scripts)


#### **Setup and Usage**

1. **Clone the repo**

```bash
git clone https://github.com/yourusername/llm-perf-testing.git
cd llm-perf-testing
```

2. **Install Python dependencies**

```bash
pip install -r requirements.txt
```

3. **Spin up the stack**

```bash
docker-compose -f docker-compose/docker-compose.yml up
```

4. **Run the Streamlit UI**

```bash
streamlit run src/ui/page_body.py
```

5. **Run a performance test**

```bash
jmeter -n -t demo-llm-llama3-2-1b.jmx
```

6. **Assess quality**

```bash
python src/tools/deepeval_assessment.py
```

7. **(Planned) Compare with Leaderboards**
    - Automated scripts (coming soon!) to benchmark your results against Hugging Face and other public leaderboards.

### 📊 Metrics Captured

- **Time to First Token (TTFT)**
- **Tokens per Second (TPS)**
- **Time per Output Token (TPOT)**
- **DeepEval Quality Score**


### 📝 Contributing

Contributions, issues, and feature requests are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

### 📄 License

BSD 2-Clause License (see [LICENSE](LICENSE) for details).

### 🙏 Acknowledgments

- [Streamlit](https://streamlit.io/)
- [streamlit-autorefresh](https://github.com/streamlit/streamlit-autorefresh)
- [Ollama](https://ollama.com/)
- [ChromaDB](https://www.trychroma.com/)
- [OpenWebUI](https://github.com/open-webui/open-webui)
- [JMeter](https://jmeter.apache.org/)
- [DeepEval](https://github.com/confident-ai/deepeval)
- [Hugging Face Leaderboard](https://huggingface.co/spaces/open-llm-leaderboard)

> 💡 **Tip:** Use your own PDF datasets for custom RAG testing. Swap in any Ollama-supported LLM for broader benchmarking.

### 🌟 Stay tuned for leaderboard integration, advanced visualizations, and more!

*Made with ❤️ for the LLM community.*