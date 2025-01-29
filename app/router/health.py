# app/routers/health.py

from fastapi import APIRouter
import logging

# Create a separate logger for this module
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/health", tags=["health"])
def health_check():
    """
    Health check endpoint to verify that the service is up.
    """
    logger.info("Health check endpoint called")
    return {"status": "ok"}