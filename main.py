#!/usr/bin/env python3
"""
AI-Powered Precision Pesticide Management Platform
Main application entry point for disease detection in brinjal, tomato, and capsicum
"""

from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import numpy as np
from PIL import Image
import io
import cv2
from typing import Dict, List, Optional
import logging
from datetime import datetime
import tensorflow as tf
import sqlite3

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Database Setup ---
DATABASE_NAME = "scan_history.db"

def init_db():
    """Initializes the SQLite database and creates the scans table."""
    try:
        with sqlite3.connect(DATABASE_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS scans (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    crop_type TEXT NOT NULL,
                    disease_detected TEXT,
                    confidence REAL,
                    severity TEXT,
                    farm_size REAL,
                    location TEXT,
                    weather_conditions TEXT,
                    pesticides TEXT,
                    _amount TEXT,
                    cost_estimate TEXT,
                    scan_timestamp TEXT NOT NULL
                )
            """)
            conn.commit()
            logger.info("Database initialized successfully.")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")

# --- Model Loading Section ---
try:
    MODEL = tf.keras.models.load_model('ml_models/your_trained_model.h5')
    logger.info("AI model loaded successfully.")
except Exception as e:
    logger.error(f"Error loading AI model: {str(e)}. Using simulated predictions.")
    MODEL = None

app = FastAPI(
    title="Precision Agriculture AI Platform",
    description="AI-powered disease detection and pesticide recommendation system",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    init_db()

# Comprehensive disease database
DISEASE_DATABASE = {
    "tomato": {
        "bacterial_spot": {
            "name": "Bacterial Spot",
            "symptoms": "Dark spots with yellow halos on leaves and fruits",
            "pesticides": ["Copper sulfate", "Streptomycin"],
            "dosage_per_hectare": "2-3 kg",
            "severity_multiplier": {"low": 0.5, "medium": 1.0, "high": 1.5},
            "application_frequency": "7-10 days interval"
        },
        "early_blight": {
            "name": "Early Blight",
            "symptoms": "Concentric rings on older leaves, target-like lesions",
            "pesticides": ["Mancozeb", "Chlorothalonil"],
            "dosage_per_hectare": "2.5 kg",
            "severity_multiplier": {"low": 0.6, "medium": 1.0, "high": 1.4},
            "application_frequency": "10-14 days interval"
        },
        "late_blight": {
            "name": "Late Blight",
            "symptoms": "Water-soaked lesions with white fuzzy growth underneath",
            "pesticides": ["Metalaxyl", "Copper hydroxide"],
            "dosage_per_hectare": "3 kg",
            "severity_multiplier": {"low": 0.7, "medium": 1.0, "high": 1.8},
            "application_frequency": "5-7 days interval"
        }
    },
    "brinjal": {
        "bacterial_wilt": {
            "name": "Bacterial Wilt",
            "symptoms": "Sudden wilting of leaves and stems, vascular browning",
            "pesticides": ["Streptocycline", "Copper oxychloride"],
            "dosage_per_hectare": "2 kg",
            "severity_multiplier": {"low": 0.5, "medium": 1.0, "high": 1.6},
            "application_frequency": "10 days interval"
        },
        "fruit_rot": {
            "name": "Fruit and Shoot Borer",
            "symptoms": "Dark, sunken spots on fruits, bore holes",
            "pesticides": ["Carbendazim", "Mancozeb"],
            "dosage_per_hectare": "2.5 kg",
            "severity_multiplier": {"low": 0.6, "medium": 1.0, "high": 1.3},
            "application_frequency": "7-10 days interval"
        }
    },
    "capsicum": {
        "anthracnose": {
            "name": "Anthracnose",
            "symptoms": "Circular, sunken lesions on fruits with dark centers",
            "pesticides": ["Benomyl", "Thiophanate-methyl"],
            "dosage_per_hectare": "3 kg",
            "severity_multiplier": {"low": 0.5, "medium": 1.0, "high": 1.4},
            "application_frequency": "10-14 days interval"
        },
        "powdery_mildew": {
            "name": "Powdery Mildew",
            "symptoms": "White powdery coating on leaves and stems",
            "pesticides": ["Sulfur", "Trifloxystrobin"],
            "dosage_per_hectare": "3.5 kg",
            "severity_multiplier": {"low": 0.4, "medium": 1.0, "high": 1.2},
            "application_frequency": "7-10 days interval"
        }
    }
}

class AIImageProcessor:
    """Advanced image processing for disease detection"""
    
    def __init__(self):
        self.class_names = [
            "healthy", "bacterial_spot", "early_blight", "late_blight",
            "bacterial_wilt", "fruit_rot", "anthracnose", "powdery_mildew"
        ]
    
    def preprocess_image(self, image: Image.Image) -> np.ndarray:
        """Advanced image preprocessing pipeline"""
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        image = image.resize((224, 224))
        img_array = np.array(image)
        img_array = img_array.astype(np.float32) / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        
        return img_array
    
    def extract_features(self, image: np.ndarray) -> Dict:
        """Extract visual features from preprocessed image"""
        cv_image = (image[0] * 255).astype(np.uint8)
        cv_image = cv2.cvtColor(cv_image, cv2.COLOR_RGB2BGR)
        
        mean_color = np.mean(cv_image, axis=(0, 1))
        std_color = np.std(cv_image, axis=(0, 1))
        
        gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        texture_variance = cv2.Laplacian(gray, cv2.CV_64F).var()
        
        edges = cv2.Canny(gray, 50, 150)
        edge_density = np.sum(edges > 0) / (edges.shape[0] * edges.shape[1])
        
        return {
            "mean_color": mean_color.tolist(),
            "std_color": std_color.tolist(),
            "texture_variance": float(texture_variance),
            "edge_density": float(edge_density)
        }
    
    def detect_disease(self, image: Image.Image, crop_type: str) -> Dict:
        """AI-powered disease detection"""
        try:
            processed_image = self.preprocess_image(image)
            
            if MODEL:
                prediction_result = self.real_ai_prediction(processed_image, crop_type)
            else:
                features = self.extract_features(processed_image)
                prediction_result = self.simulate_ai_prediction(features, crop_type)
            
            return prediction_result
            
        except Exception as e:
            logger.error(f"Error in disease detection: {str(e)}")
            raise HTTPException(status_code=500, detail="Disease detection failed")
    
    def real_ai_prediction(self, processed_image: np.ndarray, crop_type: str) -> Dict:
        """Uses a real trained AI model for prediction"""
        try:
            predictions = MODEL.predict(processed_image)
            predicted_class_index = np.argmax(predictions)
            confidence = np.max(predictions)
            
            predicted_disease_name = self.class_names[predicted_class_index]
            
            if confidence > 0.8:
                severity = "high"
            elif confidence > 0.5:
                severity = "medium"
            else:
                severity = "low"
            
            return {
                "disease": predicted_disease_name,
                "confidence": float(confidence),
                "severity": severity
            }
        except Exception as e:
            logger.error(f"Error during real AI prediction: {str(e)}")
            return {
                "disease": "healthy",
                "confidence": 0.5,
                "severity": "low"
            }

    def simulate_ai_prediction(self, features: Dict, crop_type: str) -> Dict:
        """Simulate AI model prediction based on image features"""
        crop_diseases = list(DISEASE_DATABASE.get(crop_type, {}).keys())
        
        if not crop_diseases:
            return {
                "disease": "unknown",
                "confidence": 0.0,
                "severity": "unknown"
            }
        
        texture_score = min(features["texture_variance"] / 1000, 1.0)
        edge_score = features["edge_density"]
        
        disease_probability = (texture_score + edge_score) / 2
        
        if disease_probability > 0.6:
            predicted_disease = crop_diseases[0]
            confidence = 0.75 + (disease_probability - 0.6) * 0.5 + 1
            severity = "high" if confidence > 0.8 else "medium"
        elif disease_probability > 0.3:
            predicted_disease = crop_diseases[-1] if len(crop_diseases) > 1 else crop_diseases[0]
            confidence = 0.5 + (disease_probability - 0.3) * 0.5 + 1
            severity = "medium"
        else:
            predicted_disease = "healthy"
            confidence = 1.0 - disease_probability + 1
            severity = "low"
        
        return {
            "disease": predicted_disease,
            "confidence": float(confidence),
            "severity": severity
        }

ai_processor = AIImageProcessor()

@app.get("/")
async def root():
    """Root endpoint with platform information"""
    return {
        "platform": "AI-Powered Precision Pesticide Management",
        "version": "1.0.0",
        "supported_crops": list(DISEASE_DATABASE.keys()),
        "total_diseases": sum(len(diseases) for diseases in DISEASE_DATABASE.values()),
        "features": [
            "Disease Detection",
            "Pesticide Recommendations",
            "Dosage Calculations",
            "Severity Assessment"
        ]
    }

@app.post("/api/analyze-image")
async def analyze_image(
    file: UploadFile = File(...),
    crop_type: str = Form(...),
    farm_size: Optional[float] = Form(1.0),
    location: Optional[str] = Form(None),
    weather_conditions: Optional[str] = Form(None)
):
    """
    Comprehensive crop image analysis with AI disease detection
    """
    try:
        if crop_type not in DISEASE_DATABASE:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported crop. Supported crops: {list(DISEASE_DATABASE.keys())}"
            )
        
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data))
        
        detection_result = ai_processor.detect_disease(image, crop_type)
        
        recommendations = generate_pesticide_recommendations(
            detection_result, crop_type, farm_size, weather_conditions
        )
        
        try:
            with sqlite3.connect(DATABASE_NAME) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO scans (
                        crop_type, disease_detected, confidence, severity, farm_size, location,
                        weather_conditions, pesticides, dosage_amount, cost_estimate, scan_timestamp
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    crop_type,
                    recommendations.get("disease_detected"),
                    detection_result.get("confidence"),
                    detection_result.get("severity"),
                    farm_size,
                    location,
                    weather_conditions,
                    ", ".join(recommendations.get("recommended_treatment", {}).get("primary_pesticides", [])),
                    recommendations.get("recommended_treatment", {}).get("dosage_calculation", {}).get("total_amount_needed"),
                    recommendations.get("recommended_treatment", {}).get("dosage_calculation", {}).get("cost_estimate"),
                    datetime.now().isoformat()
                ))
                conn.commit()
                logger.info("Scan data saved to database.")
        except Exception as db_e:
            logger.error(f"Failed to save scan data to database: {db_e}")

        response = {
            "analysis": {
                **detection_result,
                "crop_type": crop_type,
                "image_size": f"{image.width}x{image.height}",
                "analysis_timestamp": datetime.now().isoformat()
            },
            "recommendations": recommendations,
            "metadata": {
                "location": location,
                "farm_size_hectares": farm_size,
                "weather_conditions": weather_conditions,
                "processing_time": "< 1 second"
            }
        }
        
        logger.info(f"Analysis completed: {crop_type} - {detection_result['disease']}")
        return response
        
    except Exception as e:
        logger.error(f"Analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/scan-history")
async def get_scan_history():
    """Retrieves all historical scans from the database."""
    try:
        with sqlite3.connect(DATABASE_NAME) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM scans ORDER BY scan_timestamp DESC")
            scans = cursor.fetchall()
            return [dict(scan) for scan in scans]
    except Exception as e:
        logger.error(f"Failed to retrieve scan history: {e}")
        raise HTTPException(status_code=500, detail="Could not retrieve scan history.")

def generate_pesticide_recommendations(
    detection_result: Dict, 
    crop_type: str, 
    farm_size: float, 
    weather_conditions: Optional[str]
) -> Dict:
    """Generate comprehensive pesticide recommendations"""
    
    disease = detection_result["disease"]
    severity = detection_result["severity"]
    confidence = detection_result["confidence"]
    
    if disease == "healthy" or confidence < 0.3:
        return {
            "status": "No treatment required",
            "message": "Crop appears healthy. Continue regular monitoring.",
            "preventive_measures": [
                "Maintain proper plant spacing",
                "Ensure adequate drainage",
                "Regular field sanitation",
                "Monitor weather conditions"
            ],
            "next_inspection": "7 days"
        }
    
    disease_info = DISEASE_DATABASE[crop_type].get(disease)
    if not disease_info:
        return {"error": "Disease information not available"}
    
    base_dosage = float(disease_info["dosage_per_hectare"].split()[0])
    severity_multiplier = disease_info["severity_multiplier"][severity]
    total_dosage = base_dosage * severity_multiplier * farm_size
    
    weather_adjustment = 1.0
    weather_warnings = []
    
    if weather_conditions:
        if "rain" in weather_conditions.lower():
            weather_adjustment = 1.2
            weather_warnings.append("Increase dosage due to expected rainfall")
        elif "dry" in weather_conditions.lower():
            weather_adjustment = 0.9
            weather_warnings.append("Reduced dosage due to dry conditions")
    
    final_dosage = total_dosage * weather_adjustment
    
    return {
        "disease_detected": disease_info["name"],
        "confidence_level": f"{confidence * 100:.1f}%",
        "severity_assessment": severity.upper(),
        "recommended_treatment": {
            "primary_pesticides": disease_info["pesticides"],
            "dosage_calculation": {
                "base_rate": disease_info["dosage_per_hectare"],
                "severity_factor": severity_multiplier,
                "weather_adjustment": weather_adjustment,
                "total_amount_needed": f"{final_dosage:.2f} kg",
                "cost_estimate": f"₹{final_dosage * 120:.2f}"
            },
            "application_schedule": {
                "frequency": disease_info["application_frequency"],
                "best_time": "Early morning (6-8 AM) or evening (5-7 PM)",
                "weather_requirements": "No rain expected for 4-6 hours"
            }
        },
        "application_instructions": [
            "Wear complete protective equipment (PPE)",
            "Ensure uniform coverage of affected areas",
            "Use appropriate nozzle for fine spray",
            "Maintain recommended water volume (400-500L/hectare)",
            "Avoid drift to non-target areas"
        ],
        "safety_precautions": [
            "Keep children and animals away during application",
            "Do not contaminate water sources",
            "Store unused pesticide in original container",
            "Dispose of empty containers properly",
            "Follow pre-harvest interval guidelines"
        ],
        "monitoring_plan": [
            "Check treated areas after 3-4 days",
            "Look for improvement in symptoms",
            "Reapply if necessary after 7-10 days",
            "Document treatment effectiveness"
        ],
        "weather_considerations": weather_warnings
    }

@app.get("/api/diseases/{crop_type}")
async def get_crop_diseases(crop_type: str):
    """Get detailed disease information for specific crop"""
    if crop_type not in DISEASE_DATABASE:
        raise HTTPException(status_code=404, detail="Crop type not supported")
    
    diseases = DISEASE_DATABASE[crop_type]
    return {
        "crop_type": crop_type,
        "disease_count": len(diseases),
        "diseases": [
            {
                "id": disease_id,
                "name": info["name"],
                "symptoms": info["symptoms"],
                "common_pesticides": info["pesticides"][:2]
            }
            for disease_id, info in diseases.items()
        ]
    }

@app.get("/api/crops")
async def get_supported_crops():
    """Get comprehensive crop information"""
    crop_info = {}
    for crop, diseases in DISEASE_DATABASE.items():
        crop_info[crop] = {
            "disease_count": len(diseases),
            "common_diseases": list(diseases.keys())[:3]
        }
    
    return {
        "supported_crops": crop_info,
        "platform_stats": {
            "total_crops": len(DISEASE_DATABASE),
            "total_diseases": sum(len(d) for d in DISEASE_DATABASE.values()),
            "total_pesticides": len(set(
                p for diseases in DISEASE_DATABASE.values() 
                for disease in diseases.values() 
                for p in disease["pesticides"]
            ))
        }
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )