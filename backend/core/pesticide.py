from typing import Dict, List

# Basic pesticide catalog and simple dosage + cost estimation logic.
# Real logic should consider label rates, formulation, PHI, resistance management.

CATALOG: Dict[str, Dict[str, Dict[str, Dict]]] = {
    "tomato": {
        "Early blight": {
            "actives": ["Mancozeb", "Chlorothalonil"],
            "dose_per_ha_l": 0.8,
            "price_per_l": 600.0,
        },
        "Late blight": {
            "actives": ["Metalaxyl", "Copper oxychloride"],
            "dose_per_ha_l": 1.2,
            "price_per_l": 750.0,
        },
        "Bacterial spot": {
            "actives": ["Copper hydroxide"],
            "dose_per_ha_l": 1.0,
            "price_per_l": 680.0,
        },
        "Septoria leaf spot": {
            "actives": ["Chlorothalonil"],
            "dose_per_ha_l": 0.9,
            "price_per_l": 620.0,
        },
        "Leaf mold": {
            "actives": ["Copper oxychloride"],
            "dose_per_ha_l": 0.7,
            "price_per_l": 640.0,
        },
    },
    "brinjal": {
        "Phomopsis blight": {
            "actives": ["Carbendazim", "Mancozeb"],
            "dose_per_ha_l": 0.8,
            "price_per_l": 550.0,
        },
        "Bacterial wilt": {
            "actives": ["Copper oxychloride"],
            "dose_per_ha_l": 1.0,
            "price_per_l": 640.0,
        },
        "Little leaf": {
            "actives": ["Imidacloprid"],
            "dose_per_ha_l": 0.3,
            "price_per_l": 900.0,
        },
        "Shoot and fruit borer": {
            "actives": ["Emamectin benzoate"],
            "dose_per_ha_l": 0.2,
            "price_per_l": 1200.0,
        },
    },
    "capsicum": {
        "Anthracnose": {
            "actives": ["Azoxystrobin", "Difenoconazole"],
            "dose_per_ha_l": 0.5,
            "price_per_l": 1100.0,
        },
        "Phytophthora blight": {
            "actives": ["Metalaxyl", "Mancozeb"],
            "dose_per_ha_l": 1.0,
            "price_per_l": 780.0,
        },
        "Powdery mildew": {
            "actives": ["Sulfur"],
            "dose_per_ha_l": 1.2,
            "price_per_l": 350.0,
        },
        "Bacterial leaf spot": {
            "actives": ["Copper hydroxide"],
            "dose_per_ha_l": 0.8,
            "price_per_l": 680.0,
        },
    },
}

SEVERITY_MULTIPLIER = {"low": 0.7, "moderate": 1.0, "high": 1.3}


def get_pesticide_catalog() -> Dict:
    return CATALOG


def compute_pesticide_plan(
    crop_type: str,
    disease: str,
    severity: str,
    farm_size_ha: float,
    weather_conditions: str | None,
) -> Dict:
    crop_key = crop_type.lower()
    entry = CATALOG.get(crop_key, {}).get(disease)

    if not entry:
        # Default/fallback
        actives: List[str] = ["General copper fungicide"]
        dose_per_ha_l = 0.8
        price_per_l = 600.0
    else:
        actives = entry["actives"]
        dose_per_ha_l = entry["dose_per_ha_l"]
        price_per_l = entry["price_per_l"]

    severity_multiplier = SEVERITY_MULTIPLIER.get(severity, 1.0)

    # Weather adjustment: avoid recommending spray in rain/wind, but for demo we just adjust dose slightly
    weather_multiplier = 1.0
    if weather_conditions:
        text = weather_conditions.lower()
        if "rain" in text:
            weather_multiplier *= 1.1
        if "wind" in text:
            weather_multiplier *= 1.05
        if "hot" in text or ">35" in text or "heat" in text:
            weather_multiplier *= 0.95

    liters_needed = dose_per_ha_l * severity_multiplier * weather_multiplier * max(farm_size_ha, 0.01)
    liters_needed = round(liters_needed, 2)
    cost = round(liters_needed * price_per_l, 2)

    return {
        "recommended_treatment": {
            "primary_pesticides": actives,
            "dosage_calculation": {
                "dose_per_hectare": f"{dose_per_ha_l} L/ha",
                "severity_multiplier": severity_multiplier,
                "weather_multiplier": round(weather_multiplier, 2),
                "farm_size_hectares": farm_size_ha,
                "total_amount_needed": f"{liters_needed} L",
                "cost_estimate": f"₹{cost}",
            },
            "application_guidance": [
                "Spray during calm hours: early morning or late evening",
                "Ensure full leaf coverage, avoid runoff",
                "Rotate modes of action to manage resistance",
                "Follow local regulations and label instructions",
            ],
        }
    }
