# Use Python 3.12 slim base image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies for Manim, LaTeX, Pango, PyAudio, and other requirements
RUN apt-get update && apt-get install -y \
    build-essential \
    libcairo2-dev \
    pkg-config \
    python3-dev \
    texlive \
    texlive-latex-extra \
    texlive-fonts-extra \
    libpango1.0-dev \
    libpangocairo-1.0-0 \
    ffmpeg \
    portaudio19-dev \  
&& rm -rf /var/lib/apt/lists/*

# Upgrade pip first
RUN pip install --upgrade pip

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Set PYTHONPATH to include src for module imports
ENV PYTHONPATH=/app:/app/src:$PYTHONPATH

# Default command to keep container running
CMD ["bash"]