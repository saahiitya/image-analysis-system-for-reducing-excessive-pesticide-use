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

# AI Model Settings (for future integration)
MODEL_PATH = "models/"
MODEL_CONFIDENCE_THRESHOLD = 0.7
ENABLE_GPU = False

# Database Settings (for future use)
DATABASE_URL = "sqlite:///cropguard.db"
ENABLE_DATABASE = False

# Weather API Settings (for real integration)
WEATHER_API_KEY = "your_weather_api_key_here"
WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather"
ENABLE_REAL_WEATHER = False

# Location Settings
DEFAULT_LOCATION = {
    "latitude": 20.5937,  # India center
    "longitude": 78.9629,
    "city": "India"
}

# Pesticide Database Settings
CURRENCY = "INR"
CURRENCY_SYMBOL = "₹"
DEFAULT_FARM_AREA = 1.0  # hectares

# Feature Flags
ENABLE_CAMERA = True
ENABLE_LOCATION = True
ENABLE_WEATHER = True
ENABLE_ANALYTICS = True
ENABLE_HISTORY = True

# Security Settings
CORS_ORIGINS = ["*"]  # Restrict in production
MAX_REQUEST_SIZE = 50 * 1024 * 1024  # 50MB
RATE_LIMIT_REQUESTS = 100
RATE_LIMIT_WINDOW = 3600  # 1 hour

# Logging Configuration
LOG_LEVEL = "INFO"
LOG_FILE = "cropguard.log"
ENABLE_FILE_LOGGING = False

# Regional Settings
SUPPORTED_LANGUAGES = ["en", "hi", "te", "ta", "kn"]  # English, Hindi, Telugu, Tamil, Kannada
DEFAULT_LANGUAGE = "en"
TIMEZONE = "Asia/Kolkata"

# Performance Settings
CACHE_ENABLED = True
CACHE_TTL = 3600  # 1 hour
MAX_CONCURRENT_REQUESTS = 10

# Development Settings
MOCK_AI_ENABLED = True  # Set to False when real AI model is integrated
DEMO_MODE = True
SAMPLE_DATA_ENABLED = True