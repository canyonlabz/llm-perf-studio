

---

## 1. JMeter Results (Load & Performance Metrics)

| Metric                  | Definition                                   | QA Performance Version                         | QA Functional Version                        |
|-------------------------|----------------------------------------------|------------------------------------------------|----------------------------------------------|
| **Concurrent Users**    | Max users system can handle concurrently     | Assesses system scalability, bottlenecks       | Ensures core features remain available under load |
| **Error Rate**          | % of failed or errored requests              | Reliability at scale/under stress              | Detects functional bugs, API misbehavior     |

---

## 2. LLM Metrics (Runtime & Retrieval KPIs)

| Metric                  | Definition                                   | QA Performance Version                         | QA Functional Version                        |
|-------------------------|----------------------------------------------|------------------------------------------------|----------------------------------------------|
| **Token Utilization**   | How many tokens are used per request         | Reveals efficiency and cost scaling            | Ensures all input/outputs are processed      |
| **Query Latency P95**   | 95th percentile retrieval latency (ms)       | Surfaces tail-latency or spikes under load     | Ensures search/retrieval functionality isn't slow |
| **Queries Per Second (QPS)** | Maximum similarity searches per sec  | Measures backend throughput under high access  | Verifies ability to handle user queries timely|
| **Embedding Latency**   | Time to create embedding from input (ms)     | Shows bottlenecks in pipeline, especially for streamed/real-time scenarios | Ensures feature (embedding) works for each case |
| **Context Relevance**   | Proportion of retrieved context useful to LLM| Monitors degradation under pipeline stress     | Verifies context selection is functionally correct |
| **Similarity Score**    | Cosine similarity between query & retrieved  | Used to tune search/indexing for speed vs. accuracy | Validates retrieval quality                  |

---

## 3. DeepEval Metrics (Output Quality & Correctness)

| Metric                        | Definition                                          | QA Performance Version                                 | QA Functional Version                                 |
|-------------------------------|-----------------------------------------------------|--------------------------------------------------------|-------------------------------------------------------|
| **Correctness GEval Score**   | 0 or 1 if actual==expected, strict string match     | Degradation in score may indicate failure under load    | Verifies step-by-step output meets requirements        |
| **Pass Rate**                 | % of answers matching ground truth                  | Drop indicates model or pipeline fails at high load     | Indicates overall capability of LLM for task           |
| **Strict Mode**               | Whether grading is exact match or tolerant          | Used to stress-test LLM under strict evaluation         | Used functionally to distinguish between minor/major errors |
| **Quality Degradation**       | Change in pass rate/GEval from baseline to load     | Measures if functional accuracy falls as load increases | Functional QA uses as regression signal in updates     |

---
