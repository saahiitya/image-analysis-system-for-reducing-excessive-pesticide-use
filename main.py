from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
import json
import random
from datetime import datetime
from typing import List, Optional
import numpy as np
from PIL import Image
import io
import base64
import config

app = FastAPI(
    title=config.APP_TITLE,
    version=config.APP_VERSION,
    description=config.APP_DESCRIPTION
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Disease database with Indian pesticide recommendations
DISEASE_DATABASE = {
    "tomato": {
        "early_blight": {
            "name": "Early Blight",
            "description": "Fungal disease causing dark spots on leaves",
            "severity_levels": {
                "low": {
                    "pesticides": [
                        {"name": "Mancozeb 75% WP", "dosage": "2-2.5g/L", "cost_per_kg": 180, "application_rate": "500-600L/hectare"},
                        {"name": "Copper Oxychloride 50% WP", "dosage": "2-3g/L", "cost_per_kg": 120, "application_rate": "500L/hectare"}
                    ]
                },
                "medium": {
                    "pesticides": [
                        {"name": "Propiconazole 25% EC", "dosage": "1ml/L", "cost_per_L": 850, "application_rate": "600L/hectare"},
                        {"name": "Azoxystrobin 23% SC", "dosage": "1ml/L", "cost_per_L": 1200, "application_rate": "500L/hectare"}
                    ]
                },
                "high": {
                    "pesticides": [
                        {"name": "Tebuconazole 25.9% EC", "dosage": "1ml/L", "cost_per_L": 950, "application_rate": "600-700L/hectare"},
                        {"name": "Difenoconazole 25% EC", "dosage": "0.5ml/L", "cost_per_L": 1100, "application_rate": "600L/hectare"}
                    ]
                }
            }
        },
        "late_blight": {
            "name": "Late Blight",
            "description": "Serious fungal disease affecting leaves and fruits",
            "severity_levels": {
                "low": {
                    "pesticides": [
                        {"name": "Metalaxyl 8% + Mancozeb 64% WP", "dosage": "2.5g/L", "cost_per_kg": 320, "application_rate": "500L/hectare"}
                    ]
                },
                "medium": {
                    "pesticides": [
                        {"name": "Cymoxanil 8% + Mancozeb 64% WP", "dosage": "2g/L", "cost_per_kg": 280, "application_rate": "600L/hectare"}
                    ]
                },
                "high": {
                    "pesticides": [
                        {"name": "Dimethomorph 9% + Mancozeb 60% WP", "dosage": "2g/L", "cost_per_kg": 450, "application_rate": "700L/hectare"}
                    ]
                }
            }
        },
        "bacterial_wilt": {
            "name": "Bacterial Wilt",
            "description": "Bacterial infection causing plant wilting",
            "severity_levels": {
                "low": {
                    "pesticides": [
                        {"name": "Streptocycline 9% + Tetracycline 1% SP", "dosage": "0.5g/L", "cost_per_kg": 650, "application_rate": "400L/hectare"}
                    ]
                },
                "medium": {
                    "pesticides": [
                        {"name": "Copper Sulphate 25% WP", "dosage": "2g/L", "cost_per_kg": 150, "application_rate": "500L/hectare"}
                    ]
                },
                "high": {
                    "pesticides": [
                        {"name": "Kasugamycin 3% SL", "dosage": "2ml/L", "cost_per_L": 800, "application_rate": "600L/hectare"}
                    ]
                }
            }
        }
    },
    "brinjal": {
        "fruit_borer": {
            "name": "Brinjal Fruit and Shoot Borer",
            "description": "Major pest causing fruit damage",
            "severity_levels": {
                "low": {
                    "pesticides": [
                        {"name": "Bt (Bacillus thuringiensis)", "dosage": "1-2g/L", "cost_per_kg": 400, "application_rate": "500L/hectare"}
                    ]
                },
                "medium": {
                    "pesticides": [
                        {"name": "Emamectin Benzoate 5% SG", "dosage": "0.4g/L", "cost_per_kg": 2200, "application_rate": "500L/hectare"}
                    ]
                },
                "high": {
                    "pesticides": [
                        {"name": "Chlorantraniliprole 18.5% SC", "dosage": "0.3ml/L", "cost_per_L": 3200, "application_rate": "600L/hectare"}
                    ]
                }
            }
        },
        "little_leaf": {
            "name": "Little Leaf Disease",
            "description": "Phytoplasma disease causing stunted growth",
            "severity_levels": {
                "low": {
                    "pesticides": [
                        {"name": "Imidacloprid 17.8% SL", "dosage": "0.5ml/L", "cost_per_L": 850, "application_rate": "400L/hectare"}
                    ]
                },
                "medium": {
                    "pesticides": [
                        {"name": "Thiamethoxam 25% WG", "dosage": "0.2g/L", "cost_per_kg": 1800, "application_rate": "500L/hectare"}
                    ]
                },
                "high": {
                    "pesticides": [
                        {"name": "Acetamiprid 20% SP", "dosage": "0.2g/L", "cost_per_kg": 1200, "application_rate": "600L/hectare"}
                    ]
                }
            }
        },
        "damping_off": {
            "name": "Damping Off",
            "description": "Fungal disease affecting seedlings",
            "severity_levels": {
                "low": {
                    "pesticides": [
                        {"name": "Captan 70% + Hexaconazole 5% WP", "dosage": "2g/L", "cost_per_kg": 380, "application_rate": "300L/hectare"}
                    ]
                },
                "medium": {
                    "pesticides": [
                        {"name": "Carbendazim 12% + Mancozeb 63% WP", "dosage": "2g/L", "cost_per_kg": 220, "application_rate": "400L/hectare"}
                    ]
                },
                "high": {
                    "pesticides": [
                        {"name": "Fosetyl Aluminium 80% WP", "dosage": "2.5g/L", "cost_per_kg": 750, "application_rate": "500L/hectare"}
                    ]
                }
            }
        }
    },
    "capsicum": {
        "anthracnose": {
            "name": "Anthracnose",
            "description": "Fungal disease causing fruit rot",
            "severity_levels": {
                "low": {
                    "pesticides": [
                        {"name": "Mancozeb 75% WP", "dosage": "2g/L", "cost_per_kg": 180, "application_rate": "500L/hectare"}
                    ]
                },
                "medium": {
                    "pesticides": [
                        {"name": "Carbendazim 50% WP", "dosage": "1g/L", "cost_per_kg": 280, "application_rate": "500L/hectare"}
                    ]
                },
                "high": {
                    "pesticides": [
                        {"name": "Azoxystrobin 23% SC", "dosage": "1ml/L", "cost_per_L": 1200, "application_rate": "600L/hectare"}
                    ]
                }
            }
        },
        "powdery_mildew": {
            "name": "Powdery Mildew",
            "description": "Fungal disease with white powdery growth",
            "severity_levels": {
                "low": {
                    "pesticides": [
                        {"name": "Wettable Sulphur 80% WP", "dosage": "2g/L", "cost_per_kg": 120, "application_rate": "400L/hectare"}
                    ]
                },
                "medium": {
                    "pesticides": [
                        {"name": "Triadimefon 25% WP", "dosage": "1g/L", "cost_per_kg": 450, "application_rate": "500L/hectare"}
                    ]
                },
                "high": {
                    "pesticides": [
                        {"name": "Hexaconazole 5% EC", "dosage": "2ml/L", "cost_per_L": 680, "application_rate": "600L/hectare"}
                    ]
                }
            }
        },
        "thrips": {
            "name": "Thrips",
            "description": "Insect pest causing leaf damage",
            "severity_levels": {
                "low": {
                    "pesticides": [
                        {"name": "Fipronil 5% SC", "dosage": "2ml/L", "cost_per_L": 950, "application_rate": "400L/hectare"}
                    ]
                },
                "medium": {
                    "pesticides": [
                        {"name": "Imidacloprid 17.8% SL", "dosage": "0.5ml/L", "cost_per_L": 850, "application_rate": "500L/hectare"}
                    ]
                },
                "high": {
                    "pesticides": [
                        {"name": "Spinosad 45% SC", "dosage": "0.3ml/L", "cost_per_L": 2800, "application_rate": "600L/hectare"}
                    ]
                }
            }
        }
    }
}

# Mock AI model for disease detection
def detect_disease(image_data, crop_type):
    """
    Mock AI disease detection function
    In production, this would use a trained deep learning model
    """
    diseases = list(DISEASE_DATABASE.get(crop_type.lower(), {}).keys())
    if not diseases:
        return None
    
    # Simulate AI detection with random selection for demo
    detected_disease = random.choice(diseases)
    confidence = random.uniform(0.75, 0.95)
    severity = random.choice(['low', 'medium', 'high'])
    affected_area = random.uniform(10, 80)  # percentage
    
    return {
        "disease": detected_disease,
        "confidence": round(confidence, 2),
        "severity": severity,
        "affected_area_percentage": round(affected_area, 1)
    }

def calculate_pesticide_cost(pesticide_info, area_hectares, severity):
    """Calculate total cost for pesticide application"""
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
    else:  # ml
        total_pesticide_needed = (dosage_val * total_water_needed) / 1000  # Convert to L
        cost_per_unit = pesticide_info.get("cost_per_L", 800)
    
    # Adjust for severity
    severity_multiplier = {"low": 1.0, "medium": 1.2, "high": 1.5}
    total_pesticide_needed *= severity_multiplier.get(severity, 1.0)
    
    total_cost = total_pesticide_needed * cost_per_unit
    
    return {
        "pesticide_amount": round(total_pesticide_needed, 2),
        "unit": "kg" if dosage_unit == "g" else "L",
        "water_needed": round(total_water_needed, 0),
        "total_cost": round(total_cost, 2)
    }

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the main HTML page"""
    with open("pesticide.html", "r") as f:
        return HTMLResponse(content=f.read())

@app.post("/analyze-crop")
async def analyze_crop(
    crop_type: str = Form(...),
    area_hectares: float = Form(default=1.0),
    files: List[UploadFile] = File(...)
):
    """
    Analyze crop images and provide disease detection with pesticide recommendations
    """
    try:
        if not files:
            raise HTTPException(status_code=400, detail="No images provided")
        
        results = []
        
        for file in files:
            # Read image
            image_data = await file.read()
            image = Image.open(io.BytesIO(image_data))
            
            # Convert image to base64 for frontend display
            buffered = io.BytesIO()
            image.save(buffered, format="JPEG")
            img_base64 = base64.b64encode(buffered.getvalue()).decode()
            
            # Detect disease using mock AI
            detection_result = detect_disease(image_data, crop_type)
            
            if detection_result:
                disease_key = detection_result["disease"]
                severity = detection_result["severity"]
                
                # Get disease info and pesticide recommendations
                disease_info = DISEASE_DATABASE[crop_type.lower()][disease_key]
                pesticide_options = disease_info["severity_levels"][severity]["pesticides"]
                
                # Calculate costs for each pesticide option
                pesticide_recommendations = []
                for pesticide in pesticide_options:
                    cost_calc = calculate_pesticide_cost(pesticide, area_hectares, severity)
                    pesticide_recommendations.append({
                        **pesticide,
                        **cost_calc
                    })
                
                results.append({
                    "filename": file.filename,
                    "image_base64": img_base64,
                    "detection": {
                        "disease_name": disease_info["name"],
                        "description": disease_info["description"],
                        "confidence": detection_result["confidence"],
                        "severity": severity,
                        "affected_area_percentage": detection_result["affected_area_percentage"]
                    },
                    "pesticide_recommendations": pesticide_recommendations,
                    "timestamp": datetime.now().isoformat()
                })
            else:
                results.append({
                    "filename": file.filename,
                    "image_base64": img_base64,
                    "detection": {
                        "disease_name": "Healthy",
                        "description": "No disease detected",
                        "confidence": 0.95,
                        "severity": "none",
                        "affected_area_percentage": 0
                    },
                    "pesticide_recommendations": [],
                    "timestamp": datetime.now().isoformat()
                })
        
        return JSONResponse(content={
            "status": "success",
            "crop_type": crop_type,
            "area_hectares": area_hectares,
            "total_images": len(files),
            "results": results
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.get("/weather")
async def get_weather():
    """
    Get current weather conditions (mock data)
    In production, this would integrate with a weather API
    """
    return {
        "temperature": random.randint(20, 35),
        "humidity": random.randint(30, 80),
        "wind_speed": random.randint(5, 15),
        "uv_index": random.randint(1, 8),
        "rain_probability": random.randint(0, 30),
        "condition": random.choice(["Sunny", "Partly Cloudy", "Cloudy", "Clear"]),
        "spray_recommendation": {
            "suitable": random.choice([True, False]),
            "best_time": "Morning (6-10 AM) or Evening (4-7 PM)",
            "warning": "Avoid spraying during high wind or rain"
        }
    }

@app.get("/scan-history")
async def get_scan_history():
    """Get scan history (mock data)"""
    return {
        "total_scans": random.randint(15, 50),
        "healthy_percentage": random.randint(60, 85),
        "active_treatments": random.randint(2, 8),
        "pesticide_saved": random.randint(50, 200),
        "cost_savings": random.randint(2000, 8000)
    }

if __name__ == "__main__":
    uvicorn.run(
        app, 
        host=config.SERVER_HOST, 
        port=config.SERVER_PORT,
        reload=config.DEBUG_MODE
    )