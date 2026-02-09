"""InsertedLogo FastAPI Application"""

from fastapi import FastAPI
from app.routes.overlay import router as overlay_router


def create_app() -> FastAPI:
    """Create and configure FastAPI application"""
    app = FastAPI(
        title="InsertedLogo API",
        description="API for overlaying logos on images",
        version="1.0.0"
    )
    
    # Include routers
    app.include_router(overlay_router, tags=["overlay"])
    
    return app
