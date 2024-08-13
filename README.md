# Biological Test Management Services

## Overview

This application is designed to record and consult biological test results for patients. It consists of two main services:

1. **Laboratory Service**: Allows laboratories to record biological test results.
2. **Patient Service**: Enables patients to consult their biological test results and view their evolution over time.

## Stack

- Backend: Python, FastAPI, SQLite, Redis
- Infrastructure: Docker, Docker Compose

## Run Services locally

```bash
python3.11 -m venv venv
source venv/bin/activate

pip install -r src/laboratory_service/requirements.txt
export PYTHONPATH="${PYTHONPATH}:src/laboratory_service"
uvicorn src.laboratory_service.main:app --host 0.0.0.0 --port 8001 --reload

pip install -r src/patient_service/requirements.txt
export PYTHONPATH="${PYTHONPATH}:src/patient_service"
uvicorn src.patient_service.main:app --host 0.0.0.0 --port 8002 --reload
```

### Using docker

```bash
export HOST_IP=$(hostname -I | awk '{print $1}')
docker run -d --name redis -p 6377:6379 redis

docker build -t laboratory_service:latest src/laboratory_service
docker run -p 8001:8001 --name laboratory_service -e REDIS_HOST=$HOST_IP -v $(pwd)/src/laboratory_service/bio_lab.db:/app/bio_lab.db laboratory_service:latest

docker build -t patient_service:latest src/patient_service
docker run -p 8002:8002 --name patient_service -e REDIS_HOST=$HOST_IP -v $(pwd)/src/patient_service/bio.db:/app/bio.db patient_service:latest
```

### Using docker-compose

```bash
cd infrastructure
docker compose up --build
```

### Demo

- laboratory_service: <http://0.0.0.0:8001/docs>
- patient_service: <http://0.0.0.0:8002/docs>
