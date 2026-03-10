FROM python:3.9.7-slim-buster

ENV DEBIAN_FRONTEND=noninteractive

# Replace sources.list with archive.debian.org for Buster
RUN sed -i 's|http://deb.debian.org/debian|http://archive.debian.org/debian|g' /etc/apt/sources.list && \
    sed -i 's|http://security.debian.org/debian-security|http://archive.debian.org/debian-security|g' /etc/apt/sources.list && \
    apt-get update -o Acquire::Check-Valid-Until=false && \
    apt-get install -y --no-install-recommends \
        apt-utils \
        ca-certificates \
        gnupg \
        lsb-release \
        wget \
        git \
        curl \
        python3-pip \
        ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip3 install --no-cache-dir --upgrade pip

# Copy app files
COPY . /app/
WORKDIR /app/

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Start the bot
CMD ["python", "main.py"]
