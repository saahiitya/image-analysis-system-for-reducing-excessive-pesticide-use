"""
Main FastAPI application for CropGuard AI Platform
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from pathlib import Path

from .config import (
    APP_TITLE, APP_VERSION, APP_DESCRIPTION,
    SERVER_HOST, SERVER_PORT, DEBUG_MODE,
    CORS_ORIGINS, MAX_REQUEST_SIZE
)
from .api.routes import router

# Create FastAPI application
app = FastAPI(
    title=APP_TITLE,
    version=APP_VERSION,
    description=APP_DESCRIPTION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api/v1", tags=["CropGuard AI"])

# Mount static files
static_path = Path(__file__).parent.parent / "frontend" / "static"
if static_path.exists():
    app.mount("/static", StaticFiles(directory=str(static_path)), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the main HTML page"""
    html_path = Path(__file__).parent.parent / "frontend" / "index.html"
    
    if html_path.exists():
        return FileResponse(html_path)
    else:
        # Fallback HTML if file doesn't exist
        return HTMLResponse(content="""
        <!DOCTYPE html>
        <html>
        <head>
            <title>CropGuard AI</title>
        </head>
        <body>
            <h1>🌱 CropGuard AI Platform</h1>
            <p>Welcome to the AI-powered precision pesticide management platform!</p>
            <p>Please ensure the frontend files are properly placed in the frontend directory.</p>
            <p><a href="/docs">View API Documentation</a></p>
        </body>
        </html>
        """)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "CropGuard AI",
        "version": APP_VERSION
    }

# Legacy routes for backward compatibility
@app.post("/analyze-crop")
async def analyze_crop_legacy(*args, **kwargs):
    """Legacy route - redirects to new API"""
    from .api.routes import analyze_crop
    return await analyze_crop(*args, **kwargs)

@app.get("/weather")
async def get_weather_legacy():
    """Legacy route - redirects to new API"""
    from .api.routes import get_weather
    return await get_weather()

@app.get("/scan-history")
async def get_scan_history_legacy():
    """Legacy route - redirects to new API"""
    from .api.routes import get_scan_history
    return await get_scan_history()

if __name__ == "__main__":
    uvicorn.run(
        "backend.main:app",
        host=SERVER_HOST,
        port=SERVER_PORT,
        reload=DEBUG_MODE,
        access_log=True
    )