# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies and Supervisor
RUN apt-get update && apt-get install -y supervisor && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your application code into the container
COPY . .

# Create logs directory (make sure Supervisor can write logs)
RUN mkdir -p /app/logs

# Copy the Supervisor configuration file into the container
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Expose ports for FastAPI (8000) and Streamlit (8501)
EXPOSE 8000 8501

# Run Supervisor when the container launches
CMD ["/usr/bin/supervisord", "-n"]
