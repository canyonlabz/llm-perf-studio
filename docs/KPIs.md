# 📊 Key Performance Indicators for LLM Performance Testing

This document defines the key performance indicators used by the LLM Performance Testing Framework and how to interpret them. It groups metrics into three layers—system load/performance (JMeter), LLM runtime/retrieval behavior (tokens, latency, throughput), and output quality (DeepEval)—and also outlines stage-specific KPIs across the pipeline (chunking, embedding, vector search, retrieval assembly). Use these KPIs to compare runs, detect regressions, and tune for both speed and quality under load.

---

## 1. ⚙️ JMeter Results (Load & Performance Metrics)

| Metric                  | Definition                                   | QA Performance Version                         | QA Functional Version                        |
|-------------------------|----------------------------------------------|------------------------------------------------|----------------------------------------------|
| ⏱️ **API Response Times**   | Min, Avg, Max, 90th percentile response times | Detects latency spikes, slowdowns, and tail-latency under load | Ensures endpoints respond within acceptable SLAs and user experience is not degraded |
| 👥 **Concurrent Users**    | Max users system can handle concurrently     | Assesses system scalability, bottlenecks       | Ensures core features remain available under load |
| ❌ **Error Rate**          | % of failed or errored requests              | Reliability at scale/under stress              | Detects functional bugs, API misbehavior     |

---

## 2. 🤖 LLM Metrics (LLM Inference)

| Metric                  | Definition                                   | QA Performance Version                         | QA Functional Version                        |
|-------------------------|----------------------------------------------|------------------------------------------------|----------------------------------------------|
| ⏳ **Time To First Token (TTFT)** | Time from request sent to first token received (ms)              | Detects model/pipeline cold start or backend delays     | Ensures prompt is processed and model responds        |
| ⚡ **Time Per Output Token (TPOT)** | Average time to generate each output token (ms/token)           | Surfaces generation slowdowns under load                | Verifies token streaming is functional                |
| 🚀 **Tokens Per Second (TPS)**     | Output tokens generated per second (throughput)                 | Measures LLM throughput and scaling                     | Ensures output is not throttled or stuck              |
| 📈 **LLM Requests Per Second (RPS)** | Number of LLM requests processed per second                     | Indicates backend capacity and concurrency              | Verifies system can handle expected query volume       |

---

## 3. 🧠 DeepEval Metrics (Output Quality & Correctness)

| Metric                        | Definition                                          | QA Performance Version                                 | QA Functional Version                                 |
|-------------------------------|-----------------------------------------------------|--------------------------------------------------------|-------------------------------------------------------|
| ✔️ **Correctness GEval Score**   | 0 or 1 if actual==expected, strict string match     | Degradation in score may indicate failure under load    | Verifies step-by-step output meets requirements        |
| 📊 **Pass Rate**                 | % of answers matching ground truth                  | Drop indicates model or pipeline fails at high load     | Indicates overall capability of LLM for task           |
| 🔍 **Strict Mode**               | Whether grading is exact match or tolerant          | Used to stress-test LLM under strict evaluation         | Used functionally to distinguish between minor/major errors |
| 📉 **Quality Degradation**       | Change in pass rate/GEval from baseline to load     | Measures if functional accuracy falls as load increases | Functional QA uses as regression signal in updates     |

---

## 4. 🧩 Chunking (Segmentation)
| Metric                        | Definition                                          | QA Performance Version                                 | QA Functional Version                                 |
|-------------------------------|-----------------------------------------------------|--------------------------------------------------------|-------------------------------------------------------|
| ⏱️ **Chunking Duration (millisecond/document)** | Time to split a document into semantic chunks. Impacts pipeline speed as file size grows. | Detects slowdowns in preprocessing as document size increases; helps identify bottlenecks in the chunking pipeline. | Ensures all documents are chunked correctly and within acceptable time for user experience or batch SLAs. |
| ⚙️ **Chunk Throughput (chunks/sec)** | Number of chunks created per second, reflecting scalability. Higher is better for batch/large-ingest. | Measures system's ability to handle large-scale or batch ingestion; higher throughput means better scalability. | Verifies all expected chunks are produced and no data is lost or skipped during segmentation. |

---

## 5. 💾 Embedding Generation
| Metric                        | Definition                                          | QA Performance Version                                 | QA Functional Version                                 |
|-------------------------------|-----------------------------------------------------|--------------------------------------------------------|-------------------------------------------------------|
| ⏲️ **Query Embedding Latency - Retrieval (Duration in ms.)** | Time to generate a vector for a user query. User sends a query or prompt that is embedded to search the stored vector. | Detects slowdowns in real-time search; high latency impacts user experience and E2E response time. | Ensures every query is embedded and returned within acceptable latency for interactive use. |
| ⏲️ **Document Embedding Latency - Ingestion (Duration per chunk ms.)** | Time to compute a vector from a chunk (often in batch). Affects ingest speed for content due to processing chunks to store in vector DB. | Measures batch processing speed for large ingests; identifies bottlenecks in content onboarding. | Verifies all chunks are embedded and stored; ensures no data loss or excessive delays during ingestion. |
| ⚡ **Embedding Throughput (Embeddings/sec)** | Chunks converted to vectors per second; higher means faster bulk processing. | Indicates system's ability to scale for large datasets; higher throughput means faster onboarding. | Confirms all expected embeddings are produced and stored; checks for completeness in batch jobs. |
| ❗ **Embedding Error Rate (Failures/timeouts %)** | Reliability of conversion; failures disrupt pipeline. | Tracks stability and robustness of embedding service under load; high error rates signal reliability issues. | Ensures all embeddings succeed or errors are handled gracefully; no silent data loss. |

---

## 6. 🔍 Vector Query Search
| Metric                        | Definition                                          | QA Performance Version                                 | QA Functional Version                                 |
|-------------------------------|-----------------------------------------------------|--------------------------------------------------------|-------------------------------------------------------|
| ⏱️ **Query Latency - Search (latency ms.)** | Time to complete a semantic search for top-k most similar vectors; higher means slow downstream context for LLM | Detects slowdowns in retrieval pipeline; high latency can bottleneck LLM response time and degrade user experience. | Ensures all search queries return results within acceptable latency; validates search is functional and not timing out. |
| 📊 **QPS (Queries/second)** | System capacity to handle vector searches. Parallel searches DB can serve—throughput for scale. | Measures backend throughput and scalability for concurrent search; higher QPS means better support for multi-user or batch workloads. | Verifies system can handle expected query volume without errors or dropped requests. |
| ⏲️ **Upsert Latency - Indexing (Duration to write vectors ms.)** | Time to store new vectors in the index. Ingest and index time for new vectors—affects content updates. | Surfaces bottlenecks in content update/refresh; high latency slows onboarding and retraining. | Ensures all new vectors are indexed and available for search promptly; validates no data loss or index corruption. |

---

## 7: 7️⃣ Retrieval Assembly
| Metric                        | Definition                                          | QA Performance Version                                 | QA Functional Version                                 |
|-------------------------------|-----------------------------------------------------|--------------------------------------------------------|-------------------------------------------------------|
| ⏲️ **Assembly Latency (Duration of prompt assembly ms.)** | Time to compile retrieved results into a prompt. Time to aggregate top-k chunks and package prompt for LLM; impacts E2E speed. | Detects bottlenecks in final prompt construction; high latency here slows E2E response even if retrieval is fast. | Ensures all required context is assembled and prompt is built correctly for LLM; validates no missing or duplicated content. |
| ⏲️ **Tokens Assembled (Token count)** | Total number of tokens added to the final prompt. Ensures prompt fits LLM context; overflow slows or fails LLM inference. Assembled via top-k chunks into prompt. | Monitors prompt size for context overflow; helps tune chunking and retrieval to avoid exceeding LLM limits. | Verifies prompt fits within LLM context window and contains all necessary information; prevents truncation or errors. |
