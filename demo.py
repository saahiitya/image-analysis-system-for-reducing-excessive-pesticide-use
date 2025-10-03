#!/usr/bin/env python3
"""
Demo script for CropGuard AI Platform
Tests the API endpoints and demonstrates functionality
"""

import requests
import json
from PIL import Image, ImageDraw
import io
import base64

def create_sample_image(crop_type, disease_type="healthy"):
    """Create a sample crop image for testing"""
    # Create a simple test image
    img = Image.new('RGB', (400, 300), color='green')
    draw = ImageDraw.Draw(img)
    
    # Add some crop-like features
    draw.rectangle([50, 50, 350, 250], fill='lightgreen', outline='darkgreen', width=2)
    draw.text((100, 100), f"{crop_type.upper()}", fill='black')
    draw.text((100, 130), f"Disease: {disease_type}", fill='red' if disease_type != "healthy" else 'green')
    
    # Add some spots for diseased images
    if disease_type != "healthy":
        for i in range(5):
            x, y = 100 + i * 40, 160 + i * 10
            draw.ellipse([x, y, x+20, y+20], fill='brown')
    
    # Convert to bytes
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    
    return img_bytes.getvalue()

def test_weather_api():
    """Test weather API endpoint"""
    print("🌤️ Testing Weather API...")
    try:
        response = requests.get("http://localhost:8000/weather")
        if response.status_code == 200:
            weather_data = response.json()
            print(f"✅ Weather API working!")
            print(f"   Temperature: {weather_data['temperature']}°C")
            print(f"   Condition: {weather_data['condition']}")
            print(f"   Spray Suitable: {weather_data['spray_recommendation']['suitable']}")
        else:
            print(f"❌ Weather API failed with status {response.status_code}")
    except Exception as e:
        print(f"❌ Weather API error: {e}")

def test_scan_history_api():
    """Test scan history API endpoint"""
    print("\n📊 Testing Scan History API...")
    try:
        response = requests.get("http://localhost:8000/scan-history")
        if response.status_code == 200:
            history_data = response.json()
            print(f"✅ Scan History API working!")
            print(f"   Total Scans: {history_data['total_scans']}")
            print(f"   Healthy Percentage: {history_data['healthy_percentage']}%")
            print(f"   Cost Savings: ₹{history_data['cost_savings']}")
        else:
            print(f"❌ Scan History API failed with status {response.status_code}")
    except Exception as e:
        print(f"❌ Scan History API error: {e}")

def test_crop_analysis_api():
    """Test crop analysis API endpoint"""
    print("\n🤖 Testing Crop Analysis API...")
    
    # Test different crops and scenarios
    test_cases = [
        {"crop": "tomato", "area": 1.5, "description": "Tomato with potential disease"},
        {"crop": "brinjal", "area": 2.0, "description": "Brinjal healthy sample"},
        {"crop": "capsicum", "area": 0.8, "description": "Capsicum with pest damage"}
    ]
    
    for i, test_case in enumerate(test_cases):
        print(f"\n   Test Case {i+1}: {test_case['description']}")
        
        # Create sample image
        disease_type = "early_blight" if i == 0 else "healthy"
        img_data = create_sample_image(test_case['crop'], disease_type)
        
        # Prepare form data
        files = {'files': ('test_image.jpg', img_data, 'image/jpeg')}
        data = {
            'crop_type': test_case['crop'],
            'area_hectares': test_case['area']
        }
        
        try:
            response = requests.post("http://localhost:8000/analyze-crop", files=files, data=data)
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ Analysis successful!")
                print(f"   Crop: {result['crop_type'].title()}")
                print(f"   Area: {result['area_hectares']} hectares")
                print(f"   Images processed: {result['total_images']}")
                
                for j, image_result in enumerate(result['results']):
                    detection = image_result['detection']
                    print(f"   \n   Image {j+1} Results:")
                    print(f"     Disease: {detection['disease_name']}")
                    print(f"     Confidence: {detection['confidence']*100:.1f}%")
                    
                    if image_result['pesticide_recommendations']:
                        pesticide = image_result['pesticide_recommendations'][0]
                        print(f"     Recommended: {pesticide['name']}")
                        print(f"     Cost: ₹{pesticide['total_cost']}")
                        print(f"     Amount needed: {pesticide['pesticide_amount']} {pesticide['unit']}")
            else:
                print(f"   ❌ Analysis failed with status {response.status_code}")
                print(f"   Error: {response.text}")
        except Exception as e:
            print(f"   ❌ Analysis error: {e}")

def main():
    """Run all demo tests"""
    print("🌱 CropGuard AI Platform Demo")
    print("=" * 50)
    print("This demo tests all API endpoints with sample data")
    print("Make sure the server is running on http://localhost:8000")
    print("=" * 50)
    
    # Test all endpoints
    test_weather_api()
    test_scan_history_api()
    test_crop_analysis_api()
    
    print("\n" + "=" * 50)
    print("🎉 Demo completed!")
    print("You can now test the web interface at http://localhost:8000")
    print("=" * 50)

if __name__ == "__main__":
    main()