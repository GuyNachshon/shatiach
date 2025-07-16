
#!/bin/bash

# Create directories for the airgap package
mkdir -p airgap/images
mkdir -p airgap/packages
mkdir -p airgap/models

# Download Python packages
pip download -r requirements.txt -d airgap/packages

# Download the Whisper model
GIT_LFS_SKIP_SMUDGE=1 git clone https://huggingface.co/ivrit-ai/whisper-large-v3 airgap/models/whisper-large-v3
(cd airgap/models/whisper-large-v3 && git lfs pull)

# Download Docker images
docker pull ollama/ollama
docker save ollama/ollama -o airgap/images/ollama.tar

docker pull chromadb/chroma
docker save chromadb/chroma -o airgap/images/chroma.tar

# Build and save the application image
docker build -t shatiach-api -f airgap.Dockerfile .
docker save shatiach-api -o airgap/images/shatiach-api.tar

echo "Airgap package created in the 'airgap' directory."
