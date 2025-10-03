"""
API Routes for CropGuard AI Platform
"""

from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
from typing import List
import base64
import io
from datetime import datetime
from PIL import Image

from ..models.ai_engine import detect_disease_from_image
from ..models.disease_db import get_disease_info, DISEASE_DATABASE
from .utils import (
    generate_treatment_recommendations,
    generate_mock_weather_data,
    generate_mock_scan_history
)

router = APIRouter()

@router.post("/analyze-crop")
async def analyze_crop(
    crop_type: str = Form(...),
    area_hectares: float = Form(default=1.0),
    files: List[UploadFile] = File(...)
):
    """
    Analyze crop images and provide disease detection with pesticide recommendations
    
    Args:
        crop_type: Type of crop (tomato, brinjal, capsicum)
        area_hectares: Farm area in hectares
        files: List of uploaded image files
    
    Returns:
        Analysis results with disease detection and pesticide recommendations
    """
    try:
        if not files:
            raise HTTPException(status_code=400, detail="No images provided")
        
        # Validate crop type
        if crop_type.lower() not in DISEASE_DATABASE:
            raise HTTPException(
                status_code=400, 
                detail=f"Unsupported crop type. Supported crops: {list(DISEASE_DATABASE.keys())}"
            )
        
        # Validate area
        if area_hectares <= 0:
            raise HTTPException(status_code=400, detail="Area must be greater than 0")
        
        results = []
        
        for file in files:
            # Validate file type
            if not file.content_type.startswith('image/'):
                raise HTTPException(
                    status_code=400, 
                    detail=f"File {file.filename} is not an image"
                )
            
            # Read and process image
            image_data = await file.read()
            
            # Validate file size (10MB limit)
            if len(image_data) > 10 * 1024 * 1024:
                raise HTTPException(
                    status_code=400,
                    detail=f"File {file.filename} is too large (max 10MB)"
                )
            
            try:
                # Convert image to base64 for frontend display
                image = Image.open(io.BytesIO(image_data))
                # Resize for display if too large
                if image.width > 800 or image.height > 600:
                    image.thumbnail((800, 600), Image.Resampling.LANCZOS)
                
                buffered = io.BytesIO()
                image.save(buffered, format="JPEG", quality=85)
                img_base64 = base64.b64encode(buffered.getvalue()).decode()
                
            except Exception as e:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid image file {file.filename}: {str(e)}"
                )
            
            # Detect disease using AI engine
            try:
                detection_result = detect_disease_from_image(image_data, crop_type)
            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"AI analysis failed for {file.filename}: {str(e)}"
                )
            
            # Process results
            if detection_result and detection_result["disease"] != "healthy":
                disease_key = detection_result["disease"]
                severity = detection_result["severity"]
                
                # Get disease information
                disease_info = get_disease_info(crop_type, disease_key)
                if not disease_info:
                    raise HTTPException(
                        status_code=500,
                        detail=f"Disease information not found for {disease_key}"
                    )
                
                # Generate treatment recommendations
                pesticide_recommendations = generate_treatment_recommendations(
                    crop_type, disease_key, severity, area_hectares
                )
                
                results.append({
                    "filename": file.filename,
                    "image_base64": img_base64,
                    "detection": {
                        "disease_name": disease_info["name"],
                        "description": disease_info["description"],
                        "symptoms": disease_info.get("symptoms", []),
                        "confidence": detection_result["confidence"],
                        "severity": severity,
                        "affected_area_percentage": detection_result["affected_area_percentage"],
                        "health_score": detection_result.get("health_score", 0)
                    },
                    "pesticide_recommendations": pesticide_recommendations,
                    "timestamp": datetime.now().isoformat()
                })
            else:
                # Healthy crop
                results.append({
                    "filename": file.filename,
                    "image_base64": img_base64,
                    "detection": {
                        "disease_name": "Healthy",
                        "description": "No disease detected - crop appears healthy",
                        "symptoms": [],
                        "confidence": detection_result.get("confidence", 0.95),
                        "severity": "none",
                        "affected_area_percentage": 0,
                        "health_score": detection_result.get("health_score", 0.9)
                    },
                    "pesticide_recommendations": [],
                    "timestamp": datetime.now().isoformat()
                })
        
        # Calculate summary statistics
        total_diseased = len([r for r in results if r["detection"]["disease_name"] != "Healthy"])
        total_healthy = len(results) - total_diseased
        avg_confidence = sum(r["detection"]["confidence"] for r in results) / len(results)
        
        return JSONResponse(content={
            "status": "success",
            "crop_type": crop_type.title(),
            "area_hectares": area_hectares,
            "total_images": len(files),
            "summary": {
                "healthy_count": total_healthy,
                "diseased_count": total_diseased,
                "average_confidence": round(avg_confidence, 3),
                "health_percentage": round((total_healthy / len(results)) * 100, 1)
            },
            "results": results,
            "analysis_timestamp": datetime.now().isoformat()
        })
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@router.get("/weather")
async def get_weather():
    """
    Get current weather conditions and spraying recommendations
    
    Returns:
        Weather data with spraying suitability assessment
    """
    try:
        weather_data = generate_mock_weather_data()
        return JSONResponse(content=weather_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Weather data unavailable: {str(e)}")

@router.get("/scan-history")
async def get_scan_history():
    """
    Get scan history and dashboard statistics
    
    Returns:
        Historical scan data and analytics
    """
    try:
        history_data = generate_mock_scan_history()
        return JSONResponse(content=history_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"History data unavailable: {str(e)}")

@router.get("/crops")
async def get_supported_crops():
    """
    Get list of supported crops and their diseases
    
    Returns:
        Dictionary of supported crops and associated diseases
    """
    try:
        crops_info = {}
        for crop, diseases in DISEASE_DATABASE.items():
            crops_info[crop] = {
                "name": crop.title(),
                "diseases": [
                    {
                        "key": disease_key,
                        "name": disease_info["name"],
                        "description": disease_info["description"]
                    }
                    for disease_key, disease_info in diseases.items()
                ]
            }
        
        return JSONResponse(content={
            "supported_crops": crops_info,
            "total_crops": len(crops_info),
            "total_diseases": sum(len(diseases) for diseases in DISEASE_DATABASE.values())
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Crops data unavailable: {str(e)}")

@router.get("/health")
async def health_check():
    """
    Health check endpoint
    
    Returns:
        System health status
    """
    return JSONResponse(content={
        "status": "healthy",
        "service": "CropGuard AI",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    })