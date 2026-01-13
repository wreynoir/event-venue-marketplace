"""
Event Venue Marketplace - FastAPI Backend
Main application entry point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api import auth, venues, briefs, matching

app = FastAPI(
    title="Event Venue Marketplace API",
    description="Two-sided marketplace connecting event hosts with NYC venues",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# CORS configuration for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api")
app.include_router(venues.router, prefix="/api")
app.include_router(briefs.router, prefix="/api")
app.include_router(matching.router, prefix="/api")


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Event Venue Marketplace API",
        "version": "1.0.0"
    }


@app.get("/api/health")
async def health_check():
    """Detailed health check endpoint"""
    return {
        "status": "healthy",
        "database": "not configured",  # Will update when DB is connected
        "services": {
            "stripe": "mocked",
            "anthropic": "configured",
            "email": "mocked",
            "sms": "mocked"
        }
    }
