# app/core/exception_handlers.py
import logging
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)

async def global_exception_handler(request: Request, exc: Exception):
    # Log the exception with full stack trace
    logger.exception("Unhandled error occurred: %s", exc)
    # Return a generic error message. You can customize this response.
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error. Please try again later."},
    )