from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import logging
from datetime import datetime
import traceback
import json

logger = logging.getLogger(__name__)

def _make_serializable(obj):
    """Convert non-serializable objects to strings"""
    if isinstance(obj, (str, int, float, bool, type(None))):
        return obj
    elif isinstance(obj, (list, tuple)):
        return [_make_serializable(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: _make_serializable(value) for key, value in obj.items()}
    else:
        # Convert non-serializable objects to string
        return str(obj)

async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions"""
    logger.error(f"HTTP {exc.status_code} error: {exc.detail}")
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "HTTP Exception",
            "detail": str(exc.detail),
            "timestamp": datetime.now().isoformat(),
            "path": str(request.url)
        }
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors with proper serialization"""
    logger.error(f"Validation error: {exc.errors()}")
    
    # Make error details JSON serializable
    error_details = _make_serializable(exc.errors())
    
    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation Error",
            "detail": error_details,
            "message": "Request validation failed",
            "timestamp": datetime.now().isoformat(),
            "path": str(request.url)
        }
    )

async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions"""
    logger.error(f"Unexpected error: {str(exc)}")
    logger.error(f"Traceback: {traceback.format_exc()}")
    
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "detail": "An unexpected error occurred",
            "timestamp": datetime.now().isoformat(),
            "path": str(request.url)
        }
    )

class APIException(Exception):
    """Custom API exception"""
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

async def api_exception_handler(request: Request, exc: APIException):
    """Handle custom API exceptions"""
    logger.error(f"API Exception: {exc.message}")
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "API Exception",
            "detail": exc.message,
            "timestamp": datetime.now().isoformat(),
            "path": str(request.url)
        }
    )