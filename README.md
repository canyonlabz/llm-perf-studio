# LLM Performance Testing Framework

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
│ • Test Config   │───▶│ • Load Testing  │───▶│ • Ollama/OpenAI │
│ • Monitoring    │    │ • Metrics       │    │ • Local/Cloud   │
│ • Results       │    │ • Logging       │    │ • RAG Enabled   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │              ┌─────────────────┐              │
         └─────────────▶│  DeepEval QA    │◀─────────────┘
                        │                 │
                        │ • Correctness   │
                        │ • Quality Score │
                        │ • Category Test │
                        └─────────────────┘
```

## 📋 Prerequisites

- **Python 3.8+**
- **Apache JMeter 5.6.3+**
- **Java 8+** (for JMeter)
- **Ollama** (for local model testing)
- **OpenAI API Key** (for OpenAI testing)

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/llm-perf-testing.git
   cd llm-perf-testing
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install JMeter:**
   - Download from [Apache JMeter](https://jmeter.apache.org/download_jmeter.cgi)
   - Extract to `C:\opt\apache-jmeter-5.6.3\` (Windows) or `/opt/apache-jmeter-5.6.3/` (Linux/Mac)

4. **Configure environment:**
   ```bash
   cp config/config.yaml.example config/config.yaml
   # Edit config.yaml with your settings
   ```

5. **Set up Ollama (optional):**
   ```bash
   # Install Ollama
   curl -fsSL https://ollama.ai/install.sh | sh
   
   # Pull a model
   ollama pull llama3.2:1b
   ```

## ⚙️ Configuration

### Main Configuration (`config/config.yaml`)

```yaml
llm_services:
  ollama:
    base_url: "http://localhost:11434"
    model: "llama3.2:1b"
    timeout: 30
  
  openai:
    api_key: "${OPENAI_API_KEY}"
    model: "gpt-3.5-turbo"
    timeout: 30

jmeter:
  bin_path: "C:/opt/apache-jmeter-5.6.3/bin"
  test_plan: "jmeter/llm_load_test.jmx"
  
deepeval:
  evaluator_model: "gpt-4"
  correctness_threshold: 0.7
```

### Environment Variables

```bash
# .env file
OPENAI_API_KEY=your_openai_api_key_here
DEEPEVAL_API_KEY=your_deepeval_api_key_here
```

## 🚀 Quick Start

1. **Start the dashboard:**
   ```bash
   streamlit run streamlit_ui.py
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
llm-perf-testing/
├── config/
│   ├── config.yaml              # Main configuration
│   └── prompts/                 # Test prompt datasets
├── docs/
│   ├── KPIs.md                 # Key Performance Indicators
│   └── architecture.md         # System architecture
├── jmeter/
│   ├── llm_load_test.jmx       # JMeter test plan
│   └── test_results/           # Generated test results
├── src/
│   ├── tools/
│   │   ├── jmeter_executor.py  # JMeter integration
│   │   └── deepeval_assessment.py # Quality assessment
│   ├── ui/
│   │   ├── page_body.py        # Main UI components
│   │   └── page_styles.py      # UI styling
│   └── utils/
│       ├── config.py           # Configuration management
│       └── test_state.py       # Test state management
├── streamlit_ui.py             # Main application entry
└── requirements.txt            # Python dependencies
```

## 🔧 Usage Examples

### Basic Load Test

```python
# Configure test parameters
test_config = {
    "vusers": 10,
    "ramp_up": 30,
    "duration": 300,
    "llm_mode": "ollama",
    "model": "llama3.2:1b"
}

# Run via UI or programmatically
results = run_jmeter_test(test_config)
```

### Quality Assessment

```python
# Run DeepEval analysis on responses
quality_results = analyze_response_quality(
    responses_file="test_responses.json",
    test_cases="prompts/ai_knowledge_qa.json"
)

print(f"Overall accuracy: {quality_results['pass_rate']}%")
```

### Combined Performance + Quality

```python
# Full workflow
perf_results = run_load_test(config)
quality_results = assess_quality(perf_results['responses'])

# Analyze correlation
analyze_performance_quality_correlation(
    perf_results, quality_results
)
```

## 📈 Sample Results

### Performance Test Results
- **Test Duration**: 5 minutes
- **Virtual Users**: 10 concurrent
- **Total Requests**: 1,247
- **Average Response Time**: 2.3 seconds
- **90th Percentile**: 4.1 seconds
- **Error Rate**: 0.2%

### Quality Assessment Results
- **Total Test Cases**: 25
- **Overall Accuracy**: 40%
- **Best Category**: Pre-trained Models (100%)
- **Worst Category**: AI Technologies (0%)
- **Evaluation Cost**: $0.04

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit changes (`git commit -am 'Add new feature'`)
4. Push to branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: Check the `docs/` directory
- **Issues**: Report bugs via GitHub Issues
- **Discussions**: Use GitHub Discussions for questions

## 🔮 Roadmap

- [ ] Support for additional LLM providers (Anthropic, Cohere)
- [ ] Advanced RAG testing capabilities
- [ ] Automated performance regression detection
- [ ] Integration with CI/CD pipelines
- [ ] Custom quality metrics framework
- [ ] Multi-region load testing support

## 📚 Related Projects

- [Apache JMeter](https://jmeter.apache.org/) - Load testing framework
- [DeepEval](https://github.com/confident-ai/deepeval) - LLM evaluation framework
- [Ollama](https://ollama.ai/) - Local LLM runtime
- [Streamlit](https://streamlit.io/) - Web app framework

---

**Built with ❤️ for the LLM testing community**