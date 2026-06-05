# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

import google.auth
from fastapi import FastAPI
from google.adk.cli.fast_api import get_fast_api_app
from google.cloud import logging as google_cloud_logging

from app.app_utils.telemetry import setup_telemetry
from app.app_utils.typing import Feedback

setup_telemetry()
_, project_id = google.auth.default()
logging_client = google_cloud_logging.Client()
logger = logging_client.logger(__name__)
allow_origins = (
    os.getenv("ALLOW_ORIGINS", "").split(",") if os.getenv("ALLOW_ORIGINS") else None
)

# Artifact bucket for ADK (created by Terraform, passed via env var)
logs_bucket_name = os.environ.get("LOGS_BUCKET_NAME")

# app/fast_api_app.py lives at insightflow-ai/app/fast_api_app.py
# dirname once -> insightflow-ai/app
# dirname twice -> insightflow-ai  (where charts are saved)
AGENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# In-memory session configuration - no persistent storage
session_service_uri = None

artifact_service_uri = f"gs://{logs_bucket_name}" if logs_bucket_name else None

app: FastAPI = get_fast_api_app(
    agents_dir=AGENT_DIR,
    web=True,
    artifact_service_uri=artifact_service_uri,
    allow_origins=allow_origins,
    session_service_uri=session_service_uri,
    otel_to_cloud=True,
)
app.title = "platform-engineering-agent"
app.description = "API for interacting with the Agent platform-engineering-agent"


@app.post("/feedback")
def collect_feedback(feedback: Feedback) -> dict[str, str]:
    """Collect and log feedback.

    Args:
        feedback: The feedback data to log

    Returns:
        Success message
    """
    logger.log_struct(feedback.model_dump(), severity="INFO")
    return {"status": "success"}


import logging as _logging
from fastapi.responses import FileResponse
from fastapi import HTTPException

_chart_logger = _logging.getLogger("chart_server")

# NOTE: We intentionally serve charts at /charts/ (not /dev-ui/) because
# /dev-ui/ is a Starlette Mount that intercepts ALL sub-paths before FastAPI
# routing, making custom routes under that prefix unreachable.
@app.get("/charts/{filename:path}")
def get_chart_image(filename: str):
    # Strip .png suffix if already present, then re-add it
    base = filename.removesuffix(".png")
    file_name = f"{base}.png"
    # Charts are saved relative to the insightflow-ai directory (AGENT_DIR)
    file_path = os.path.join(AGENT_DIR, file_name)
    _chart_logger.info("Chart request: %s -> %s (exists=%s)", filename, file_path, os.path.exists(file_path))
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="image/png")
    raise HTTPException(status_code=404, detail=f"Chart not found at: {file_path}")


# Main execution
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
