#!/bin/bash
set -e

IMAGE_NAME=shatiach-airgapbuild
CONTAINER_NAME=shatiach-airgapbuild-tmp
BUNDLE_DIR=airgap_bundle
PLATFORM=linux/amd64

echo "[INFO] Using platform: $PLATFORM (x86_64) for all build steps."
echo "[INFO] Mounting host Docker socket into container for Docker CLI access."

# 1. Build the Docker image
echo "[1/5] Building Docker image..."
docker build --platform=$PLATFORM -t $IMAGE_NAME -f Dockerfile.airgapbuild .

# 2. Remove any previous container
echo "[2/5] Cleaning up old container (if any)..."
docker rm -f $CONTAINER_NAME 2>/dev/null || true

# 3. Run the airgap bundle script in the container
echo "[3/5] Running airgap bundle script in container..."
docker run --platform=$PLATFORM --name $CONTAINER_NAME \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v $PWD:/workspace \
  $IMAGE_NAME \
  bash -c "./prepare_airgap_bundle.sh"

# 4. Copy the resulting bundle out (if not already present)
echo "[4/5] Copying airgap bundle to host (if needed)..."
if [ -d "$BUNDLE_DIR" ]; then
  rm -rf ${BUNDLE_DIR}-docker
  cp -r $BUNDLE_DIR ${BUNDLE_DIR}-docker
  echo "Copied $BUNDLE_DIR to ${BUNDLE_DIR}-docker on host."
else
  echo "No $BUNDLE_DIR found to copy."
fi

# 5. Clean up
echo "[5/5] Cleaning up container..."
docker rm -f $CONTAINER_NAME 2>/dev/null || true

echo "Airgap build complete. Bundle is in ${BUNDLE_DIR}-docker/ and tarball if created." 