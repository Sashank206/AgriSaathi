import os
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "AgriSaathi - Our Farmer Friend"
    VERSION: str = "1.0.0-alpha (40% Milestone)"
    API_V1_PREFIX: str = "/api"
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    ENVIRONMENT: str = "development"
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000"
    
    # Auth
    SECRET_KEY: str = "agrisaathi-dev-super-secure-key-change-in-production-2025"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    
    # Database
    MONGODB_URI: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "agrisaathi_db"
    
    # External APIs
    OPENWEATHER_API_KEY: str = ""
    
    # ML paths
    DISEASE_MODEL_PATH: str = "ml/saved_models/full_plant_disease_model.keras"
    CLASS_MAPPING_PATH: str = "ml/disease_detection/class_mapping.json"
    CROP_MODEL_PATH: str = "ml/saved_models/crop_recommendation_model.pkl"
    
    # Storage
    UPLOAD_DIR: str = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "uploads", "disease_images")

    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()

# Ensure uploads directory exists
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
