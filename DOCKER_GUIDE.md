# Docker & Containerization Guide for Epilot Scripts

**Target Audience:** Developer learning containerization  
**Context:** Packaging Epilot Python scripts for consistent deployment  
**Prerequisites:** Basic terminal knowledge

---

## Table of Contents

1. [What is Docker?](#1-what-is-docker)
2. [Why Docker for This Repo?](#2-why-docker-for-this-repo)
3. [Docker Basics](#3-docker-basics)
4. [Dockerizing Python Scripts](#4-dockerizing-python-scripts)
5. [Multi-Stage Builds](#5-multi-stage-builds)
6. [Docker Compose for Local Development](#6-docker-compose-for-local-development)
7. [CI/CD with Docker](#7-cicd-with-docker)
8. [Production Deployment](#8-production-deployment)

---

## 1. What is Docker?

### Mental Model for Developers

**Your current problem:**
```bash
# On your laptop (works fine)
python scripts/workflows/create_tarifabschluss_fulfillment.py
✅ Success!

# On colleague's laptop
python scripts/workflows/create_tarifabschluss_fulfillment.py
❌ ModuleNotFoundError: No module named 'aiohttp'

# On CI server
python scripts/workflows/create_tarifabschluss_fulfillment.py
❌ ImportError: Python 3.8 required, found 3.7
```

**With Docker:**
```bash
# On ANY machine (yours, colleague's, CI, production)
docker run epilot-scripts python scripts/workflows/create_tarifabschluss_fulfillment.py
✅ Success! (always works, everywhere)
```

### Docker vs Virtual Machines

```
┌─────────────────────────────────────────────────────────────┐
│ Your Laptop                                                 │
├─────────────────────────────────────────────────────────────┤
│ Host OS (Ubuntu/macOS/Windows)                              │
├─────────────────────────────────────────────────────────────┤
│ Docker Engine                                               │
├──────────────┬──────────────┬──────────────┬───────────────┤
│ Container 1  │ Container 2  │ Container 3  │ Container 4   │
│ Python 3.11  │ Node.js 20   │ Postgres 15  │ Redis 7       │
│ (20 MB)      │ (50 MB)      │ (100 MB)     │ (10 MB)       │
└──────────────┴──────────────┴──────────────┴───────────────┘

vs

┌─────────────────────────────────────────────────────────────┐
│ Your Laptop                                                 │
├─────────────────────────────────────────────────────────────┤
│ Host OS (Ubuntu/macOS/Windows)                              │
├─────────────────────────────────────────────────────────────┤
│ Hypervisor (VMware/VirtualBox)                              │
├──────────────┬──────────────┬──────────────────────────────┤
│ VM 1         │ VM 2         │ VM 3                          │
│ Ubuntu       │ Ubuntu       │ Ubuntu                        │
│ (2 GB)       │ (2 GB)       │ (2 GB)                        │
│  + Python    │  + Node.js   │  + Postgres                   │
└──────────────┴──────────────┴──────────────────────────────┘
```

**Key difference:**
- **Containers:** Share host OS kernel, lightweight, fast startup
- **VMs:** Each has full OS, heavy, slow startup

---

## 2. Why Docker for This Repo?

### Problems Docker Solves

| Problem | Without Docker | With Docker |
|---------|---------------|-------------|
| **Dependencies** | "Works on my machine" | Works everywhere identically |
| **Python Version** | Must match on all machines | Specified in Dockerfile |
| **Environment Setup** | 15-step README | `docker run` |
| **Isolation** | Global Python packages conflict | Each container isolated |
| **Reproducibility** | Hard to recreate exact environment | Dockerfile = recipe |
| **CI/CD** | Configure runner every time | Pre-built image |
| **Multi-Customer** | One Python env per customer? | One container per customer |

### Real-World Benefits for Epilot Scripts

```bash
# Without Docker: Manual setup
git clone epilot-scripts
cd epilot-scripts
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with credentials
python scripts/workflows/create_tarifabschluss_fulfillment.py

# With Docker: One command
docker run --env-file .env epilot-scripts \
  python scripts/workflows/create_tarifabschluss_fulfillment.py
```

---

## 3. Docker Basics

### Core Concepts

| Term | Analogy | Example |
|------|---------|---------|
| **Image** | Recipe/Template | `epilot-scripts:1.0` |
| **Container** | Running instance of image | Your script executing |
| **Dockerfile** | Recipe instructions | `FROM python:3.11...` |
| **Registry** | App store for images | Docker Hub, GitHub Container Registry |
| **Volume** | Shared folder | Mount local `data/` into container |
| **Network** | Communication channel | Connect Python app to Postgres |

### Essential Commands

```bash
# Build an image
docker build -t epilot-scripts:1.0 .

# Run a container
docker run epilot-scripts:1.0

# List running containers
docker ps

# List all containers (including stopped)
docker ps -a

# Stop a container
docker stop <container-id>

# Remove a container
docker rm <container-id>

# List images
docker images

# Remove an image
docker rmi epilot-scripts:1.0

# View logs
docker logs <container-id>

# Execute command in running container
docker exec -it <container-id> bash

# Clean up everything
docker system prune -a
```

---

## 4. Dockerizing Python Scripts

### Simple Dockerfile

```dockerfile
# Dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first (Docker layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Default command
CMD ["python", "scripts/utilities/show_help.py"]
```

### Build and Run

```bash
# Build image
docker build -t epilot-scripts:latest .

# Run with environment variables
docker run \
  -e EPILOT_TOKEN="Bearer xyz..." \
  -e EPILOT_ORG_ID="20000382" \
  epilot-scripts:latest \
  python scripts/workflows/create_tarifabschluss_fulfillment.py

# Run with .env file
docker run --env-file .env epilot-scripts:latest \
  python scripts/entities/list_entities.py
```

### Better Dockerfile (Optimized)

```dockerfile
# Dockerfile
FROM python:3.11-slim AS base

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY lib/ ./lib/
COPY scripts/ ./scripts/
COPY config/ ./config/

# Create non-root user for security
RUN useradd -m -u 1000 epilot && chown -R epilot:epilot /app
USER epilot

# Set Python environment
ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Entry point for easy script execution
ENTRYPOINT ["python"]
CMD ["scripts/utilities/show_help.py"]
```

### Usage Examples

```bash
# Build
docker build -t epilot-scripts:1.0 .

# List entities
docker run --env-file .env epilot-scripts:1.0 \
  scripts/entities/list_entities.py

# Create workflow
docker run --env-file .env epilot-scripts:1.0 \
  scripts/workflows/create_tarifabschluss_fulfillment.py

# Interactive Python shell
docker run -it --env-file .env epilot-scripts:1.0

# Run specific script
docker run --env-file .env epilot-scripts:1.0 \
  scripts/demo/erstelle_demo_kontakte.py
```

---

## 5. Multi-Stage Builds

### Why Multi-Stage?

**Problem:** Development needs are different from production needs

```dockerfile
# Multi-stage Dockerfile
# Stage 1: Development environment
FROM python:3.11 AS development

WORKDIR /app

# Install dev dependencies (testing, linting, etc.)
COPY requirements.txt requirements-dev.txt ./
RUN pip install -r requirements.txt -r requirements-dev.txt

COPY . .

# Run tests
RUN pytest tests/ --cov=lib

# Stage 2: Production environment (smaller, no dev tools)
FROM python:3.11-slim AS production

WORKDIR /app

# Only install production dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy only necessary files
COPY lib/ ./lib/
COPY scripts/ ./scripts/
COPY config/ ./config/

# Security: non-root user
RUN useradd -m epilot && chown -R epilot:epilot /app
USER epilot

ENV PYTHONUNBUFFERED=1 PYTHONPATH=/app

ENTRYPOINT ["python"]
CMD ["scripts/utilities/show_help.py"]
```

### Build Specific Stage

```bash
# Build development image (includes tests, linting)
docker build --target development -t epilot-scripts:dev .

# Build production image (smaller, optimized)
docker build --target production -t epilot-scripts:prod .

# Compare sizes
docker images epilot-scripts
# epilot-scripts:dev   1.2 GB
# epilot-scripts:prod  200 MB  ← Much smaller!
```

---

## 6. Docker Compose for Local Development

### What is Docker Compose?

**Docker:** Run one container  
**Docker Compose:** Run multiple containers together (application + database + cache)

### docker-compose.yml for Epilot Scripts

```yaml
# docker-compose.yml
version: '3.8'

services:
  # Main application
  epilot-scripts:
    build:
      context: .
      dockerfile: Dockerfile
      target: development
    volumes:
      # Mount source code for live editing
      - ./lib:/app/lib
      - ./scripts:/app/scripts
      - ./data:/app/data
      # Persist Python cache
      - python-cache:/home/epilot/.cache
    environment:
      - EPILOT_TOKEN=${EPILOT_TOKEN}
      - EPILOT_ORG_ID=${EPILOT_ORG_ID}
    env_file:
      - .env
    command: tail -f /dev/null  # Keep container running
    
  # PostgreSQL for local testing (if needed)
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: epilot_test
      POSTGRES_USER: epilot
      POSTGRES_PASSWORD: secret
    ports:
      - "5432:5432"
    volumes:
      - postgres-data:/var/lib/postgresql/data
  
  # Redis for caching (if needed)
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  python-cache:
  postgres-data:
```

### Using Docker Compose

```bash
# Start all services
docker compose up -d

# View logs
docker compose logs -f

# Execute script in running container
docker compose exec epilot-scripts \
  python scripts/entities/list_entities.py

# Interactive shell
docker compose exec epilot-scripts bash

# Stop all services
docker compose down

# Stop and remove volumes (clean slate)
docker compose down -v
```

### Development Workflow

```bash
# 1. Start development environment
docker compose up -d

# 2. Edit code in your IDE (changes reflected immediately via volume mount)
vim scripts/workflows/create_tarifabschluss_fulfillment.py

# 3. Run script
docker compose exec epilot-scripts \
  python scripts/workflows/create_tarifabschluss_fulfillment.py

# 4. Run tests
docker compose exec epilot-scripts pytest tests/

# 5. Check linting
docker compose exec epilot-scripts flake8 lib/ scripts/

# 6. Stop when done
docker compose down
```

---

## 7. CI/CD with Docker

### GitHub Actions with Docker

```yaml
# .github/workflows/docker-ci.yml
name: Docker CI/CD

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  build-and-test:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v3
    
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v2
    
    - name: Build development image
      uses: docker/build-push-action@v4
      with:
        context: .
        target: development
        push: false
        tags: epilot-scripts:test
        cache-from: type=gha
        cache-to: type=gha,mode=max
    
    - name: Run tests in container
      run: |
        docker run --rm epilot-scripts:test pytest tests/
    
    - name: Run linting in container
      run: |
        docker run --rm epilot-scripts:test flake8 lib/ scripts/
  
  build-and-push:
    needs: build-and-test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    permissions:
      contents: read
      packages: write
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v3
    
    - name: Log in to Container Registry
      uses: docker/login-action@v2
      with:
        registry: ${{ env.REGISTRY }}
        username: ${{ github.actor }}
        password: ${{ secrets.GITHUB_TOKEN }}
    
    - name: Extract metadata
      id: meta
      uses: docker/metadata-action@v4
      with:
        images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
        tags: |
          type=ref,event=branch
          type=ref,event=pr
          type=semver,pattern={{version}}
          type=sha,prefix={{branch}}-
    
    - name: Build and push production image
      uses: docker/build-push-action@v4
      with:
        context: .
        target: production
        push: true
        tags: ${{ steps.meta.outputs.tags }}
        labels: ${{ steps.meta.outputs.labels }}
        cache-from: type=gha
        cache-to: type=gha,mode=max
```

### Using Published Image

```bash
# Pull from GitHub Container Registry
docker pull ghcr.io/timoelony/epilot-scripts:main

# Run
docker run --env-file .env \
  ghcr.io/timoelony/epilot-scripts:main \
  scripts/workflows/create_tarifabschluss_fulfillment.py
```

---

## 8. Production Deployment

### Running on AWS ECS (Elastic Container Service)

```bash
# 1. Build and push to registry
docker build -t epilot-scripts:prod --target production .
docker tag epilot-scripts:prod 123456789.dkr.ecr.eu-central-1.amazonaws.com/epilot-scripts:latest
docker push 123456789.dkr.ecr.eu-central-1.amazonaws.com/epilot-scripts:latest

# 2. Create ECS task definition
# task-definition.json (simplified)
{
  "family": "epilot-scripts",
  "containerDefinitions": [
    {
      "name": "epilot-scripts",
      "image": "123456789.dkr.ecr.eu-central-1.amazonaws.com/epilot-scripts:latest",
      "environment": [
        {"name": "EPILOT_ORG_ID", "value": "20000382"}
      ],
      "secrets": [
        {
          "name": "EPILOT_TOKEN",
          "valueFrom": "arn:aws:secretsmanager:eu-central-1:123456789:secret:epilot-token"
        }
      ]
    }
  ]
}

# 3. Run task
aws ecs run-task \
  --cluster epilot-cluster \
  --task-definition epilot-scripts \
  --launch-type FARGATE
```

### Running as Scheduled Job (Cron)

```bash
# AWS EventBridge rule to run daily at 2 AM
aws events put-rule \
  --name epilot-daily-sync \
  --schedule-expression "cron(0 2 * * ? *)"

# Target: ECS task
aws events put-targets \
  --rule epilot-daily-sync \
  --targets '{
    "Id": "1",
    "Arn": "arn:aws:ecs:eu-central-1:123456789:cluster/epilot-cluster",
    "RoleArn": "arn:aws:iam::123456789:role/ecsEventsRole",
    "EcsParameters": {
      "TaskDefinitionArn": "arn:aws:ecs:eu-central-1:123456789:task-definition/epilot-scripts",
      "LaunchType": "FARGATE"
    }
  }'
```

### Docker Security Best Practices

```dockerfile
# 1. Use specific version tags (not 'latest')
FROM python:3.11.6-slim

# 2. Run as non-root user
RUN useradd -m -u 1000 epilot
USER epilot

# 3. Don't include secrets in image
# Use environment variables or secrets manager

# 4. Minimize attack surface
RUN apt-get update && apt-get install -y \
    --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

# 5. Use .dockerignore
# .dockerignore
.env
.git
__pycache__
*.pyc
.pytest_cache
.venv
env/
```

---

## 9. Practical Exercises

### Exercise 1: Build Your First Docker Image

1. Create simple Dockerfile
2. Build image
3. Run container
4. Execute script inside

**Time:** 30 minutes  
**Difficulty:** ⭐

### Exercise 2: Multi-Stage Build

1. Create Dockerfile with dev and prod stages
2. Build both
3. Compare sizes
4. Run tests in dev image

**Time:** 45 minutes  
**Difficulty:** ⭐⭐

### Exercise 3: Docker Compose Setup

1. Create docker-compose.yml
2. Add services (app, postgres, redis)
3. Start all services
4. Run scripts in container

**Time:** 1 hour  
**Difficulty:** ⭐⭐

### Exercise 4: CI/CD Pipeline

1. Create GitHub Actions workflow with Docker
2. Build image on push
3. Run tests in container
4. Push to registry on main branch

**Time:** 2 hours  
**Difficulty:** ⭐⭐⭐

---

## 10. Cheat Sheet

```bash
# Build
docker build -t epilot-scripts:latest .

# Run interactively
docker run -it --env-file .env epilot-scripts:latest bash

# Run script
docker run --env-file .env epilot-scripts:latest \
  python scripts/entities/list_entities.py

# View logs
docker logs <container-id>

# Clean up
docker system prune -a -f

# Docker Compose
docker compose up -d        # Start
docker compose down         # Stop
docker compose logs -f      # View logs
docker compose exec app bash # Shell into container
```

---

## Summary

**Why Docker for Epilot Scripts:**
- ✅ Consistent environment everywhere
- ✅ Easy onboarding (no setup steps)
- ✅ Isolated dependencies
- ✅ Ready for production deployment
- ✅ CI/CD integration

**When to Use:**
- ✅ Production deployments
- ✅ CI/CD pipelines
- ✅ Team collaboration
- ✅ Multi-customer isolation

**When NOT to Use:**
- ❌ Quick local testing (just use venv)
- ❌ Learning Python (adds complexity)

**Next Steps:**
1. Dockerize this repo (Exercise 1-2)
2. Set up Docker Compose (Exercise 3)
3. Add to CI/CD (Exercise 4)
4. Learn Kubernetes if scaling >10 customers

You now understand containerization! Docker makes your Python scripts portable and production-ready. 🐳