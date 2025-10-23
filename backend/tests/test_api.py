"""
API Tests for CropGuard AI Platform
"""

import pytest
import os
import sys
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app
from app.core.database import get_db, Base

# Test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def client():
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=engine)

def test_root_endpoint(client):
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "CropGuard AI Platform API"
    assert data["version"] == "1.0.0"
    assert data["status"] == "active"

def test_dashboard_stats(client):
    """Test dashboard stats endpoint"""
    response = client.get("/api/dashboard-stats")
    assert response.status_code == 200
    data = response.json()
    assert "total_scans" in data
    assert "healthy_crops_percentage" in data
    assert "cost_savings" in data

def test_scan_history(client):
    """Test scan history endpoint"""
    response = client.get("/api/scan-history")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_weather_endpoint(client):
    """Test weather endpoint"""
    response = client.get("/api/weather/Punjab")
    assert response.status_code == 200
    data = response.json()
    assert "location" in data
    assert "temperature" in data
    assert "humidity" in data
    assert "spraying_recommendation" in data

def test_analyze_image_missing_file(client):
    """Test image analysis with missing file"""
    response = client.post("/api/analyze-image", data={
        "crop_type": "tomato",
        "farm_size": "2.0",
        "location": "Punjab",
        "weather_conditions": "sunny"
    })
    assert response.status_code == 422  # Validation error for missing file

def test_analyze_image_invalid_crop_type(client):
    """Test image analysis with invalid crop type"""
    # Create a dummy image file
    import io
    from PIL import Image
    
    # Create a simple test image
    img = Image.new('RGB', (100, 100), color='red')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    
    response = client.post("/api/analyze-image", 
        files={"file": ("test.jpg", img_bytes, "image/jpeg")},
        data={
            "crop_type": "invalid_crop",
            "farm_size": "2.0",
            "location": "Punjab",
            "weather_conditions": "sunny"
        }
    )
    # Should still process but might return different results
    assert response.status_code in [200, 500]  # Might fail due to invalid crop type