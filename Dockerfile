# Use the official slim Python image
FROM python:3.13-slim

# Set a working directory
WORKDIR /app

# Install any system dependencies (if needed for certain packages)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your application code into the container
COPY . .

# (Optional) expose a port if your agent serves a web interface
# EXPOSE 8000

CMD ["bash"]
