"""
Main FastAPI application for AutoSwas Process Management System.
Configures the FastAPI app, includes routers, and handles CORS.

Author: Cline
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import sys
from datetime import datetime
from pathlib import Path

# Add parent directory to Python path for imports
sys.path.append(str(Path(__file__).parent.parent))

from app.models.database import engine, Base
from app.routers import process

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AutoSwas Process Management API",
    description="API for managing business processes and their automation status",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(process.router)


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Handle all unhandled exceptions."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error occurred. Please try again later."},
    )


@app.get("/")
async def root():
    """Root endpoint for API health check."""
    return {
        "status": "healthy",
        "message": "AutoSwas Process Management API is running",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    try:
        # Add any additional health checks here (e.g., database connection)
        return {
            "status": "healthy",
            "version": "1.0.0",
            "timestamp": datetime.now().isoformat(),
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail="Service unavailable")


if __name__ == "__main__":
    import uvicorn

    logger.info("Starting AutoSwas API server")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, log_level="info")
