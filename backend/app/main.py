import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.database.mongodb import connect_to_mongo, close_mongo_connection, db_manager
from app.api import auth, disease, crop, fertilizers, weather, admin, expert

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("agrisaathi")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting AgriSaathi API Service...")
    await connect_to_mongo()
    yield
    # Shutdown
    logger.info("Shutting down AgriSaathi API Service...")
    await close_mongo_connection()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=(
        "AgriSaathi Backend REST API: AI-Powered Agriculture Advisory Platform. "
        "Delivering Plant Disease Detection, Location-Based Crop Recommendation, "
        "Fertilizer Quality & Price Comparison, and Weather Alerts."
    ),
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Open in development for Vite dev server & test environments
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static file serving for uploaded crop leaf images
if not os.path.exists(settings.UPLOAD_DIR):
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=os.path.dirname(settings.UPLOAD_DIR)), name="uploads")

# Include Feature Routers
app.include_router(auth.router, prefix=settings.API_V1_PREFIX)
app.include_router(disease.router, prefix=settings.API_V1_PREFIX)
app.include_router(crop.router, prefix=settings.API_V1_PREFIX)
app.include_router(fertilizers.router, prefix=settings.API_V1_PREFIX)
app.include_router(weather.router, prefix=settings.API_V1_PREFIX)
app.include_router(admin.router, prefix=settings.API_V1_PREFIX)
app.include_router(expert.router, prefix=settings.API_V1_PREFIX)

@app.get("/")
async def root():
    return {
        "app": "AgriSaathi - Our Farmer Friend",
        "milestone": "40% Foundation Complete",
        "documentation": "/docs",
        "health": "/api/health"
    }

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "database": {
            "connected": db_manager.is_connected,
            "engine": "MongoDB Atlas / PyMongo (Motor)"
        },
        "services": {
            "disease_detection_cnn": "Ready (Modular weights interface)",
            "crop_recommendation": "Ready (Environmental & agro-climatic rules active)",
            "fertilizer_comparison": "Active (Standard ranking formula)",
            "weather_alerts": "Active (OpenWeather / Ag-meteorological rule engine)"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=True)

