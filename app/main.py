# app/main.py

import logging
from fastapi import FastAPI

from app.core.config import Settings
from app.router import health
from app.router import deep_researcher
from app.router import feedback_routes

# Instantiate our Pydantic Settings (reads from environment)
settings = Settings()

def create_app() -> FastAPI:
    # Basic logging configuration
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )
    logger = logging.getLogger(__name__)
    logger.info(f"Starting app in '{settings.ENV_NAME}' environment")

    # Initialize FastAPI
    app = FastAPI(
        title=settings.API_TITLE,
        version=settings.API_VERSION
    )

    # Include routers
    app.include_router(health.router, prefix="/api")
    app.include_router(deep_researcher.router, prefix="/api", tags=["deep-research"])
    app.include_router(feedback_routes.router, prefix="/api", tags=["feedback"])
    return app

app = create_app()
