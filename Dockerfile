# Stage 1: Base image for dependency installation
FROM python:3.10-slim AS base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Install Node.js for JavaScript dependencies
FROM node:18-slim AS node_modules

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package.json package-lock.json ./

# Install JavaScript dependencies
RUN npm install --production

# Stage 3: Run tests
FROM base AS test

# Copy application code and dependencies
COPY . .
COPY --from=node_modules /app/node_modules ./node_modules

# Run Python and JavaScript tests
RUN pytest --disable-warnings
RUN npm test

# Stage 4: Production build
FROM python:3.10-slim AS production

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy Python dependencies
COPY --from=base /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=base /usr/local/bin /usr/local/bin

# Copy Node.js dependencies
COPY --from=node_modules /app/node_modules ./node_modules

# Copy application code
COPY . .

# Expose the application port
EXPOSE 8000

# Set the entrypoint
CMD ["python", "app.py"]