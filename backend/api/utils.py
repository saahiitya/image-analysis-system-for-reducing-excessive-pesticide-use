"""
Utility functions for API operations
"""

import random
from typing import Dict, List
from ..models.disease_db import get_disease_info, get_pesticide_recommendations

def calculate_pesticide_cost(pesticide_info: Dict, area_hectares: float, severity: str) -> Dict:
    """
    Calculate total cost for pesticide application
    
    Args:
        pesticide_info: Pesticide information from database
        area_hectares: Farm area in hectares
        severity: Disease severity level
    
    Returns:
        Dictionary with cost calculations
    """
    dosage = pesticide_info["dosage"]
    application_rate = pesticide_info["application_rate"]
    
    # Extract numeric values from dosage and application rate
    if "g/L" in dosage:
        dosage_val = float(dosage.split("g/L")[0].split("-")[-1])
        dosage_unit = "g"
    elif "ml/L" in dosage:
        dosage_val = float(dosage.split("ml/L")[0].split("-")[-1])
        dosage_unit = "ml"
    else:
        dosage_val = 2.0
        dosage_unit = "g"
    
    # Extract application rate
    app_rate = float(application_rate.split("L/hectare")[0].split("-")[-1])
    
    # Calculate total pesticide needed
    total_water_needed = app_rate * area_hectares
    
    if dosage_unit == "g":
        total_pesticide_needed = (dosage_val * total_water_needed) / 1000  # Convert to kg
        cost_per_unit = pesticide_info.get("cost_per_kg", 200)
        unit = "kg"
    else:  # ml
        total_pesticide_needed = (dosage_val * total_water_needed) / 1000  # Convert to L
        cost_per_unit = pesticide_info.get("cost_per_L", 800)
        unit = "L"
    
    # Adjust for severity
    severity_multiplier = {"low": 1.0, "medium": 1.2, "high": 1.5}
    total_pesticide_needed *= severity_multiplier.get(severity, 1.0)
    
    total_cost = total_pesticide_needed * cost_per_unit
    
    return {
        "pesticide_amount": round(total_pesticide_needed, 2),
        "unit": unit,
        "water_needed": round(total_water_needed, 0),
        "total_cost": round(total_cost, 2),
        "cost_per_unit": cost_per_unit,
        "application_rate": application_rate,
        "severity_multiplier": severity_multiplier.get(severity, 1.0)
    }

def generate_treatment_recommendations(crop_type: str, disease_key: str, severity: str, 
                                     area_hectares: float) -> List[Dict]:
    """
    Generate comprehensive treatment recommendations
    
    Args:
        crop_type: Type of crop
        disease_key: Disease identifier
        severity: Severity level
        area_hectares: Farm area
    
    Returns:
        List of pesticide recommendations with costs
    """
    pesticides = get_pesticide_recommendations(crop_type, disease_key, severity)
    recommendations = []
    
    for pesticide in pesticides:
        cost_calc = calculate_pesticide_cost(pesticide, area_hectares, severity)
        
        recommendation = {
            **pesticide,
            **cost_calc,
            "effectiveness_rating": _get_effectiveness_rating(pesticide, severity),
            "environmental_impact": _get_environmental_impact(pesticide),
            "application_timing": _get_application_timing(disease_key, severity),
            "precautions": _get_precautions(pesticide)
        }
        recommendations.append(recommendation)
    
    # Sort by cost-effectiveness
    recommendations.sort(key=lambda x: x["total_cost"] / x["effectiveness_rating"])
    
    return recommendations

def _get_effectiveness_rating(pesticide: Dict, severity: str) -> float:
    """Get effectiveness rating for pesticide based on active ingredient and severity"""
    effectiveness_map = {
        "low": {"Mancozeb": 4.5, "Copper": 4.0, "Sulphur": 4.2, "Bt": 4.8},
        "medium": {"Propiconazole": 4.7, "Azoxystrobin": 4.6, "Imidacloprid": 4.5},
        "high": {"Tebuconazole": 4.8, "Chlorantraniliprole": 4.9, "Spinosad": 4.7}
    }
    
    active_ingredient = pesticide.get("active_ingredient", "").split()[0]
    return effectiveness_map.get(severity, {}).get(active_ingredient, 4.0)

def _get_environmental_impact(pesticide: Dict) -> str:
    """Assess environmental impact of pesticide"""
    active_ingredient = pesticide.get("active_ingredient", "").lower()
    
    if any(bio in active_ingredient for bio in ["bt", "bacillus", "spinosad"]):
        return "Low - Biological/Organic"
    elif any(copper in active_ingredient for copper in ["copper", "sulphur"]):
        return "Low-Medium - Mineral based"
    elif "mancozeb" in active_ingredient:
        return "Medium - Contact fungicide"
    else:
        return "Medium-High - Synthetic"

def _get_application_timing(disease_key: str, severity: str) -> str:
    """Get optimal application timing"""
    timing_map = {
        "early_blight": "Early morning or evening, avoid midday heat",
        "late_blight": "Preventive spraying before rain, early morning preferred",
        "bacterial_wilt": "Soil drenching in evening, avoid overhead spraying",
        "fruit_borer": "Evening application when larvae are active",
        "little_leaf": "Morning application, target vector insects",
        "damping_off": "Soil treatment before sowing, morning application",
        "anthracnose": "Preventive spraying before fruit development",
        "powdery_mildew": "Early morning when humidity is high",
        "thrips": "Early morning or evening when thrips are active"
    }
    
    base_timing = timing_map.get(disease_key, "Early morning or evening")
    
    if severity == "high":
        return f"{base_timing}. Repeat application after 7-10 days"
    elif severity == "medium":
        return f"{base_timing}. Monitor and reapply if needed"
    else:
        return f"{base_timing}. Single application may be sufficient"

def _get_precautions(pesticide: Dict) -> List[str]:
    """Get safety precautions for pesticide use"""
    base_precautions = [
        "Wear protective clothing and gloves",
        "Avoid spraying during windy conditions",
        "Do not spray during flowering to protect pollinators",
        "Follow pre-harvest interval guidelines"
    ]
    
    active_ingredient = pesticide.get("active_ingredient", "").lower()
    
    if "copper" in active_ingredient:
        base_precautions.append("Avoid repeated use to prevent copper buildup")
    
    if any(systemic in active_ingredient for systemic in ["propiconazole", "tebuconazole"]):
        base_precautions.append("Rotate with different mode of action to prevent resistance")
    
    if "imidacloprid" in active_ingredient:
        base_precautions.append("Highly toxic to bees - avoid application during bloom")
    
    return base_precautions

def generate_mock_weather_data() -> Dict:
    """Generate mock weather data for demonstration"""
    temperature = random.randint(20, 35)
    humidity = random.randint(30, 80)
    wind_speed = random.randint(5, 15)
    uv_index = random.randint(1, 8)
    rain_probability = random.randint(0, 30)
    
    conditions = ["Sunny", "Partly Cloudy", "Cloudy", "Clear"]
    condition = random.choice(conditions)
    
    # Determine spray suitability
    suitable = (
        wind_speed <= 10 and 
        rain_probability <= 20 and 
        temperature <= 32 and
        humidity >= 40
    )
    
    return {
        "temperature": temperature,
        "humidity": humidity,
        "wind_speed": wind_speed,
        "uv_index": uv_index,
        "rain_probability": rain_probability,
        "condition": condition,
        "spray_recommendation": {
            "suitable": suitable,
            "best_time": "Morning (6-10 AM) or Evening (4-7 PM)",
            "warning": "Avoid spraying during high wind or rain" if not suitable else "Good conditions for application"
        }
    }

def generate_mock_scan_history() -> Dict:
    """Generate mock scan history data"""
    return {
        "total_scans": random.randint(15, 50),
        "healthy_percentage": random.randint(60, 85),
        "active_treatments": random.randint(2, 8),
        "pesticide_saved": random.randint(50, 200),
        "cost_savings": random.randint(2000, 8000),
        "environmental_impact": {
            "pesticide_reduction": random.randint(15, 35),
            "water_saved": random.randint(100, 500),
            "carbon_footprint_reduced": random.randint(10, 50)
        }
    }