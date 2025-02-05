# app/main.py

import logging
from fastapi import FastAPI

from app.core.config import Settings
from app.core.logging_config import setup_logging
from app.router import health
from app.router import deep_researcher
from app.router import feedback_routes
from app.router import indexer
# Instantiate our Pydantic Settings (reads from environment)
settings = Settings()

def create_app() -> FastAPI:
    # Basic logging configuration
    setup_logging()
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
    app.include_router(indexer.router, prefix="/api", tags=["indexer"])
    return app

app = create_app()
