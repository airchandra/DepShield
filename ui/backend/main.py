"""FastAPI application for DepShield dashboard."""

import logging
import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from ui.backend.routes import logs, matrix, reports, runs, vulns

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    """Create and configure FastAPI application.

    Returns:
        Configured FastAPI app
    """
    app = FastAPI(
        title="DepShield Dashboard",
        description="Web dashboard for vulnerability remediation pipeline",
        version="0.1.0",
    )

    # CORS middleware - restrict origins in production
    allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:5173").split(",")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE"],
        allow_headers=["*"],
    )

    # Include routes
    app.include_router(runs.router)
    app.include_router(logs.router)
    app.include_router(vulns.router)
    app.include_router(matrix.router)
    app.include_router(reports.router)

    # Health check endpoint
    @app.get("/api/health")
    async def health():
        """Health check endpoint."""
        return {"status": "ok"}

    # Serve frontend static files if they exist
    frontend_dist = Path(__file__).parent.parent / "frontend" / "dist"
    if frontend_dist.exists():
        app.mount("/", StaticFiles(directory=frontend_dist, html=True), name="frontend")

    logger.info("FastAPI app created")
    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
