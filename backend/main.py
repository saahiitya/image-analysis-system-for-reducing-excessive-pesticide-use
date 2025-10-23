"""
CropGuard AI - Main FastAPI Application
AI-powered crop disease detection and pesticide management platform
"""

from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import uvicorn
import os
from datetime import datetime
from typing import List, Optional

from app.core.config import settings
from app.core.database import get_db, engine, Base
from app.services.disease_detection import DiseaseDetectionService
from app.services.pesticide_recommendation import PesticideRecommendationService
from app.services.cost_calculation import CostCalculationService
from app.api.models import (
    ScanRequest, ScanResponse, HistoryResponse, 
    WeatherData, PesticideRecommendation
)

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CropGuard AI Platform",
    description="AI-powered crop disease detection and pesticide management",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files
app.mount("/static", StaticFiles(directory="data/uploads"), name="static")

# Initialize services
disease_service = DiseaseDetectionService()
pesticide_service = PesticideRecommendationService()
cost_service = CostCalculationService()

@app.get("/")
async def root():
    return {
        "message": "CropGuard AI Platform API",
        "version": "1.0.0",
        "status": "active"
    }

@app.post("/api/analyze-image", response_model=ScanResponse)
async def analyze_crop_image(
    file: UploadFile = File(...),
    crop_type: str = Form(...),
    farm_size: float = Form(...),
    location: str = Form(""),
    weather_conditions: str = Form(""),
    db: Session = Depends(get_db)
):
    """
    Analyze uploaded crop image for disease detection and pesticide recommendations
    """
    try:
        # Validate file type
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Save uploaded file
        upload_dir = "data/uploads"
        os.makedirs(upload_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{file.filename}"
        file_path = os.path.join(upload_dir, filename)
        
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Perform disease detection
        disease_result = await disease_service.detect_disease(
            image_path=file_path,
            crop_type=crop_type
        )
        
        # Get pesticide recommendations
        pesticide_recommendations = await pesticide_service.get_recommendations(
            disease=disease_result['disease'],
            crop_type=crop_type,
            severity=disease_result['severity'],
            weather_conditions=weather_conditions
        )
        
        # Calculate costs and dosage
        cost_calculation = await cost_service.calculate_treatment_cost(
            pesticides=pesticide_recommendations['primary_pesticides'],
            farm_size=farm_size,
            severity=disease_result['severity'],
            location=location
        )
        
        # Store scan in database
        from app.core.models import CropScan
        scan_record = CropScan(
            crop_type=crop_type,
            disease_detected=disease_result['disease'],
            confidence_score=disease_result['confidence'],
            severity_level=disease_result['severity'],
            farm_size=farm_size,
            location=location,
            image_path=file_path,
            scan_timestamp=datetime.now(),
            treatment_cost=cost_calculation['cost_estimate']
        )
        
        db.add(scan_record)
        db.commit()
        db.refresh(scan_record)
        
        # Prepare response
        response = ScanResponse(
            scan_id=scan_record.id,
            recommendations={
                "disease_detected": disease_result['disease'],
                "confidence_score": disease_result['confidence'],
                "severity_assessment": disease_result['severity'],
                "recommended_treatment": {
                    "primary_pesticides": pesticide_recommendations['primary_pesticides'],
                    "alternative_pesticides": pesticide_recommendations['alternative_pesticides'],
                    "application_method": pesticide_recommendations['application_method'],
                    "dosage_calculation": cost_calculation,
                    "timing_recommendations": pesticide_recommendations['timing']
                },
                "prevention_tips": pesticide_recommendations['prevention_tips'],
                "follow_up_schedule": pesticide_recommendations['follow_up_schedule']
            },
            environmental_impact={
                "pesticide_reduction": cost_calculation.get('reduction_percentage', 0),
                "water_usage": cost_calculation.get('water_needed', 0),
                "cost_savings": cost_calculation.get('savings', 0)
            }
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.get("/api/scan-history", response_model=List[HistoryResponse])
async def get_scan_history(
    limit: int = 50,
    crop_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Retrieve scan history with optional filtering
    """
    try:
        from app.core.models import CropScan
        
        query = db.query(CropScan)
        
        if crop_type:
            query = query.filter(CropScan.crop_type == crop_type)
        
        scans = query.order_by(CropScan.scan_timestamp.desc()).limit(limit).all()
        
        return [
            HistoryResponse(
                id=scan.id,
                crop_type=scan.crop_type,
                disease_detected=scan.disease_detected,
                confidence_score=scan.confidence_score,
                severity_level=scan.severity_level,
                scan_timestamp=scan.scan_timestamp,
                treatment_cost=scan.treatment_cost,
                location=scan.location
            )
            for scan in scans
        ]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch history: {str(e)}")

@app.get("/api/weather/{location}")
async def get_weather_data(location: str):
    """
    Get current weather data for spraying recommendations
    """
    try:
        # This would integrate with a weather API like OpenWeatherMap
        # For now, returning mock data
        return WeatherData(
            location=location,
            temperature=25.0,
            humidity=65,
            wind_speed=8.5,
            weather_condition="Partly Cloudy",
            uv_index=3,
            rain_probability=15,
            spraying_recommendation="Suitable for spraying",
            best_spraying_times=["06:00-10:00", "16:00-19:00"]
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Weather data unavailable: {str(e)}")

@app.get("/api/dashboard-stats")
async def get_dashboard_stats(db: Session = Depends(get_db)):
    """
    Get dashboard statistics for farmer overview
    """
    try:
        from app.core.models import CropScan
        from sqlalchemy import func
        
        total_scans = db.query(func.count(CropScan.id)).scalar()
        
        # Calculate healthy crop percentage
        healthy_scans = db.query(func.count(CropScan.id)).filter(
            CropScan.disease_detected == "Healthy"
        ).scalar()
        
        healthy_percentage = (healthy_scans / total_scans * 100) if total_scans > 0 else 0
        
        # Calculate total cost savings
        total_savings = db.query(func.sum(CropScan.treatment_cost)).scalar() or 0
        
        return {
            "total_scans": total_scans,
            "healthy_crops_percentage": round(healthy_percentage, 1),
            "active_treatments": 0,  # Would be calculated based on treatment tracking
            "pesticide_saved": f"{round(total_savings * 0.3, 1)}L",  # Estimated savings
            "cost_savings": f"₹{round(total_savings * 0.25, 2)}"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Stats unavailable: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )