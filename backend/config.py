"""
Configuration file for CropGuard AI Platform
Customize settings here for your deployment
"""

# Server Configuration
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 8000
DEBUG_MODE = True

# Application Settings
APP_TITLE = "CropGuard AI - Precision Pesticide Management Platform"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "AI-powered crop disease detection and pesticide recommendation system"

# Image Processing Settings
MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/jpg", "image/png"]
MAX_IMAGES_PER_REQUEST = 10

# AI Model Settings
MODEL_PATH = "models/crop_disease_model"  # Path to your trained model
MODEL_CONFIDENCE_THRESHOLD = 0.7
MOCK_AI_ENABLED = False  # Set to True only for testing without model

# Currency Settings
CURRENCY = "INR"
CURRENCY_SYMBOL = "₹"
DEFAULT_FARM_AREA = 1.0  # hectares

# Feature Flags
ENABLE_CAMERA = True
ENABLE_LOCATION = True
ENABLE_WEATHER = True
ENABLE_ANALYTICS = True

# Security Settings
CORS_ORIGINS = ["*"]  # Restrict in production
MAX_REQUEST_SIZE = 50 * 1024 * 1024  # 50MB

# Regional Settings
TIMEZONE = "Asia/Kolkata"
DEFAULT_LANGUAGE = "en"