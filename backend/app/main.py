"""FastAPI application entry point for OpsPilot."""

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="OpsPilot API", version="0.1.0")


class HealthLiveResponse(BaseModel):
    """Schema for API liveness probe response."""

    status: str = Field(default="ok", description="Process health status")
    service: str = Field(default="opspilot-backend", description="Service identifier")
    version: str = Field(default="0.1.0", description="API version")


@app.get(
    "/health",
    tags=["health"],
    response_model=HealthLiveResponse,
    summary="Basic Health Check",
)
@app.get(
    "/health/live",
    tags=["health"],
    response_model=HealthLiveResponse,
    summary="Liveness Probe",
)
async def health_live() -> HealthLiveResponse:
    """Report that the API process is running and responsive."""
    return HealthLiveResponse(
        status="ok",
        service="opspilot-backend",
        version=app.version,
    )
