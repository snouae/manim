
FROM python:3.12-slim


WORKDIR /app

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


RUN pip install --upgrade pip


COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt


COPY . .

# Set PYTHONPATH to include src for module imports
ENV PYTHONPATH=/app:/app/src:$PYTHONPATH

CMD ["bash"]