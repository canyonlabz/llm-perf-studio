# Key Performance Indicators for LLM Performance Testing

This document defines the key performance indicators used by the LLM Performance Testing Framework and how to interpret them. It groups metrics into three layers—system load/performance (JMeter), LLM runtime/retrieval behavior (tokens, latency, throughput), and output quality (DeepEval)—and also outlines stage-specific KPIs across the pipeline (chunking, embedding, vector search, retrieval assembly). Use these KPIs to compare runs, detect regressions, and tune for both speed and quality under load.

---

## 1. JMeter Results (Load & Performance Metrics)

| Metric                  | Definition                                   | QA Performance Version                         | QA Functional Version                        |
|-------------------------|----------------------------------------------|------------------------------------------------|----------------------------------------------|
| **API Response Time**   | Min, Avg, Max, 90th percentile response times |
| **Concurrent Users**    | Max users system can handle concurrently     | Assesses system scalability, bottlenecks       | Ensures core features remain available under load |
| **Error Rate**          | % of failed or errored requests              | Reliability at scale/under stress              | Detects functional bugs, API misbehavior     |

---

## 2. LLM Metrics (LLM Inference)

| Metric                  | Definition                                   | QA Performance Version                         | QA Functional Version                        |
|-------------------------|----------------------------------------------|------------------------------------------------|----------------------------------------------|
| **Time To First Token (TTFT)** | Time from request sent to first token received (ms)              | Detects model/pipeline cold start or backend delays     | Ensures prompt is processed and model responds        |
| **Time Per Output Token (TPOT)** | Average time to generate each output token (ms/token)           | Surfaces generation slowdowns under load                | Verifies token streaming is functional                |
| **Tokens Per Second (TPS)**     | Output tokens generated per second (throughput)                 | Measures LLM throughput and scaling                     | Ensures output is not throttled or stuck              |
| **LLM Requests Per Second (RPS)** | Number of LLM requests processed per second                     | Indicates backend capacity and concurrency              | Verifies system can handle expected query volume       |

---

## 3. DeepEval Metrics (Output Quality & Correctness)

| Metric                        | Definition                                          | QA Performance Version                                 | QA Functional Version                                 |
|-------------------------------|-----------------------------------------------------|--------------------------------------------------------|-------------------------------------------------------|
| **Correctness GEval Score**   | 0 or 1 if actual==expected, strict string match     | Degradation in score may indicate failure under load    | Verifies step-by-step output meets requirements        |
| **Pass Rate**                 | % of answers matching ground truth                  | Drop indicates model or pipeline fails at high load     | Indicates overall capability of LLM for task           |
| **Strict Mode**               | Whether grading is exact match or tolerant          | Used to stress-test LLM under strict evaluation         | Used functionally to distinguish between minor/major errors |
| **Quality Degradation**       | Change in pass rate/GEval from baseline to load     | Measures if functional accuracy falls as load increases | Functional QA uses as regression signal in updates     |

---

## 4. Chunking (Segmentation)
- Chunking Duration (millisecond/document)
- Chunk Throughput (chunks/sec)

---

## 5. Embedding Generation
- Query Embedding Latency - Retrieval (Duration in ms.)
- Document Embedding Latency - Ingestion (Duration per chunk ms.)
- Embedding Throughput (Embeddings/sec)
- Embedding Error Rate (Failures/timeouts %)

---

## 6. Vector Query Search
- Query Latency - Search(latency ms.)
- QPS (Queries/second)
- Upsert Latency - Indexing (Duration to write vectors ms.)

---

## 7: Retrieval Assembly
- Assembly Latency (Duration of prompt assembly ms.)
- Tokens Assembled (Token count)
