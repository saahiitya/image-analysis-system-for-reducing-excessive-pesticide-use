"""
Disease Detection Service using AI/ML models
"""

import cv2
import numpy as np
import tensorflow as tf
from PIL import Image
import json
import os
from typing import Dict, List, Tuple
import logging

logger = logging.getLogger(__name__)

class DiseaseDetectionService:
    """
    Service for detecting diseases in crop images using deep learning models
    """
    
    def __init__(self):
        self.model = None
        self.class_names = {}
        self.confidence_threshold = 0.7
        self.load_models()
    
    def load_models(self):
        """
        Load pre-trained disease detection models
        """
        try:
            # In a real implementation, you would load actual trained models
            # For now, we'll simulate the model behavior
            self.disease_database = {
                'tomato': {
                    'Bacterial_spot': {
                        'symptoms': ['Dark spots on leaves', 'Yellow halos around spots'],
                        'severity_indicators': {
                            'mild': 'Few scattered spots',
                            'moderate': 'Multiple spots covering 10-30% of leaf area',
                            'severe': 'Extensive spotting covering >30% of leaf area'
                        }
                    },
                    'Early_blight': {
                        'symptoms': ['Concentric rings on leaves', 'Brown lesions'],
                        'severity_indicators': {
                            'mild': 'Few lesions on lower leaves',
                            'moderate': 'Lesions spreading to middle leaves',
                            'severe': 'Extensive defoliation and fruit infection'
                        }
                    },
                    'Late_blight': {
                        'symptoms': ['Water-soaked lesions', 'White fuzzy growth'],
                        'severity_indicators': {
                            'mild': 'Small water-soaked spots',
                            'moderate': 'Lesions expanding rapidly',
                            'severe': 'Plant collapse and fruit rot'
                        }
                    },
                    'Leaf_Mold': {
                        'symptoms': ['Yellow spots on upper leaf surface', 'Fuzzy growth underneath'],
                        'severity_indicators': {
                            'mild': 'Few yellow spots',
                            'moderate': 'Moderate leaf coverage',
                            'severe': 'Extensive leaf coverage and defoliation'
                        }
                    },
                    'Septoria_leaf_spot': {
                        'symptoms': ['Small circular spots with dark borders', 'Tiny black specks in center'],
                        'severity_indicators': {
                            'mild': 'Few spots on lower leaves',
                            'moderate': 'Spots spreading upward',
                            'severe': 'Severe defoliation'
                        }
                    },
                    'Spider_mites': {
                        'symptoms': ['Fine webbing on leaves', 'Stippled appearance', 'Yellow/bronze coloration'],
                        'severity_indicators': {
                            'mild': 'Light stippling on few leaves',
                            'moderate': 'Visible webbing and yellowing',
                            'severe': 'Heavy webbing and leaf drop'
                        }
                    },
                    'Target_Spot': {
                        'symptoms': ['Concentric ring patterns', 'Brown lesions'],
                        'severity_indicators': {
                            'mild': 'Few target spots',
                            'moderate': 'Multiple spots per leaf',
                            'severe': 'Extensive leaf damage'
                        }
                    },
                    'Mosaic_virus': {
                        'symptoms': ['Mottled yellow-green pattern', 'Distorted leaves'],
                        'severity_indicators': {
                            'mild': 'Slight mottling',
                            'moderate': 'Clear mosaic pattern',
                            'severe': 'Severe distortion and stunting'
                        }
                    },
                    'Yellow_Leaf_Curl_Virus': {
                        'symptoms': ['Upward curling of leaves', 'Yellowing', 'Stunted growth'],
                        'severity_indicators': {
                            'mild': 'Slight leaf curling',
                            'moderate': 'Pronounced curling and yellowing',
                            'severe': 'Severe stunting and yield loss'
                        }
                    },
                    'Healthy': {
                        'symptoms': ['Green healthy foliage', 'No visible damage'],
                        'severity_indicators': {
                            'healthy': 'No disease symptoms present'
                        }
                    }
                },
                'brinjal': {
                    'Bacterial_wilt': {
                        'symptoms': ['Wilting of leaves', 'Brown vascular discoloration'],
                        'severity_indicators': {
                            'mild': 'Few wilted leaves',
                            'moderate': 'Plant wilting during day',
                            'severe': 'Complete plant collapse'
                        }
                    },
                    'Cercospora_leaf_spot': {
                        'symptoms': ['Circular brown spots', 'Yellow halos'],
                        'severity_indicators': {
                            'mild': 'Few scattered spots',
                            'moderate': 'Multiple spots per leaf',
                            'severe': 'Extensive defoliation'
                        }
                    },
                    'Damping_off': {
                        'symptoms': ['Stem rot at soil level', 'Seedling collapse'],
                        'severity_indicators': {
                            'mild': 'Few affected seedlings',
                            'moderate': 'Patches of affected plants',
                            'severe': 'Widespread seedling death'
                        }
                    },
                    'Healthy': {
                        'symptoms': ['Green healthy foliage', 'No visible damage'],
                        'severity_indicators': {
                            'healthy': 'No disease symptoms present'
                        }
                    }
                },
                'capsicum': {
                    'Bacterial_spot': {
                        'symptoms': ['Dark spots on leaves and fruits', 'Raised lesions'],
                        'severity_indicators': {
                            'mild': 'Few spots on leaves',
                            'moderate': 'Spots on leaves and fruits',
                            'severe': 'Extensive fruit damage'
                        }
                    },
                    'Powdery_mildew': {
                        'symptoms': ['White powdery coating', 'Leaf distortion'],
                        'severity_indicators': {
                            'mild': 'Light powdery patches',
                            'moderate': 'Moderate leaf coverage',
                            'severe': 'Extensive coverage and defoliation'
                        }
                    },
                    'Anthracnose': {
                        'symptoms': ['Sunken lesions on fruits', 'Dark spots with pink centers'],
                        'severity_indicators': {
                            'mild': 'Few fruit lesions',
                            'moderate': 'Multiple lesions per fruit',
                            'severe': 'Fruit rot and unmarketable produce'
                        }
                    },
                    'Healthy': {
                        'symptoms': ['Green healthy foliage', 'No visible damage'],
                        'severity_indicators': {
                            'healthy': 'No disease symptoms present'
                        }
                    }
                }
            }
            
            logger.info("Disease detection models loaded successfully")
            
        except Exception as e:
            logger.error(f"Error loading disease detection models: {str(e)}")
            raise
    
    async def detect_disease(self, image_path: str, crop_type: str) -> Dict:
        """
        Detect disease in the uploaded crop image
        
        Args:
            image_path: Path to the uploaded image
            crop_type: Type of crop (tomato, brinjal, capsicum)
            
        Returns:
            Dictionary containing disease detection results
        """
        try:
            # Load and preprocess image
            image = self.preprocess_image(image_path)
            
            # Simulate AI model prediction
            # In a real implementation, this would use actual trained models
            prediction_result = self.simulate_disease_prediction(image, crop_type)
            
            return prediction_result
            
        except Exception as e:
            logger.error(f"Error in disease detection: {str(e)}")
            raise
    
    def preprocess_image(self, image_path: str) -> np.ndarray:
        """
        Preprocess image for model input
        """
        try:
            # Load image
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError(f"Could not load image from {image_path}")
            
            # Convert BGR to RGB
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Resize to model input size (typically 224x224 for most models)
            image = cv2.resize(image, (224, 224))
            
            # Normalize pixel values
            image = image.astype(np.float32) / 255.0
            
            # Add batch dimension
            image = np.expand_dims(image, axis=0)
            
            return image
            
        except Exception as e:
            logger.error(f"Error preprocessing image: {str(e)}")
            raise
    
    def simulate_disease_prediction(self, image: np.ndarray, crop_type: str) -> Dict:
        """
        Simulate disease prediction (replace with actual model inference)
        """
        try:
            # Get available diseases for the crop type
            available_diseases = list(self.disease_database.get(crop_type, {}).keys())
            
            if not available_diseases:
                return {
                    'disease': 'Unknown',
                    'confidence': 0.0,
                    'severity': 'unknown'
                }
            
            # Simulate prediction based on image characteristics
            # In reality, this would be model.predict(image)
            
            # Simple simulation based on image properties
            image_mean = np.mean(image)
            image_std = np.std(image)
            
            # Simulate different disease probabilities based on image characteristics
            if image_mean > 0.6 and image_std < 0.2:
                # Bright, uniform image - likely healthy
                predicted_disease = 'Healthy'
                confidence = 0.92
                severity = 'healthy'
            elif image_mean < 0.3:
                # Dark image - might indicate severe disease
                predicted_disease = available_diseases[1] if len(available_diseases) > 1 else available_diseases[0]
                confidence = 0.85
                severity = 'severe'
            elif image_std > 0.3:
                # High variation - might indicate moderate disease
                predicted_disease = available_diseases[2] if len(available_diseases) > 2 else available_diseases[0]
                confidence = 0.78
                severity = 'moderate'
            else:
                # Default to mild disease
                predicted_disease = available_diseases[1] if len(available_diseases) > 1 else available_diseases[0]
                confidence = 0.73
                severity = 'mild'
            
            return {
                'disease': predicted_disease,
                'confidence': confidence,
                'severity': severity,
                'symptoms': self.disease_database[crop_type][predicted_disease]['symptoms'],
                'severity_description': self.disease_database[crop_type][predicted_disease]['severity_indicators'].get(severity, 'Unknown severity')
            }
            
        except Exception as e:
            logger.error(f"Error in disease prediction simulation: {str(e)}")
            return {
                'disease': 'Error',
                'confidence': 0.0,
                'severity': 'unknown'
            }
    
    def analyze_image_features(self, image: np.ndarray) -> Dict:
        """
        Extract features from image for disease analysis
        """
        try:
            # Convert to single image if batch
            if len(image.shape) == 4:
                image = image[0]
            
            # Convert to uint8 for OpenCV operations
            image_uint8 = (image * 255).astype(np.uint8)
            
            # Color analysis
            mean_rgb = np.mean(image_uint8, axis=(0, 1))
            
            # Convert to HSV for better color analysis
            hsv = cv2.cvtColor(image_uint8, cv2.COLOR_RGB2HSV)
            
            # Calculate color distribution
            green_mask = cv2.inRange(hsv, (40, 40, 40), (80, 255, 255))
            brown_mask = cv2.inRange(hsv, (10, 50, 20), (20, 255, 200))
            yellow_mask = cv2.inRange(hsv, (20, 100, 100), (30, 255, 255))
            
            green_ratio = np.sum(green_mask > 0) / (image_uint8.shape[0] * image_uint8.shape[1])
            brown_ratio = np.sum(brown_mask > 0) / (image_uint8.shape[0] * image_uint8.shape[1])
            yellow_ratio = np.sum(yellow_mask > 0) / (image_uint8.shape[0] * image_uint8.shape[1])
            
            # Texture analysis using Laplacian variance
            gray = cv2.cvtColor(image_uint8, cv2.COLOR_RGB2GRAY)
            laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
            
            return {
                'mean_rgb': mean_rgb.tolist(),
                'green_ratio': green_ratio,
                'brown_ratio': brown_ratio,
                'yellow_ratio': yellow_ratio,
                'texture_variance': laplacian_var,
                'overall_brightness': np.mean(image_uint8)
            }
            
        except Exception as e:
            logger.error(f"Error analyzing image features: {str(e)}")
            return {}
    
    def get_disease_info(self, disease_name: str, crop_type: str) -> Dict:
        """
        Get detailed information about a specific disease
        """
        try:
            crop_diseases = self.disease_database.get(crop_type, {})
            disease_info = crop_diseases.get(disease_name, {})
            
            return {
                'disease_name': disease_name,
                'crop_type': crop_type,
                'symptoms': disease_info.get('symptoms', []),
                'severity_indicators': disease_info.get('severity_indicators', {}),
                'description': f"{disease_name} affecting {crop_type}"
            }
            
        except Exception as e:
            logger.error(f"Error getting disease info: {str(e)}")
            return {}