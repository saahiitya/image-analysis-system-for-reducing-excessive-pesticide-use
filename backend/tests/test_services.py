"""
Service Tests for CropGuard AI Platform
"""

import pytest
import asyncio
import os
import sys
from unittest.mock import Mock, patch
import numpy as np

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.disease_detection import DiseaseDetectionService
from app.services.pesticide_recommendation import PesticideRecommendationService
from app.services.cost_calculation import CostCalculationService

class TestDiseaseDetectionService:
    """Test Disease Detection Service"""
    
    def setup_method(self):
        self.service = DiseaseDetectionService()
    
    def test_service_initialization(self):
        """Test service initializes correctly"""
        assert self.service is not None
        assert hasattr(self.service, 'disease_database')
        assert 'tomato' in self.service.disease_database
        assert 'brinjal' in self.service.disease_database
        assert 'capsicum' in self.service.disease_database
    
    def test_preprocess_image_with_mock_image(self):
        """Test image preprocessing with mock image"""
        # Create a temporary test image
        import tempfile
        from PIL import Image
        
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp:
            img = Image.new('RGB', (224, 224), color='red')
            img.save(tmp.name, 'JPEG')
            
            try:
                processed = self.service.preprocess_image(tmp.name)
                assert processed.shape == (1, 224, 224, 3)
                assert processed.dtype == np.float32
                assert processed.min() >= 0.0
                assert processed.max() <= 1.0
            finally:
                os.unlink(tmp.name)
    
    @pytest.mark.asyncio
    async def test_detect_disease_tomato(self):
        """Test disease detection for tomato"""
        # Create a temporary test image
        import tempfile
        from PIL import Image
        
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp:
            img = Image.new('RGB', (224, 224), color='green')
            img.save(tmp.name, 'JPEG')
            
            try:
                result = await self.service.detect_disease(tmp.name, 'tomato')
                assert 'disease' in result
                assert 'confidence' in result
                assert 'severity' in result
                assert result['disease'] in self.service.disease_database['tomato']
            finally:
                os.unlink(tmp.name)
    
    def test_get_disease_info(self):
        """Test getting disease information"""
        info = self.service.get_disease_info('Bacterial_spot', 'tomato')
        assert 'disease_name' in info
        assert 'crop_type' in info
        assert 'symptoms' in info
        assert info['disease_name'] == 'Bacterial_spot'
        assert info['crop_type'] == 'tomato'

class TestPesticideRecommendationService:
    """Test Pesticide Recommendation Service"""
    
    def setup_method(self):
        self.service = PesticideRecommendationService()
    
    def test_service_initialization(self):
        """Test service initializes correctly"""
        assert self.service is not None
        assert hasattr(self.service, 'pesticide_database')
        assert 'tomato' in self.service.pesticide_database
    
    @pytest.mark.asyncio
    async def test_get_recommendations_bacterial_spot(self):
        """Test getting recommendations for bacterial spot"""
        recommendations = await self.service.get_recommendations(
            disease='Bacterial_spot',
            crop_type='tomato',
            severity='moderate',
            weather_conditions='humid'
        )
        
        assert 'primary_pesticides' in recommendations
        assert 'alternative_pesticides' in recommendations
        assert 'application_method' in recommendations
        assert 'timing' in recommendations
        assert 'follow_up_schedule' in recommendations
        assert len(recommendations['primary_pesticides']) > 0
    
    @pytest.mark.asyncio
    async def test_get_recommendations_healthy_crop(self):
        """Test getting recommendations for healthy crop"""
        recommendations = await self.service.get_recommendations(
            disease='Healthy',
            crop_type='tomato',
            severity='healthy',
            weather_conditions='sunny'
        )
        
        assert 'prevention_tips' in recommendations
        assert len(recommendations.get('primary_pesticides', [])) == 0
    
    def test_adjust_for_severity(self):
        """Test severity adjustment"""
        mock_disease_data = {
            'primary_pesticides': ['Copper Hydroxide', 'Mancozeb'],
            'alternative_pesticides': ['Streptomycin'],
            'application_method': 'Foliar spray'
        }
        
        # Test severe adjustment
        severe_result = self.service.adjust_for_severity(mock_disease_data, 'severe')
        assert 'combination treatment' in severe_result['application_method']
        
        # Test mild adjustment
        mild_result = self.service.adjust_for_severity(mock_disease_data, 'mild')
        assert mild_result is not None
    
    def test_get_timing_recommendations(self):
        """Test timing recommendations"""
        timing = self.service.get_timing_recommendations('Bacterial_spot', 'severe', 'rainy')
        assert isinstance(timing, list)
        assert len(timing) > 0
        assert any('rain' in t.lower() for t in timing)

class TestCostCalculationService:
    """Test Cost Calculation Service"""
    
    def setup_method(self):
        self.service = CostCalculationService()
    
    def test_service_initialization(self):
        """Test service initializes correctly"""
        assert self.service is not None
        assert hasattr(self.service, 'pesticide_prices')
        assert 'Copper Hydroxide' in self.service.pesticide_prices
    
    @pytest.mark.asyncio
    async def test_calculate_treatment_cost(self):
        """Test treatment cost calculation"""
        result = await self.service.calculate_treatment_cost(
            pesticides=['Copper Hydroxide'],
            farm_size=2.0,
            severity='moderate',
            location='Punjab'
        )
        
        assert 'pesticide_name' in result
        assert 'total_amount_needed' in result
        assert 'cost_estimate' in result
        assert 'water_needed' in result
        assert 'applications_needed' in result
        assert result['pesticide_name'] == 'Copper Hydroxide'
    
    def test_get_severity_multiplier(self):
        """Test severity multiplier calculation"""
        assert self.service.get_severity_multiplier('mild') == 0.8
        assert self.service.get_severity_multiplier('moderate') == 1.0
        assert self.service.get_severity_multiplier('severe') == 1.3
        assert self.service.get_severity_multiplier('healthy') == 0.0
    
    def test_get_regional_multiplier(self):
        """Test regional price multiplier"""
        # Test known regions
        punjab_multiplier = self.service.get_regional_multiplier('Punjab, India')
        assert punjab_multiplier == 1.0  # North region
        
        karnataka_multiplier = self.service.get_regional_multiplier('Karnataka, India')
        assert karnataka_multiplier == 1.1  # South region
        
        # Test unknown region
        unknown_multiplier = self.service.get_regional_multiplier('Unknown Location')
        assert unknown_multiplier == 1.0  # Default
    
    def test_get_applications_needed(self):
        """Test applications calculation"""
        assert self.service.get_applications_needed('mild') == 2
        assert self.service.get_applications_needed('moderate') == 3
        assert self.service.get_applications_needed('severe') == 4
        assert self.service.get_applications_needed('healthy') == 0
    
    def test_compare_pesticide_costs(self):
        """Test pesticide cost comparison"""
        comparison = self.service.compare_pesticide_costs(
            ['Copper Hydroxide', 'Mancozeb', 'Streptomycin'],
            farm_size=2.0
        )
        
        assert isinstance(comparison, list)
        assert len(comparison) == 3
        for item in comparison:
            assert 'pesticide' in item
            assert 'cost' in item
            assert 'effectiveness_rating' in item
    
    def test_calculate_seasonal_cost(self):
        """Test seasonal cost calculation"""
        seasonal = self.service.calculate_seasonal_cost('tomato', 2.0, 'Punjab')
        
        assert 'crop_type' in seasonal
        assert 'treatments_per_season' in seasonal
        assert 'total_seasonal_cost' in seasonal
        assert seasonal['crop_type'] == 'tomato'