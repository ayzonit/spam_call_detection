import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from App.api import routes_auth, routes_alert
from App.core.logger import logger
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(
    title="🎤 Voice Authentication API",
    description="Authenticate users by voice and detect spoofed or recorded attempts.",
    version="1.0.0"
)

# CORS configuration
ALLOWED_ORIGINS = [
    "http://localhost:3000",  # React dev server
    "http://localhost:5173",  # Vite dev server
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(routes_auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(routes_alert.router, prefix="/api", tags=["Alerts"])

# Frontend build directory
FRONTEND_BUILD_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend", "dist")

@app.on_event("startup")
async def startup_event():
    logger.info("Voice Authentication API started successfully!")
    os.makedirs("models/embeddings", exist_ok=True)
    os.makedirs("audio_samples", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    
    # Check if frontend build exists
    if os.path.exists(FRONTEND_BUILD_DIR):
        logger.info(f"Frontend build found at: {FRONTEND_BUILD_DIR}")
        app.mount("/static", StaticFiles(directory=os.path.join(FRONTEND_BUILD_DIR, "assets")), name="static")
    else:
        logger.warning(f"Frontend build not found at: {FRONTEND_BUILD_DIR}")
        logger.info("Run 'npm run build' in the frontend directory to enable single-page serving")

@app.get("/test-frontend")
def test_frontend():
    """Test endpoint to verify frontend serving works"""
    if os.path.exists(FRONTEND_BUILD_DIR):
        index_file = os.path.join(FRONTEND_BUILD_DIR, "index.html")
        if os.path.exists(index_file):
            return FileResponse(index_file)
    return {"error": "Frontend not found"}

@app.get("/")
def root():
    # Always serve the React app if it exists
    if os.path.exists(FRONTEND_BUILD_DIR):
        index_file = os.path.join(FRONTEND_BUILD_DIR, "index.html")
        if os.path.exists(index_file):
            return FileResponse(index_file)
    
    # Otherwise, return API info
    return {
        "status": "Voice Authentication API is running 🚀",
        "endpoints": {
            "enroll": "/api/auth/enroll",
            "verify": "/api/auth/verify",
            "health": "/api/health",
            "docs": "/docs",
            "test_frontend": "/test-frontend"
        },
        "note": "Frontend not built. Run 'npm run build' in frontend directory to enable single-page serving."
    }

# Catch-all route for React Router (SPA) - must be last
@app.get("/{full_path:path}")
def serve_frontend(full_path: str):
    # Don't interfere with API routes
    if full_path.startswith("api/") or full_path.startswith("docs") or full_path.startswith("openapi.json") or full_path.startswith("static/") or full_path == "test-frontend":
        return {"error": "Not found"}
    
    # Serve React app for all other routes
    if os.path.exists(FRONTEND_BUILD_DIR):
        index_file = os.path.join(FRONTEND_BUILD_DIR, "index.html")
        if os.path.exists(index_file):
            return FileResponse(index_file)
    
    return {"error": "Frontend not available. Build the frontend first."}

''''@app.post("/train")
def train_models():
    try:
        from App.training.train import train_spoof_model, train_speaker_model
        logger.info("Starting model training...")
        train_spoof_model()
        train_speaker_model()
        return {"message": "Model training completed successfully!"}
    except Exception as e:
        logger.error(f"Training failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))'''