from typing import Optional, Dict
import random

# This is a placeholder for a real ML model.
# It simulates disease detection for tomato, brinjal, and capsicum.

DISEASES = {
    "tomato": [
        "Early blight",
        "Late blight",
        "Bacterial spot",
        "Septoria leaf spot",
        "Leaf mold",
    ],
    "brinjal": [
        "Phomopsis blight",
        "Bacterial wilt",
        "Little leaf",
        "Shoot and fruit borer",
    ],
    "capsicum": [
        "Anthracnose",
        "Phytophthora blight",
        "Powdery mildew",
        "Bacterial leaf spot",
    ],
}

SEVERITIES = ["low", "moderate", "high"]


def analyze_image_and_metadata(
    image_path: str,
    crop_type: str,
    location: Optional[str] = None,
    weather_conditions: Optional[str] = None,
) -> Dict[str, str]:
    random.seed(hash((image_path, crop_type)) % (2**32 - 1))
    disease_list = DISEASES.get(crop_type.lower(), []) or ["Unknown disease"]
    disease = random.choice(disease_list)
    severity = random.choices(SEVERITIES, weights=[0.5, 0.35, 0.15])[0]

    return {
        "disease_detected": disease,
        "severity_assessment": severity,
    }
