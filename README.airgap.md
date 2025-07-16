
# Airgapped Deployment Instructions

This document provides instructions for deploying the Shatiach application in an airgapped environment.

## 1. Load Docker Images

Load the Docker images from the `.tar` files:

```bash
docker load -i images/ollama.tar
docker load -i images/chroma.tar
docker load -i images/shatiach-api.tar
```

## 2. Prepare Ollama Models

In the airgapped environment, you will need to manually create the Ollama models.

First, start the Ollama service:

```bash
docker-compose up -d ollama
```

Then, from another terminal, copy the model files to the Ollama container and create the models:

```bash
# For qwen2.5:72b
docker cp /path/to/qwen2.5-72b.gguf ollama:/root/.ollama/models/qwen2.5-72b.gguf
ollama create qwen2.5:72b -f /root/.ollama/models/qwen2.5-72b.gguf

# For nomic-embed-text
docker cp /path/to/nomic-embed-text.gguf ollama:/root/.ollama/models/nomic-embed-text.gguf
ollama create nomic-embed-text -f /root/.ollama/models/nomic-embed-text.gguf
```

Repeat this for all the Ollama models you need.

## 3. Configure and Start the Application

Update the `docker-compose.yml` to use the local application image and set the environment variable for the local transcription model:

```yaml
services:
  api:
    image: shatiach-api:latest # Use the loaded image
    environment:
      - TRANSCRIPTION_MODEL_PATH=/app/models/whisper-large-v3
    # ... rest of the service definition
```

Now, start all the services:

```bash
docker-compose up -d
```
