
# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY pyproject.toml .

# Install any needed packages specified in pyproject.toml
RUN pip install --no-cache-dir "fastapi[all]" "uvicorn[standard]" "python-multipart" "whisper" "torch" "torchaudio" "agno" "chromadb" "ollama"

# Copy the rest of the application's code to the working directory
COPY . .

# Command to run the API
CMD ["uvicorn", "shatiach.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
