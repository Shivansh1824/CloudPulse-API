# CloudPulse API

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-009688.svg)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)

CloudPulse is a high-throughput microservice backend engineered for distributed cloud infrastructure management. It exposes endpoints for:
- Synchronizing YAML cluster configurations across regions
- Processing user avatar and document media previews
- Dispatching asynchronous telemetry webhooks to external monitoring services

## Architecture & Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | Root service health & telemetry status |
| `GET` | `/api/v1/health` | Automated uptime heartbeat probe |
| `GET` | `/api/v1/system/status` | Active cluster nodes and system load |
| `POST` | `/api/v1/config/sync` | Parses and validates cluster topology YAML |
| `POST` | `/api/v1/media/avatar` | Resizes and encodes profile media assets |
| `POST` | `/api/v1/webhooks/dispatch` | Dispatches outbound telemetry webhooks |

## Quick Start

```bash
# Clone the repository
git clone https://github.com/Shivansh1824/CloudPulse-API.git
cd CloudPulse-API

# Install dependencies
pip install -r requirements.txt

# Start the application server
uvicorn main:app --host 0.0.0.0 --port 8080 --reload
```
