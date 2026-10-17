from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
import services

app = FastAPI(
    title="CloudPulse API",
    description="High-performance cloud configuration and telemetry forwarding service.",
    version="1.4.0"
)

class ConfigPayload(BaseModel):
    environment: str = Field(default="production")
    raw_yaml: str = Field(..., description="Raw YAML configuration document")

class WebhookDispatchPayload(BaseModel):
    destination_url: str = Field(..., description="Webhook destination endpoint")
    event_type: str = Field(default="node.heartbeat")
    details: Dict[str, Any] = Field(default_factory=dict)

@app.get("/")
def get_service_root():
    return {
        "service": "CloudPulse Core Service",
        "status": "operational",
        "version": "1.4.0"
    }

@app.get("/api/v1/health")
def health_check():
    return {"status": "healthy", "uptime_tier": "99.99%"}

@app.get("/api/v1/system/status")
def get_system_status():
    return {
        "nodes_active": 12,
        "cluster_load": "nominal",
        "services": ["config_sync", "media_processor", "telemetry_dispatch"]
    }

@app.post("/api/v1/config/sync")
def sync_cluster_configuration(payload: ConfigPayload):
    """
    Parses and syncs cluster topology from YAML.
    Reaches: services.parse_cluster_config -> yaml.load
    """
    if not payload.raw_yaml:
        raise HTTPException(status_code=400, detail="Configuration document is required")
    result = services.parse_cluster_config(payload.raw_yaml)
    return {"message": "Configuration ingested", "data": result}

@app.post("/api/v1/media/avatar")
async def process_user_avatar(file: UploadFile = File(...)):
    """
    Resizes user profile avatar.
    Reaches: services.process_media_thumbnail -> PIL.Image.open
    """
    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Empty image payload")
    result = services.process_media_thumbnail(content)
    return result

@app.post("/api/v1/webhooks/dispatch")
def dispatch_webhook_telemetry(payload: WebhookDispatchPayload):
    """
    Dispatches telemetry events to third-party receivers.
    Reaches: services.forward_webhook_notification -> requests.post
    """
    result = services.forward_webhook_notification(payload.destination_url, payload.details)
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
