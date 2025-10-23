"""
Database models for CropGuard AI Platform
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean
from sqlalchemy.sql import func
from .database import Base

class CropScan(Base):
    """
    Model for storing crop scan results and analysis data
    """
    __tablename__ = "crop_scans"
    
    id = Column(Integer, primary_key=True, index=True)
    crop_type = Column(String(50), nullable=False)
    disease_detected = Column(String(100), nullable=False)
    confidence_score = Column(Float, nullable=False)
    severity_level = Column(String(20), nullable=False)
    farm_size = Column(Float, nullable=False)
    location = Column(String(200), nullable=True)
    image_path = Column(String(500), nullable=False)
    scan_timestamp = Column(DateTime(timezone=True), server_default=func.now())
    treatment_cost = Column(Float, nullable=True)
    weather_conditions = Column(Text, nullable=True)
    
class DiseaseInfo(Base):
    """
    Model for storing disease information and characteristics
    """
    __tablename__ = "disease_info"
    
    id = Column(Integer, primary_key=True, index=True)
    disease_name = Column(String(100), unique=True, nullable=False)
    crop_types = Column(Text, nullable=False)  # JSON string of affected crops
    symptoms = Column(Text, nullable=False)
    causes = Column(Text, nullable=False)
    prevention_methods = Column(Text, nullable=False)
    treatment_options = Column(Text, nullable=False)
    severity_indicators = Column(Text, nullable=False)
    
class PesticideData(Base):
    """
    Model for storing pesticide information and pricing
    """
    __tablename__ = "pesticide_data"
    
    id = Column(Integer, primary_key=True, index=True)
    pesticide_name = Column(String(100), nullable=False)
    active_ingredient = Column(String(100), nullable=False)
    target_diseases = Column(Text, nullable=False)  # JSON string
    target_crops = Column(Text, nullable=False)  # JSON string
    dosage_per_hectare = Column(Float, nullable=False)
    price_per_liter = Column(Float, nullable=False)
    application_method = Column(String(50), nullable=False)
    safety_period = Column(Integer, nullable=False)  # Days before harvest
    environmental_impact = Column(String(20), nullable=False)  # Low, Medium, High
    
class TreatmentHistory(Base):
    """
    Model for tracking treatment applications and outcomes
    """
    __tablename__ = "treatment_history"
    
    id = Column(Integer, primary_key=True, index=True)
    scan_id = Column(Integer, nullable=False)  # Reference to CropScan
    pesticide_used = Column(String(100), nullable=False)
    application_date = Column(DateTime(timezone=True), nullable=False)
    dosage_applied = Column(Float, nullable=False)
    area_treated = Column(Float, nullable=False)
    cost_incurred = Column(Float, nullable=False)
    effectiveness_rating = Column(Integer, nullable=True)  # 1-5 scale
    notes = Column(Text, nullable=True)
    
class WeatherLog(Base):
    """
    Model for storing weather data for analysis
    """
    __tablename__ = "weather_log"
    
    id = Column(Integer, primary_key=True, index=True)
    location = Column(String(200), nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    temperature = Column(Float, nullable=False)
    humidity = Column(Float, nullable=False)
    wind_speed = Column(Float, nullable=False)
    weather_condition = Column(String(50), nullable=False)
    uv_index = Column(Float, nullable=True)
    rain_probability = Column(Float, nullable=True)
    
class UserProfile(Base):
    """
    Model for farmer/user profiles
    """
    __tablename__ = "user_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    full_name = Column(String(100), nullable=False)
    phone_number = Column(String(20), nullable=True)
    farm_location = Column(String(200), nullable=True)
    total_farm_area = Column(Float, nullable=True)
    primary_crops = Column(Text, nullable=True)  # JSON string
    registration_date = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)