"""
Database initialization script for CropGuard AI Platform
"""

import os
import sys
import json
from datetime import datetime

# Add the parent directory to the path to import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import engine, Base
from app.core.models import (
    CropScan, DiseaseInfo, PesticideData, 
    TreatmentHistory, WeatherLog, UserProfile
)
from sqlalchemy.orm import sessionmaker

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_database():
    """
    Initialize the database with tables and seed data
    """
    print("Initializing CropGuard AI Database...")
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("✓ Database tables created")
    
    # Seed initial data
    seed_disease_info()
    seed_pesticide_data()
    seed_sample_user()
    
    print("✓ Database initialization completed successfully!")

def seed_disease_info():
    """
    Seed the database with disease information
    """
    db = SessionLocal()
    
    try:
        # Check if data already exists
        if db.query(DiseaseInfo).first():
            print("✓ Disease info already exists, skipping...")
            return
        
        diseases = [
            {
                'disease_name': 'Bacterial Spot',
                'crop_types': json.dumps(['tomato', 'capsicum']),
                'symptoms': json.dumps([
                    'Dark spots on leaves with yellow halos',
                    'Raised lesions on fruits',
                    'Leaf yellowing and drop'
                ]),
                'causes': json.dumps([
                    'Xanthomonas bacteria',
                    'High humidity conditions',
                    'Water splash from irrigation',
                    'Contaminated seeds or tools'
                ]),
                'prevention_methods': json.dumps([
                    'Use disease-free seeds',
                    'Avoid overhead irrigation',
                    'Maintain proper plant spacing',
                    'Remove infected plant debris',
                    'Sanitize tools between plants'
                ]),
                'treatment_options': json.dumps([
                    'Copper-based fungicides',
                    'Streptomycin applications',
                    'Mancozeb treatments',
                    'Removal of infected parts'
                ]),
                'severity_indicators': json.dumps({
                    'mild': 'Few scattered spots on lower leaves',
                    'moderate': 'Multiple spots covering 10-30% of leaf area',
                    'severe': 'Extensive spotting covering >30% of leaf area with fruit infection'
                })
            },
            {
                'disease_name': 'Early Blight',
                'crop_types': json.dumps(['tomato']),
                'symptoms': json.dumps([
                    'Concentric rings on leaves (target spots)',
                    'Brown to black lesions',
                    'Yellowing and defoliation',
                    'Stem cankers'
                ]),
                'causes': json.dumps([
                    'Alternaria solani fungus',
                    'High temperature and humidity',
                    'Plant stress conditions',
                    'Poor air circulation'
                ]),
                'prevention_methods': json.dumps([
                    'Crop rotation with non-solanaceous crops',
                    'Remove lower leaves touching soil',
                    'Improve air circulation',
                    'Avoid water stress',
                    'Use resistant varieties'
                ]),
                'treatment_options': json.dumps([
                    'Mancozeb fungicide',
                    'Chlorothalonil applications',
                    'Copper hydroxide treatments',
                    'Metalaxyl for severe cases'
                ]),
                'severity_indicators': json.dumps({
                    'mild': 'Few lesions on lower leaves only',
                    'moderate': 'Lesions spreading to middle leaves',
                    'severe': 'Extensive defoliation and stem infection'
                })
            },
            {
                'disease_name': 'Late Blight',
                'crop_types': json.dumps(['tomato']),
                'symptoms': json.dumps([
                    'Water-soaked lesions on leaves',
                    'White fuzzy growth on leaf undersides',
                    'Brown to black lesions',
                    'Rapid plant collapse'
                ]),
                'causes': json.dumps([
                    'Phytophthora infestans',
                    'Cool, wet weather conditions',
                    'High humidity (>90%)',
                    'Temperature 15-25°C'
                ]),
                'prevention_methods': json.dumps([
                    'Monitor weather conditions closely',
                    'Use resistant varieties',
                    'Ensure good drainage',
                    'Apply preventive sprays',
                    'Remove infected plants immediately'
                ]),
                'treatment_options': json.dumps([
                    'Metalaxyl + Mancozeb combination',
                    'Cymoxanil applications',
                    'Copper hydroxide',
                    'Fosetyl-Al treatments'
                ]),
                'severity_indicators': json.dumps({
                    'mild': 'Small water-soaked spots',
                    'moderate': 'Lesions expanding rapidly with some white growth',
                    'severe': 'Plant collapse and extensive fruit rot'
                })
            },
            {
                'disease_name': 'Bacterial Wilt',
                'crop_types': json.dumps(['brinjal']),
                'symptoms': json.dumps([
                    'Sudden wilting of plants',
                    'Brown vascular discoloration',
                    'Yellowing of leaves',
                    'Plant death'
                ]),
                'causes': json.dumps([
                    'Ralstonia solanacearum bacteria',
                    'Soil-borne pathogen',
                    'High soil temperature and moisture',
                    'Contaminated irrigation water'
                ]),
                'prevention_methods': json.dumps([
                    'Use resistant varieties',
                    'Soil solarization',
                    'Crop rotation for 3-4 years',
                    'Avoid waterlogging',
                    'Use clean irrigation water'
                ]),
                'treatment_options': json.dumps([
                    'Streptomycin soil drench',
                    'Copper hydroxide applications',
                    'Bleaching powder soil treatment',
                    'Remove and destroy infected plants'
                ]),
                'severity_indicators': json.dumps({
                    'mild': 'Few plants showing wilting symptoms',
                    'moderate': 'Plants wilting during day, recovering at night',
                    'severe': 'Complete plant collapse and death'
                })
            },
            {
                'disease_name': 'Powdery Mildew',
                'crop_types': json.dumps(['capsicum']),
                'symptoms': json.dumps([
                    'White powdery coating on leaves',
                    'Leaf distortion and curling',
                    'Yellowing of affected areas',
                    'Stunted growth'
                ]),
                'causes': json.dumps([
                    'Erysiphe cichoracearum fungus',
                    'High humidity with dry conditions',
                    'Poor air circulation',
                    'Excessive nitrogen fertilization'
                ]),
                'prevention_methods': json.dumps([
                    'Ensure good air circulation',
                    'Avoid excessive nitrogen',
                    'Monitor humidity levels',
                    'Use resistant varieties',
                    'Regular field inspection'
                ]),
                'treatment_options': json.dumps([
                    'Sulfur-based fungicides',
                    'Propiconazole applications',
                    'Carbendazim treatments',
                    'Triadimefon for severe cases'
                ]),
                'severity_indicators': json.dumps({
                    'mild': 'Light powdery patches on few leaves',
                    'moderate': 'Moderate leaf coverage with some distortion',
                    'severe': 'Extensive coverage causing defoliation'
                })
            }
        ]
        
        for disease_data in diseases:
            disease = DiseaseInfo(**disease_data)
            db.add(disease)
        
        db.commit()
        print(f"✓ Seeded {len(diseases)} disease records")
        
    except Exception as e:
        print(f"Error seeding disease info: {e}")
        db.rollback()
    finally:
        db.close()

def seed_pesticide_data():
    """
    Seed the database with pesticide information
    """
    db = SessionLocal()
    
    try:
        # Check if data already exists
        if db.query(PesticideData).first():
            print("✓ Pesticide data already exists, skipping...")
            return
        
        pesticides = [
            {
                'pesticide_name': 'Copper Hydroxide',
                'active_ingredient': 'Copper Hydroxide 77% WP',
                'target_diseases': json.dumps(['Bacterial Spot', 'Early Blight', 'Late Blight', 'Bacterial Wilt']),
                'target_crops': json.dumps(['tomato', 'brinjal', 'capsicum']),
                'dosage_per_hectare': 2.5,
                'price_per_liter': 450.0,
                'application_method': 'Foliar spray',
                'safety_period': 7,
                'environmental_impact': 'Medium'
            },
            {
                'pesticide_name': 'Mancozeb',
                'active_ingredient': 'Mancozeb 75% WP',
                'target_diseases': json.dumps(['Early Blight', 'Late Blight', 'Cercospora Leaf Spot', 'Anthracnose']),
                'target_crops': json.dumps(['tomato', 'brinjal', 'capsicum']),
                'dosage_per_hectare': 2.5,
                'price_per_liter': 520.0,
                'application_method': 'Foliar spray',
                'safety_period': 14,
                'environmental_impact': 'Medium'
            },
            {
                'pesticide_name': 'Streptomycin',
                'active_ingredient': 'Streptomycin Sulphate 90% + Tetracycline HCl 10%',
                'target_diseases': json.dumps(['Bacterial Spot', 'Bacterial Wilt']),
                'target_crops': json.dumps(['tomato', 'brinjal', 'capsicum']),
                'dosage_per_hectare': 0.5,
                'price_per_liter': 1200.0,
                'application_method': 'Foliar spray and soil drench',
                'safety_period': 7,
                'environmental_impact': 'Low'
            },
            {
                'pesticide_name': 'Chlorothalonil',
                'active_ingredient': 'Chlorothalonil 75% WP',
                'target_diseases': json.dumps(['Early Blight', 'Late Blight', 'Leaf Mold', 'Anthracnose']),
                'target_crops': json.dumps(['tomato', 'brinjal', 'capsicum']),
                'dosage_per_hectare': 2.0,
                'price_per_liter': 680.0,
                'application_method': 'Foliar spray',
                'safety_period': 14,
                'environmental_impact': 'Medium'
            },
            {
                'pesticide_name': 'Metalaxyl',
                'active_ingredient': 'Metalaxyl 8% + Mancozeb 64% WP',
                'target_diseases': json.dumps(['Late Blight', 'Downy Mildew']),
                'target_crops': json.dumps(['tomato', 'brinjal', 'capsicum']),
                'dosage_per_hectare': 2.0,
                'price_per_liter': 850.0,
                'application_method': 'Foliar spray',
                'safety_period': 21,
                'environmental_impact': 'Medium'
            },
            {
                'pesticide_name': 'Propiconazole',
                'active_ingredient': 'Propiconazole 25% EC',
                'target_diseases': json.dumps(['Powdery Mildew', 'Leaf Mold']),
                'target_crops': json.dumps(['tomato', 'capsicum']),
                'dosage_per_hectare': 0.5,
                'price_per_liter': 1500.0,
                'application_method': 'Foliar spray',
                'safety_period': 14,
                'environmental_impact': 'Low'
            },
            {
                'pesticide_name': 'Sulfur',
                'active_ingredient': 'Wettable Sulfur 80% WP',
                'target_diseases': json.dumps(['Powdery Mildew']),
                'target_crops': json.dumps(['tomato', 'brinjal', 'capsicum']),
                'dosage_per_hectare': 3.0,
                'price_per_liter': 200.0,
                'application_method': 'Foliar spray',
                'safety_period': 7,
                'environmental_impact': 'Low'
            },
            {
                'pesticide_name': 'Carbendazim',
                'active_ingredient': 'Carbendazim 50% WP',
                'target_diseases': json.dumps(['Powdery Mildew', 'Anthracnose', 'Cercospora Leaf Spot']),
                'target_crops': json.dumps(['tomato', 'brinjal', 'capsicum']),
                'dosage_per_hectare': 1.0,
                'price_per_liter': 850.0,
                'application_method': 'Foliar spray',
                'safety_period': 14,
                'environmental_impact': 'Medium'
            }
        ]
        
        for pesticide_data in pesticides:
            pesticide = PesticideData(**pesticide_data)
            db.add(pesticide)
        
        db.commit()
        print(f"✓ Seeded {len(pesticides)} pesticide records")
        
    except Exception as e:
        print(f"Error seeding pesticide data: {e}")
        db.rollback()
    finally:
        db.close()

def seed_sample_user():
    """
    Create a sample user profile
    """
    db = SessionLocal()
    
    try:
        # Check if user already exists
        if db.query(UserProfile).first():
            print("✓ Sample user already exists, skipping...")
            return
        
        sample_user = UserProfile(
            username='farmer_john',
            email='john@farmeremail.com',
            full_name='John Singh',
            phone_number='+91-9876543210',
            farm_location='Punjab, India',
            total_farm_area=5.5,
            primary_crops=json.dumps(['tomato', 'brinjal', 'capsicum']),
            registration_date=datetime.now(),
            is_active=True
        )
        
        db.add(sample_user)
        db.commit()
        print("✓ Created sample user profile")
        
    except Exception as e:
        print(f"Error creating sample user: {e}")
        db.rollback()
    finally:
        db.close()

def create_sample_data():
    """
    Create some sample scan and treatment data for demonstration
    """
    db = SessionLocal()
    
    try:
        # Sample crop scans
        sample_scans = [
            CropScan(
                crop_type='tomato',
                disease_detected='Early Blight',
                confidence_score=0.87,
                severity_level='moderate',
                farm_size=2.0,
                location='Punjab, India',
                image_path='/uploads/sample_tomato_1.jpg',
                scan_timestamp=datetime.now(),
                treatment_cost=1200.0,
                weather_conditions='Humid, 28°C'
            ),
            CropScan(
                crop_type='brinjal',
                disease_detected='Healthy',
                confidence_score=0.94,
                severity_level='healthy',
                farm_size=1.5,
                location='Punjab, India',
                image_path='/uploads/sample_brinjal_1.jpg',
                scan_timestamp=datetime.now(),
                treatment_cost=0.0,
                weather_conditions='Sunny, 25°C'
            ),
            CropScan(
                crop_type='capsicum',
                disease_detected='Bacterial Spot',
                confidence_score=0.82,
                severity_level='mild',
                farm_size=1.0,
                location='Punjab, India',
                image_path='/uploads/sample_capsicum_1.jpg',
                scan_timestamp=datetime.now(),
                treatment_cost=800.0,
                weather_conditions='Cloudy, 26°C'
            )
        ]
        
        for scan in sample_scans:
            db.add(scan)
        
        db.commit()
        print(f"✓ Created {len(sample_scans)} sample scan records")
        
    except Exception as e:
        print(f"Error creating sample data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_database()
    
    # Optionally create sample data
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == '--with-samples':
        create_sample_data()