"""FastAPI application entry point for OpsPilot."""

from fastapi import FastAPI

app = FastAPI(title="OpsPilot API", version="0.1.0")


@app.get("/health/live", tags=["health"])
async def health_live() -> dict[str, str]:
    """Report that the API process is running."""
    return {"status": "ok"}
