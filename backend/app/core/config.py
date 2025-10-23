"""
Configuration settings for CropGuard AI Platform
"""

import os
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Application
    app_name: str = "CropGuard AI Platform"
    app_version: str = "1.0.0"
    debug: bool = True
    
    # Database
    database_url: str = "sqlite:///./cropguard.db"
    
    # API Keys (would be loaded from environment variables in production)
    openweather_api_key: Optional[str] = None
    google_maps_api_key: Optional[str] = None
    
    # AI Model Paths
    disease_model_path: str = "models/disease_detection/crop_disease_model.h5"
    pesticide_model_path: str = "models/pesticide_recommendation/pesticide_model.pkl"
    
    # File Upload Settings
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    allowed_extensions: list = [".jpg", ".jpeg", ".png", ".bmp", ".tiff"]
    upload_directory: str = "data/uploads"
    
    # Security
    secret_key: str = "your-secret-key-here"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    class Config:
        env_file = ".env"

settings = Settings()