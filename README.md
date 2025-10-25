# LLM Performance Test Studio

> **⚠️ This project is under active development. Features, modules, and documentation may change frequently. Use at your own risk and please report any issues or suggestions!**

A comprehensive framework for load testing Large Language Models (LLMs) with integrated quality assessment using JMeter and DeepEval.

## 🚀 Overview

This framework combines traditional load testing with AI-specific quality metrics to provide a complete performance evaluation of LLM services. It supports testing both local models (via Ollama) and cloud-based APIs (OpenAI) while measuring both performance and response quality under load.

## ✨ Key Features

- **Dual Testing Approach**: Load testing with JMeter + Quality assessment with DeepEval
- **Multi-LLM Support**: Ollama (local models) and OpenAI API compatibility
- **Real-time Monitoring**: Live dashboard with performance metrics and logs
- **Quality Under Load**: Track accuracy degradation as load increases
- **Comprehensive Metrics**: TTFT, TPOT, TPS, and traditional HTTP metrics
- **Interactive UI**: Streamlit-based dashboard for test management
- **RAG Support**: Test Retrieval-Augmented Generation workflows

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Streamlit UI  │    │  JMeter Engine  │    │  LLM Service    │
│                 │    │                 │    │                 │
│ • Test Config   │──▶│ • Load Testing  │───▶│ • Ollama/OpenAI │
│ • Monitoring    │    │ • Metrics       │    │ • Local/Cloud   │
│ • Results       │    │ • Logging       │    │ • RAG Enabled   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                      │
         │             ┌─────────────────┐              │
         └───────────▶│  DeepEval QA    │ ◀────────────┘
                       │                 │
                       │ • Correctness   │
                       │ • Quality Score │
                       │ • Category Test │
                       └─────────────────┘
```

## 📋 Prerequisites

- **Python 3.12+**
- **Apache JMeter 5.6.3+**
- **Java OpenJDK 22+** (*for JMeter*)
- **Ollama** (*optional: for local model testing*)
- **OpenAI API Key** (*optional: for OpenAI testing*)

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/canyonlabz/llm-perf-studio.git
   cd llm-perf-studio
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install JMeter:**
   - Download from [Apache JMeter](https://jmeter.apache.org/download_jmeter.cgi)
   - Extract locally to folder of your choice. Example: `C:\opt\apache-jmeter-5.6.3\` (Windows) or `/opt/apache-jmeter-5.6.3/` (Linux/Mac)

4. **Configure environment:**
   ```bash
   cp config.yaml.example config.yaml
   # Edit config.yaml with your settings
   ```
   You can create a `config.windows.yaml` or `config.mac.yaml` file depending on your operating system.
   The OS-specific YAML file will override the default `config.yaml` settings.
5. **Set up Ollama (optional):**
   ```bash
   # Install Ollama
   curl -fsSL https://ollama.ai/install.sh | sh
   
   # Pull a model
   ollama pull llama3.2:1b
   ```

## ⚙️ Configuration

### Main Configuration (`~/config.yaml`)

> 💡 **Note:** For a full breakdown of available configuration options and advanced usage, check out [docs/configuration.md](docs/configuration.md).

**Example:**
```yaml
ollama:
   base_url: "http://localhost:11434"
   model: "llama3.2:1b"
   timeout: 30
  
openai:
   model: "gpt-5-mini"
   timeout: 30

jmeter:
  bin_path: "C:/{{jmeter_path}}/apache-jmeter-5.6.3/bin"

deepeval:
  evaluator_model: "gpt-4"
  correctness_threshold: 0.7
```

### Environment Variables

```bash
# .env file
OPENAI_API_KEY=your_openai_api_key_here
```

## 🚀 Quick Start

1. **Start the dashboard:**
   ```bash
   python app.py
   ```

2. **Configure your test:**
   - Select LLM service (Ollama/OpenAI)
   - Set load parameters (users, duration, ramp-up)
   - Choose test data and RAG settings

3. **Run performance test:**
   - Click "Start JMeter Test"
   - Monitor real-time logs and metrics
   - View live performance charts

4. **Quality assessment:**
   - Navigate to "Quality Assessment" tab
   - Run DeepEval analysis on test responses
   - Review quality scores and categorized results

## 📊 Metrics & KPIs

### Performance Metrics
- **Response Time**: Average, Min, Max, 90th percentile
- **Throughput**: Requests per second
- **Error Rate**: Failed requests percentage
- **Concurrent Users**: Virtual user load over time

### LLM-Specific Metrics
- **TTFT**: Time to First Token
- **TPOT**: Time Per Output Token  
- **TPS**: Tokens Per Second
- **Token Counts**: Input/Output token statistics

### Quality Metrics
- **Correctness Score**: DeepEval accuracy assessment
- **Category Performance**: Domain-specific quality tracking
- **Quality Under Load**: Accuracy vs load correlation

## 📁 Project Structure

```
llm-perf-studio/
│   app.py
│   config.yaml
│   LICENSE
│   README.md
│   requirements.txt
│
├───data
│       ISTQB_CT-AI_SampleExam-Answers_v1.0.pdf
│       ISTQB_CT-AI_SampleExam-Questions_v1.0.pdf
│
├───docker
│       docker-compose.yml
│
├───docs
|       analysis.md
|       docker.md
│       kpis.md
│
├───jmeter
│   │   llm-ollama.jmx
│   │   llm-openai.jmx
│   │
│   ├───testdata_csv
│   │       environment_ollama.csv
|   |       environment_openai.csv
│   │       README.md
│   │
│   └───testdata_json
│           ISTQB_Final_Questions_Answers.json
└───src
    │
    ├───services
    │       chat_service.py     (Class for LLM chatbot)
    │
    ├───tools
    │   │   deepeval_assessment.py              (Agent Tool for DeepEval quality assessment)
    │   │   jmeter_executor.py                  (Agent tool for JMeter test execution)
    │   └   llm_kpi_calculations.py             (Agent Tool for calculating LLM KPI metrics)
    │
    ├───ui
    │   │   page_body_*.py  (page body rendering)
    │   │   page_header.py  (page headers rendering)
    │   │   page_styles.py  (page CSS style rendering)
    │   │   page_title.py   (page title rendering)
    │   │   page_utils.py   (page utility functions)
    │   │   streamlit_ui.py (page rendering function for all components)
    │   │   ui_handlers.py  (page UI handler functions)
    │   │
    │   └───nav_pages
    │       page_*.py       (Streamlit Pages)
    │
    └───utils
            Common Utilities
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit changes (`git commit -am 'Add new feature'`)
4. Push to branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## 📝 License

This project is licensed under the BSD-3-Clause License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: Check the `docs/` directory
- **Issues**: Report bugs via GitHub Issues
- **Discussions**: Use GitHub Discussions for questions

## 🔮 Roadmap

- [ ] Support for additional LLM providers (Anthropic, Google, etc.)
- [ ] Full RAG support for custom datasets
- [ ] Docker-based containerization for cross-platform, OS-agnostic deployment
- [ ] Additional DeepEval quality metrics
- [X] De-couple LLM calculations from JMeter to Python tools. 

## 📚 Related Projects

- [Apache JMeter](https://jmeter.apache.org/) - Load and performance testing tool for web applications and other services.
- [DeepEval](https://github.com/confident-ai/deepeval) - LLM evaluation framework and platform for testing and evaluating large language models (LLMs).
- [Ollama](https://ollama.ai/) - Ollama is an open-source platform that lets you run large language models on your device.
- [ChromaDB](https://docs.trychroma.com/docs/overview/introduction) - Open-source vector database tailored to applications with large language models.
- [OpenWebUI](https://docs.openwebui.com/) - Extensible, feature-rich, and user-friendly self-hosted AI platform designed to operate entirely offline.
- [Streamlit](https://streamlit.io/) - Open-source Python framework for data scientists and AI/ML engineers to deliver interactive data apps.
- [Docker](https://www.docker.com/) - Docker is a tool that helps developers build, share, run, and verify applications using containers.
- [Unstructured](https://github.com/Unstructured-IO/unstructured-api) - Core library for partitioning, cleaning, and chunking 25+ documents types for LLM applications and connecting to source and destination data source.

## Author ✍️

**Jason Smallcanyon | [CanyonLabz, LLC](https://canyonlabz.com/)**

---

**Built with ❤️ for the LLM performance testing community**
