# Use Python 3.11 as base
FROM python:3.11-slim

# Prevent Python from writing .pyc files and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies, Node.js (for gemini-cli), and Playwright requirements
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y \
    nodejs \
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libpango-1.0-0 \
    libcairo2 \
    libasound2 \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Gemini CLI globally via npm
RUN npm install -g @google/gemini-cli

# Install Playwright browsers for the autonomous agents
RUN playwright install chromium
RUN playwright install-deps chromium

# Copy project files
COPY . .

# Expose ports (8000 for API, 8501 for Streamlit)
EXPOSE 8000
EXPOSE 8501

# Default command to run the API server (can be overridden in docker-compose)
CMD ["python", "api_server.py"]
