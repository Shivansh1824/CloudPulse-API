import io
import yaml
from PIL import Image
import requests
from typing import Dict, Any

def parse_cluster_config(raw_yaml: str) -> Dict[str, Any]:
    """
    Parses incoming YAML configuration for microservice cluster nodes.
    Calls PyYAML unsafe loader (vulnerable in PyYAML 5.4.1).
    """
    try:
        # Intentionally demonstrates reachable call to yaml.load
        parsed_data = yaml.load(raw_yaml, Loader=yaml.Loader)
        return parsed_data if isinstance(parsed_data, dict) else {"status": "ok", "raw": str(parsed_data)}
    except Exception as e:
        return {"error": f"Failed to parse config: {str(e)}"}

def process_media_thumbnail(image_bytes: bytes, width: int = 128, height: int = 128) -> Dict[str, Any]:
    """
    Processes and resizes avatar media images for user profiles.
    Calls Pillow (vulnerable in Pillow 9.5.0).
    """
    try:
        img_buffer = io.BytesIO(image_bytes)
        with Image.open(img_buffer) as img:
            resized_img = img.resize((width, height))
            format_name = img.format or "PNG"
            return {
                "format": format_name,
                "dimensions": f"{resized_img.width}x{resized_img.height}",
                "status": "processed"
            }
    except Exception as e:
        return {"error": f"Image processing failed: {str(e)}"}

def forward_webhook_notification(target_url: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Forwards event telemetry to external monitoring webhooks.
    Calls requests (vulnerable in requests 2.28.1).
    """
    try:
        headers = {"User-Agent": "CloudPulse-Forwarder/1.0", "Content-Type": "application/json"}
        response = requests.post(target_url, json=payload, headers=headers, timeout=5)
        return {
            "status_code": response.status_code,
            "forwarded": response.status_code < 400
        }
    except Exception as e:
        return {"error": f"Webhook delivery failed: {str(e)}"}
