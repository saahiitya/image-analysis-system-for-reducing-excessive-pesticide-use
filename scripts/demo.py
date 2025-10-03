#!/usr/bin/env python3
"""
Demo script for CropGuard AI Platform
Tests the API endpoints and demonstrates functionality
"""

import requests
import json
import time
import sys
from PIL import Image, ImageDraw
import io
import base64

class CropGuardDemo:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api/v1"
        
    def create_sample_image(self, crop_type, disease_type="healthy"):
        """Create a sample crop image for testing"""
        # Create a simple test image
        img = Image.new('RGB', (400, 300), color='lightgreen')
        draw = ImageDraw.Draw(img)
        
        # Add crop-like features
        draw.rectangle([50, 50, 350, 250], fill='green', outline='darkgreen', width=3)
        
        # Add title
        draw.text((100, 80), f"{crop_type.upper()}", fill='black', font=None)
        draw.text((100, 100), f"Status: {disease_type}", 
                 fill='red' if disease_type != "healthy" else 'darkgreen')
        
        # Add some disease spots for non-healthy images
        if disease_type != "healthy":
            for i in range(8):
                x, y = 80 + i * 30, 140 + (i % 3) * 20
                draw.ellipse([x, y, x+15, y+15], fill='brown')
                draw.ellipse([x+20, y+10, x+35, y+25], fill='darkred')
        
        # Add some leaf-like shapes
        for i in range(5):
            x, y = 120 + i * 40, 180
            draw.ellipse([x, y, x+25, y+40], fill='forestgreen', outline='darkgreen')
        
        # Convert to bytes
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='JPEG', quality=85)
        img_bytes.seek(0)
        
        return img_bytes.getvalue()
    
    def test_health_check(self):
        """Test health check endpoint"""
        print("🔍 Testing Health Check...")
        try:
            response = requests.get(f"{self.api_url}/health", timeout=10)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Health Check: {data['status']}")
                print(f"   Service: {data['service']}")
                print(f"   Version: {data.get('version', 'Unknown')}")
                return True
            else:
                print(f"❌ Health check failed: HTTP {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Health check error: {e}")
            return False
    
    def test_weather_api(self):
        """Test weather API endpoint"""
        print("\n🌤️ Testing Weather API...")
        try:
            response = requests.get(f"{self.api_url}/weather", timeout=10)
            if response.status_code == 200:
                weather_data = response.json()
                print(f"✅ Weather API working!")
                print(f"   Temperature: {weather_data['temperature']}°C")
                print(f"   Condition: {weather_data['condition']}")
                print(f"   Humidity: {weather_data['humidity']}%")
                print(f"   Wind Speed: {weather_data['wind_speed']} km/h")
                print(f"   Spray Suitable: {weather_data['spray_recommendation']['suitable']}")
                return True
            else:
                print(f"❌ Weather API failed: HTTP {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Weather API error: {e}")
            return False
    
    def test_scan_history_api(self):
        """Test scan history API endpoint"""
        print("\n📊 Testing Scan History API...")
        try:
            response = requests.get(f"{self.api_url}/scan-history", timeout=10)
            if response.status_code == 200:
                history_data = response.json()
                print(f"✅ Scan History API working!")
                print(f"   Total Scans: {history_data['total_scans']}")
                print(f"   Healthy Percentage: {history_data['healthy_percentage']}%")
                print(f"   Active Treatments: {history_data['active_treatments']}")
                print(f"   Cost Savings: ₹{history_data['cost_savings']}")
                return True
            else:
                print(f"❌ Scan History API failed: HTTP {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Scan History API error: {e}")
            return False
    
    def test_crops_api(self):
        """Test supported crops API endpoint"""
        print("\n🌾 Testing Crops API...")
        try:
            response = requests.get(f"{self.api_url}/crops", timeout=10)
            if response.status_code == 200:
                crops_data = response.json()
                print(f"✅ Crops API working!")
                print(f"   Total Crops: {crops_data['total_crops']}")
                print(f"   Total Diseases: {crops_data['total_diseases']}")
                
                for crop_name, crop_info in crops_data['supported_crops'].items():
                    print(f"   📱 {crop_info['name']}: {len(crop_info['diseases'])} diseases")
                
                return True
            else:
                print(f"❌ Crops API failed: HTTP {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Crops API error: {e}")
            return False
    
    def test_crop_analysis_api(self):
        """Test crop analysis API endpoint"""
        print("\n🤖 Testing Crop Analysis API...")
        
        # Test different crops and scenarios
        test_cases = [
            {
                "crop": "tomato", 
                "area": 1.5, 
                "disease": "early_blight",
                "description": "Tomato with early blight symptoms"
            },
            {
                "crop": "brinjal", 
                "area": 2.0, 
                "disease": "healthy",
                "description": "Healthy brinjal sample"
            },
            {
                "crop": "capsicum", 
                "area": 0.8, 
                "disease": "thrips",
                "description": "Capsicum with thrips damage"
            }
        ]
        
        success_count = 0
        
        for i, test_case in enumerate(test_cases):
            print(f"\n   Test Case {i+1}: {test_case['description']}")
            
            # Create sample image
            img_data = self.create_sample_image(test_case['crop'], test_case['disease'])
            
            # Prepare form data
            files = {'files': (f'test_{test_case["crop"]}.jpg', img_data, 'image/jpeg')}
            data = {
                'crop_type': test_case['crop'],
                'area_hectares': test_case['area']
            }
            
            try:
                response = requests.post(
                    f"{self.api_url}/analyze-crop", 
                    files=files, 
                    data=data,
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    print(f"   ✅ Analysis successful!")
                    print(f"   Crop: {result['crop_type']}")
                    print(f"   Area: {result['area_hectares']} hectares")
                    print(f"   Images: {result['total_images']}")
                    print(f"   Health: {result['summary']['health_percentage']}%")
                    
                    # Show first result details
                    if result['results']:
                        first_result = result['results'][0]
                        detection = first_result['detection']
                        print(f"   Disease: {detection['disease_name']}")
                        print(f"   Confidence: {detection['confidence']*100:.1f}%")
                        
                        if first_result['pesticide_recommendations']:
                            pesticide = first_result['pesticide_recommendations'][0]
                            print(f"   Recommended: {pesticide['name']}")
                            print(f"   Cost: ₹{pesticide['total_cost']}")
                    
                    success_count += 1
                    
                else:
                    print(f"   ❌ Analysis failed: HTTP {response.status_code}")
                    try:
                        error_data = response.json()
                        print(f"   Error: {error_data.get('detail', 'Unknown error')}")
                    except:
                        print(f"   Error: {response.text[:100]}...")
                        
            except Exception as e:
                print(f"   ❌ Analysis error: {e}")
            
            # Small delay between requests
            time.sleep(1)
        
        print(f"\n📈 Analysis API Results: {success_count}/{len(test_cases)} successful")
        return success_count == len(test_cases)
    
    def test_frontend_access(self):
        """Test frontend accessibility"""
        print("\n🌐 Testing Frontend Access...")
        try:
            response = requests.get(self.base_url, timeout=10)
            if response.status_code == 200:
                content = response.text
                if "CropGuard AI" in content and "Dashboard" in content:
                    print("✅ Frontend accessible and contains expected content")
                    return True
                else:
                    print("⚠️ Frontend accessible but content may be incomplete")
                    return False
            else:
                print(f"❌ Frontend not accessible: HTTP {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Frontend access error: {e}")
            return False
    
    def run_full_demo(self):
        """Run complete demo test suite"""
        print("🌱 CropGuard AI Platform Demo")
        print("=" * 60)
        print("This demo tests all API endpoints and functionality")
        print("Make sure the server is running on", self.base_url)
        print("=" * 60)
        
        results = []
        
        # Test all endpoints
        results.append(("Health Check", self.test_health_check()))
        results.append(("Frontend Access", self.test_frontend_access()))
        results.append(("Weather API", self.test_weather_api()))
        results.append(("Scan History API", self.test_scan_history_api()))
        results.append(("Crops API", self.test_crops_api()))
        results.append(("Crop Analysis API", self.test_crop_analysis_api()))
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 Demo Results Summary:")
        print("=" * 60)
        
        passed = 0
        total = len(results)
        
        for test_name, success in results:
            status = "✅ PASS" if success else "❌ FAIL"
            print(f"{test_name:<20} {status}")
            if success:
                passed += 1
        
        print("=" * 60)
        print(f"Overall: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
        
        if passed == total:
            print("🎉 All tests passed! CropGuard AI is working perfectly!")
            print("\n🚀 You can now use the web interface at:")
            print(f"   {self.base_url}")
            print("\n📖 API documentation available at:")
            print(f"   {self.base_url}/docs")
        else:
            print("⚠️ Some tests failed. Please check the server logs.")
            print("Make sure all dependencies are installed and the server is running.")
        
        print("=" * 60)
        
        return passed == total

def main():
    """Main demo function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='CropGuard AI Demo Script')
    parser.add_argument('--url', default='http://localhost:8000', 
                       help='Base URL of the CropGuard AI server')
    parser.add_argument('--test', choices=['health', 'weather', 'history', 'crops', 'analysis', 'frontend'],
                       help='Run specific test only')
    
    args = parser.parse_args()
    
    demo = CropGuardDemo(args.url)
    
    if args.test:
        # Run specific test
        test_methods = {
            'health': demo.test_health_check,
            'weather': demo.test_weather_api,
            'history': demo.test_scan_history_api,
            'crops': demo.test_crops_api,
            'analysis': demo.test_crop_analysis_api,
            'frontend': demo.test_frontend_access
        }
        
        if args.test in test_methods:
            success = test_methods[args.test]()
            sys.exit(0 if success else 1)
    else:
        # Run full demo
        success = demo.run_full_demo()
        sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()