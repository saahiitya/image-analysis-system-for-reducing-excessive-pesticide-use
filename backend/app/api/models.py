"""
Pydantic models for API request/response schemas
"""

from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class ScanRequest(BaseModel):
    crop_type: str
    farm_size: float
    location: Optional[str] = None
    weather_conditions: Optional[str] = None

class DiseaseDetectionResult(BaseModel):
    disease_detected: str
    confidence_score: float
    severity_assessment: str

class DosageCalculation(BaseModel):
    pesticide_name: str
    amount_per_hectare: float
    total_amount_needed: str
    cost_per_liter: float
    cost_estimate: str
    water_needed: str
    application_instructions: str

class TreatmentRecommendation(BaseModel):
    primary_pesticides: List[str]
    alternative_pesticides: List[str]
    application_method: str
    dosage_calculation: DosageCalculation
    timing_recommendations: List[str]

class Recommendations(BaseModel):
    disease_detected: str
    confidence_score: float
    severity_assessment: str
    recommended_treatment: TreatmentRecommendation
    prevention_tips: List[str]
    follow_up_schedule: List[str]

class EnvironmentalImpact(BaseModel):
    pesticide_reduction: float
    water_usage: float
    cost_savings: float

class ScanResponse(BaseModel):
    scan_id: int
    recommendations: Recommendations
    environmental_impact: EnvironmentalImpact

class HistoryResponse(BaseModel):
    id: int
    crop_type: str
    disease_detected: str
    confidence_score: float
    severity_level: str
    scan_timestamp: datetime
    treatment_cost: Optional[float]
    location: Optional[str]

class WeatherData(BaseModel):
    location: str
    temperature: float
    humidity: int
    wind_speed: float
    weather_condition: str
    uv_index: int
    rain_probability: int
    spraying_recommendation: str
    best_spraying_times: List[str]

class PesticideRecommendation(BaseModel):
    pesticide_name: str
    active_ingredient: str
    dosage: str
    cost: float
    application_method: str
    safety_period: int
    environmental_rating: str

class DashboardStats(BaseModel):
    total_scans: int
    healthy_crops_percentage: float
    active_treatments: int
    pesticide_saved: str
    cost_savings: str

class CropHealthMetrics(BaseModel):
    crop_type: str
    health_score: float
    disease_incidents: int
    treatment_success_rate: float
    cost_per_hectare: float