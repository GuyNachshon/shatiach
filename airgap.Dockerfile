
# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the bundled packages to the container
COPY ./packages /app/packages

# Install the dependencies from the local packages
RUN pip install --no-index --find-links=/app/packages -r /app/packages/requirements.txt

# Copy the rest of the application's code to the working directory
COPY . .

# Command to run the API
CMD ["uvicorn", "shatiach.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
