#!/bin/bash
set -e

# --- CONFIG ---
PYTHON_REQ=requirements.txt
PYTHON_OUT=airgap_bundle/python_packages
NODE_DIR=frontend/vue-project
NODE_OUT=airgap_bundle/node_modules
NODE_PKG_OUT=airgap_bundle
DOCKER_IMG_DIR=airgap_bundle/images
MODELS_SRC=airgap_bundle/models
MODELS_OUT=airgap_bundle/models

# --- PREP ---
echo "[1/6] Creating directories..."
mkdir -p "$PYTHON_OUT" "$DOCKER_IMG_DIR" "$MODELS_OUT"

# --- PYTHON ---
echo "[2/6] Downloading Python packages..."
pip download -r "$PYTHON_REQ" -d "$PYTHON_OUT"

# --- NODE ---
echo "[3/6] Installing and bundling Node packages..."
cd "$NODE_DIR"
npm install --ignore-scripts
cd - > /dev/null
rm -rf "$NODE_OUT"
cp -r "$NODE_DIR/node_modules" "$NODE_OUT"
cp "$NODE_DIR/package.json" "$NODE_PKG_OUT/"
cp "$NODE_DIR/package-lock.json" "$NODE_PKG_OUT/"

# --- DOCKER ---
echo "[4/6] Building and saving Docker images..."
# Backend API image
if [[ -f Dockerfile ]]; then
  docker build -t shatiach-api:latest -f Dockerfile .
  docker save -o "$DOCKER_IMG_DIR/shatiach-api.tar" shatiach-api:latest
else
  echo "Dockerfile not found, skipping shatiach-api image build."
fi
# Save other required images (edit as needed)
# docker save -o "$DOCKER_IMG_DIR/other_image.tar" other_image:tag

# --- MODELS & DATA ---
echo "[5/6] Copying models and data..."
# Copy models if not already present (edit as needed)
if [[ -d "$MODELS_SRC" ]]; then
  rsync -a --ignore-existing "$MODELS_SRC/" "$MODELS_OUT/"
fi

# --- CODE ---
echo "[6/7] Copying application code into bundle..."
mkdir -p airgap_bundle/code
cp -r shatiach airgap_bundle/code/
cp -r frontend airgap_bundle/code/
# Add any other directories as needed

echo "[7/7] Creating airgap tarball..."
tar czvf shatiach_airgap_bundle.tar.gz airgap_bundle/

echo "Airgap bundle (including code) is in shatiach_airgap_bundle.tar.gz"

# --- DONE ---
echo "[6/6] Airgap bundle prepared in airgap_bundle/"
echo "Python wheels: $PYTHON_OUT"
echo "Node modules: $NODE_OUT"
echo "Docker images: $DOCKER_IMG_DIR"
echo "Models/data: $MODELS_OUT" 