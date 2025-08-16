# 📦 Docker Containers for LLM Perf Testing: Best Practices \& Usage Guide

Welcome! This document provides a quick and practical guide for managing your Docker containers—Ollama, ChromaDB, and OpenWebUI—used in your LLM performance testing setup. It covers how to start, stop, update, and troubleshoot your containers, plus tips about networking, storage, and configuration.

***

## 🚀 1. Starting All Containers

Start all three containers together by running:

```bash
docker-compose -f docker-compose.yml up
```

- Runs containers in the foreground with logs visible.
- Use `Ctrl+C` to stop.
- You can also run in detached mode (`-d`) to run containers in the background.

***

## 🛑 2. Stopping Containers

To stop \& remove all running containers defined in the compose file:

```bash
docker-compose down
```

- This removes containers but preserves data volumes for persistence.

***

## 🆕 3. Best Practices for Updating Docker Images

Keep your images up-to-date with these steps:

1. Stop containers:

```bash
docker-compose down
```

2. Pull updated images for all or specific services:

```bash
docker-compose pull
# or
docker-compose pull open-webui ollama chromadb
```

3. Restart containers to use updated images:

```bash
docker-compose -f docker-compose.yml up
```


**Tips:**

- Pull images while containers are stopped for a clean update.
- Specify explicit version tags (e.g., `v0.6.22`) in your compose file for repeatable environments.
- Avoid relying solely on `latest` to prevent unexpected breaking changes.

***

## 🔐 4. Logging into OpenWebUI

- Access the UI at: [http://localhost:3000](http://localhost:3000)
- Initially, OpenWebUI loads the default model (e.g., `llama3.2:1b`).
- After updating, you can select/download newer models like `gemma3.4b`.
- Use the Settings page to customize connections and behavior.

***

## 🐞 5. Troubleshooting OpenWebUI Issues

### Common OpenAI API Key Error

If you see errors like:

```
Exception: External Error: {'message': "Incorrect API key provided: ''...", 'code': 'invalid_api_key'}
```

**Resolution:**

- Go to **Settings → Connections**.
- Disable the OpenAI API Integration if you don’t have a valid API key or don’t need OpenAI services.
- This stops OpenWebUI from attempting unauthorized requests.


### Additional Tips

- Check logs anytime with:

```bash
docker-compose logs open-webui
```

- To access the Ollama container shell for manual commands:

```bash
docker exec -it ollama bash
```


***

## 🌐 6. Networking and Dependencies

- All three containers connect to a Docker user-defined bridge network called **`appnet`**.
- This allows seamless container-to-container communication via container names as hostnames (e.g., `ollama`, `chromadb`).
- In `docker-compose.yml`, **`depends_on`** ensures `ollama` and `chromadb` start before `open-webui`, guaranteeing backend services are ready before the UI launches.

***

## 💾 7. Persistent Storage

Data persistence is critical for your testing:

- Docker volumes are used to persist container data outside the lifecycle of individual containers.
- Example in `docker-compose.yml`:

```yaml
volumes:
  - ./data/ollama:/root/.ollama
  - ./data/chromadb:/chroma/chroma
  - ./data/open-webui:/app/backend/data
```

- This ensures data such as models, database files, and UI settings are retained across container restarts and updates.

**Best Practices:**

- Use **named volumes** or bind mounts pointing to project directories for easy backups.
- Regularly back up important data folders in your host machine.
- Avoid storing persistent data inside containers directly to prevent loss.

***

## ⚙️ 8. Environment Variable Configuration

Several environment variables configure behavior of your containers:

- Defined in `docker-compose.yml` under each service’s `environment` section.
- Examples:
    - `OLLAMA_BASE_URL=http://ollama:11434`
    - `CHROMA_HTTP_HOST=chromadb`
    - `VECTOR_DB=chroma`
    - `RAG_EMBEDDING_ENGINE=ollama`
    - `WEBUI_NAME=LLM PerfTest ChatBot`
    - `CORS_ALLOW_ORIGIN=*` (not recommended for production)
- Modify or add variables here to adjust behavior, enable debugging, or switch models.
