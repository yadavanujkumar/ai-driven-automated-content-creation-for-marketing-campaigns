from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from routes.content import content_router
from middleware.rate_limiter import rate_limit_middleware
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AI-Driven Automated Content Creation",
    description="An API for generating AI-driven marketing content with advanced analytics.",
    version="2.0.0",
)

# Add rate limiting middleware
app.middleware("http")(rate_limit_middleware)

# CORS middleware configuration
origins = [
    "http://localhost",
    "http://localhost:3000",
    "https://your-production-domain.com",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"HTTP Exception: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled Exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"message": "An unexpected error occurred. Please try again later."},
    )

# Health check route
@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint to verify the service is running with system status.
    """
    logger.info("Health check endpoint accessed.")
    return {
        "status": "healthy",
        "version": "2.0.0",
        "features": {
            "content_generation": "enabled",
            "sentiment_analysis": "enabled",
            "seo_analytics": "enabled",
            "rate_limiting": "enabled",
            "campaign_management": "enabled"
        }
    }

# Include routers
app.include_router(content_router, prefix="/api/v1/content", tags=["Content"])

# Application startup event
@app.on_event("startup")
async def startup_event():
    logger.info("Application startup: Initializing resources.")

# Application shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Application shutdown: Cleaning up resources.")

# Main entry point
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)