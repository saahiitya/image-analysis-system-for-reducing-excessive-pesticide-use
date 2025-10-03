"""
AI Engine for Crop Disease Detection
This module contains the AI/ML logic for detecting diseases from crop images
"""

import random
import numpy as np
from PIL import Image
import io
from .disease_db import get_all_diseases_for_crop, DISEASE_DATABASE

class CropDiseaseDetector:
    """
    Mock AI Disease Detection Engine
    In production, this would be replaced with a trained deep learning model
    """
    
    def __init__(self, confidence_threshold=0.7):
        self.confidence_threshold = confidence_threshold
        self.model_loaded = True  # Mock model loading
    
    def preprocess_image(self, image_data):
        """
        Preprocess image for AI analysis
        In production, this would include normalization, resizing, etc.
        """
        try:
            image = Image.open(io.BytesIO(image_data))
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Resize to standard size (mock preprocessing)
            image = image.resize((224, 224))
            
            # Convert to numpy array (mock feature extraction)
            image_array = np.array(image)
            
            return image_array
        except Exception as e:
            raise ValueError(f"Image preprocessing failed: {str(e)}")
    
    def extract_features(self, image_array):
        """
        Extract features from preprocessed image
        In production, this would use CNN feature extraction
        """
        # Mock feature extraction - calculate some basic image statistics
        features = {
            'mean_rgb': np.mean(image_array, axis=(0, 1)),
            'std_rgb': np.std(image_array, axis=(0, 1)),
            'brightness': np.mean(image_array),
            'contrast': np.std(image_array),
            'green_ratio': np.mean(image_array[:, :, 1]) / np.mean(image_array)
        }
        return features
    
    def detect_disease(self, image_data, crop_type):
        """
        Main disease detection function
        Returns disease detection results with confidence scores
        """
        try:
            # Preprocess image
            image_array = self.preprocess_image(image_data)
            
            # Extract features
            features = self.extract_features(image_array)
            
            # Get available diseases for the crop
            available_diseases = get_all_diseases_for_crop(crop_type)
            
            if not available_diseases:
                return self._create_healthy_result()
            
            # Mock AI prediction logic
            # In production, this would be model.predict(features)
            prediction_result = self._mock_prediction(features, available_diseases, crop_type)
            
            return prediction_result
            
        except Exception as e:
            raise RuntimeError(f"Disease detection failed: {str(e)}")
    
    def _mock_prediction(self, features, available_diseases, crop_type):
        """
        Mock AI prediction logic
        Simulates realistic disease detection with varying probabilities
        """
        # Simulate disease probability based on image features
        green_ratio = features['green_ratio']
        brightness = features['brightness']
        contrast = features['contrast']
        
        # Healthy crop typically has high green ratio and good contrast
        health_score = (green_ratio * 0.4 + (contrast / 255) * 0.3 + 
                       (1 - abs(brightness - 128) / 128) * 0.3)
        
        # Determine if crop is healthy or diseased
        if health_score > 0.7 and random.random() > 0.3:
            return self._create_healthy_result()
        
        # Select a disease (weighted by common occurrence)
        disease_weights = self._get_disease_weights(crop_type)
        selected_disease = random.choices(
            available_diseases, 
            weights=[disease_weights.get(d, 1.0) for d in available_diseases]
        )[0]
        
        # Generate confidence score
        base_confidence = random.uniform(0.75, 0.95)
        confidence = min(0.95, base_confidence * (1 - health_score * 0.2))
        
        # Determine severity based on health score
        if health_score > 0.5:
            severity = "low"
        elif health_score > 0.3:
            severity = "medium"
        else:
            severity = "high"
        
        # Calculate affected area percentage
        affected_area = self._calculate_affected_area(severity, health_score)
        
        return {
            "disease": selected_disease,
            "confidence": round(confidence, 3),
            "severity": severity,
            "affected_area_percentage": round(affected_area, 1),
            "health_score": round(health_score, 3)
        }
    
    def _create_healthy_result(self):
        """Create result for healthy crop"""
        return {
            "disease": "healthy",
            "confidence": random.uniform(0.85, 0.95),
            "severity": "none",
            "affected_area_percentage": 0,
            "health_score": random.uniform(0.8, 0.95)
        }
    
    def _get_disease_weights(self, crop_type):
        """
        Get disease occurrence weights for more realistic simulation
        Based on common disease prevalence in Indian agriculture
        """
        weights = {
            "tomato": {
                "early_blight": 3.0,
                "late_blight": 2.5,
                "bacterial_wilt": 1.5
            },
            "brinjal": {
                "fruit_borer": 4.0,
                "little_leaf": 2.0,
                "damping_off": 1.0
            },
            "capsicum": {
                "thrips": 3.5,
                "powdery_mildew": 2.5,
                "anthracnose": 2.0
            }
        }
        return weights.get(crop_type.lower(), {})
    
    def _calculate_affected_area(self, severity, health_score):
        """Calculate affected area percentage based on severity and health score"""
        base_areas = {
            "low": (5, 25),
            "medium": (20, 50),
            "high": (40, 80)
        }
        
        min_area, max_area = base_areas.get(severity, (10, 30))
        
        # Adjust based on health score (lower health = higher affected area)
        health_factor = 1 - health_score
        adjusted_max = min(max_area + health_factor * 20, 90)
        
        return random.uniform(min_area, adjusted_max)
    
    def batch_detect(self, image_data_list, crop_type):
        """
        Process multiple images in batch
        """
        results = []
        for i, image_data in enumerate(image_data_list):
            try:
                result = self.detect_disease(image_data, crop_type)
                result['image_index'] = i
                results.append(result)
            except Exception as e:
                results.append({
                    'image_index': i,
                    'error': str(e),
                    'disease': 'error',
                    'confidence': 0.0,
                    'severity': 'unknown',
                    'affected_area_percentage': 0
                })
        return results

# Global detector instance
detector = CropDiseaseDetector()

def detect_disease_from_image(image_data, crop_type):
    """
    Convenience function for single image disease detection
    """
    return detector.detect_disease(image_data, crop_type)

def detect_diseases_batch(image_data_list, crop_type):
    """
    Convenience function for batch disease detection
    """
    return detector.batch_detect(image_data_list, crop_type)