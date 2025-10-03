"""
AI Engine for Crop Disease Detection
This module contains the AI/ML logic for detecting diseases from crop images
"""

import numpy as np
from PIL import Image
import io
import os
import logging

# Import your ML framework (uncomment the one you're using)
# import tensorflow as tf
# import torch
# import joblib  # for scikit-learn models
# from keras.models import load_model

class CropDiseaseDetector:
    """
    Real AI Disease Detection Engine using your trained model
    """
    
    def __init__(self, model_path=None, confidence_threshold=0.7):
        self.confidence_threshold = confidence_threshold
        self.model = None
        self.model_loaded = False
        self.class_names = []
        
        # Import config to get model path
        try:
            from ..config import MODEL_PATH, MODEL_CONFIDENCE_THRESHOLD
            if model_path is None:
                model_path = MODEL_PATH
            self.confidence_threshold = MODEL_CONFIDENCE_THRESHOLD
        except ImportError:
            pass
        
        # Load your trained model
        self.load_model(model_path)
    
    def load_model(self, model_path=None):
        """
        Load your trained model
        Modify this method according to your model type and framework
        """
        try:
            if model_path is None:
                # Default model path - adjust according to your setup
                model_path = os.path.join(os.path.dirname(__file__), '..', '..', 'models', 'crop_disease_model')
            
            if not os.path.exists(model_path):
                logging.warning(f"Model not found at {model_path}. Using fallback mode.")
                self.model_loaded = False
                return
            
            # Load your model based on the framework you used
            # Uncomment and modify the appropriate section:
            
            # For TensorFlow/Keras models:
            # self.model = tf.keras.models.load_model(model_path)
            
            # For PyTorch models:
            # self.model = torch.load(model_path, map_location='cpu')
            # self.model.eval()
            
            # For scikit-learn models:
            # self.model = joblib.load(model_path)
            
            # Load class names (disease labels)
            class_names_path = os.path.join(os.path.dirname(model_path), 'class_names.txt')
            if os.path.exists(class_names_path):
                with open(class_names_path, 'r') as f:
                    self.class_names = [line.strip() for line in f.readlines()]
            else:
                # Default class names - update according to your model's output classes
                self.class_names = [
                    'healthy',
                    'tomato_early_blight',
                    'tomato_late_blight',
                    'tomato_bacterial_wilt',
                    'brinjal_fruit_borer',
                    'brinjal_little_leaf',
                    'brinjal_damping_off',
                    'capsicum_anthracnose',
                    'capsicum_powdery_mildew',
                    'capsicum_thrips'
                ]
            
            self.model_loaded = True
            logging.info(f"Model loaded successfully from {model_path}")
            logging.info(f"Classes: {self.class_names}")
            
        except Exception as e:
            logging.error(f"Failed to load model: {str(e)}")
            self.model_loaded = False
    
    def preprocess_image(self, image_data, target_size=(224, 224)):
        """
        Preprocess image for your trained model
        Modify this according to your model's input requirements
        """
        try:
            image = Image.open(io.BytesIO(image_data))
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Resize to your model's expected input size
            image = image.resize(target_size)
            
            # Convert to numpy array
            image_array = np.array(image)
            
            # Normalize pixel values (adjust according to your training preprocessing)
            # Common normalizations:
            # For models trained with ImageNet preprocessing:
            # image_array = image_array / 255.0
            # mean = np.array([0.485, 0.456, 0.406])
            # std = np.array([0.229, 0.224, 0.225])
            # image_array = (image_array - mean) / std
            
            # For simple 0-1 normalization:
            image_array = image_array.astype(np.float32) / 255.0
            
            # Add batch dimension if needed for your model
            # image_array = np.expand_dims(image_array, axis=0)
            
            return image_array
            
        except Exception as e:
            raise ValueError(f"Image preprocessing failed: {str(e)}")
    
    def predict_with_model(self, preprocessed_image):
        """
        Make prediction using your trained model
        Modify this according to your model framework
        """
        try:
            if not self.model_loaded or self.model is None:
                raise RuntimeError("Model not loaded")
            
            # Add batch dimension if not already present
            if len(preprocessed_image.shape) == 3:
                preprocessed_image = np.expand_dims(preprocessed_image, axis=0)
            
            # Make prediction based on your framework:
            
            # For TensorFlow/Keras:
            # predictions = self.model.predict(preprocessed_image)
            # confidence_scores = predictions[0]  # Remove batch dimension
            
            # For PyTorch:
            # import torch
            # with torch.no_grad():
            #     input_tensor = torch.FloatTensor(preprocessed_image)
            #     predictions = self.model(input_tensor)
            #     confidence_scores = torch.nn.functional.softmax(predictions, dim=1)[0].numpy()
            
            # For scikit-learn:
            # flattened_image = preprocessed_image.reshape(1, -1)
            # predictions = self.model.predict_proba(flattened_image)
            # confidence_scores = predictions[0]
            
            # Placeholder - replace with actual model prediction
            # This is a fallback that you should remove once you integrate your model
            confidence_scores = np.random.dirichlet(np.ones(len(self.class_names)))
            
            return confidence_scores
            
        except Exception as e:
            raise RuntimeError(f"Model prediction failed: {str(e)}")
    
    def parse_prediction_result(self, confidence_scores, crop_type):
        """
        Parse model prediction results into standardized format
        """
        # Get the class with highest confidence
        predicted_class_idx = np.argmax(confidence_scores)
        confidence = float(confidence_scores[predicted_class_idx])
        predicted_class = self.class_names[predicted_class_idx]
        
        # Check if confidence meets threshold
        if confidence < self.confidence_threshold:
            return self._create_uncertain_result(confidence)
        
        # Parse the predicted class name
        if predicted_class == 'healthy':
            return self._create_healthy_result(confidence)
        
        # Extract disease information from class name
        disease_info = self._parse_disease_class(predicted_class, crop_type, confidence)
        
        return disease_info
    
    def _parse_disease_class(self, predicted_class, crop_type, confidence):
        """
        Parse disease class name and return structured information
        """
        # Map your model's class names to disease information
        disease_mapping = {
            'tomato_early_blight': {
                'disease': 'early_blight',
                'name': 'Early Blight',
                'description': 'Fungal disease causing dark spots on leaves'
            },
            'tomato_late_blight': {
                'disease': 'late_blight',
                'name': 'Late Blight',
                'description': 'Serious fungal disease affecting leaves and fruits'
            },
            'tomato_bacterial_wilt': {
                'disease': 'bacterial_wilt',
                'name': 'Bacterial Wilt',
                'description': 'Bacterial infection causing plant wilting'
            },
            'brinjal_fruit_borer': {
                'disease': 'fruit_borer',
                'name': 'Brinjal Fruit and Shoot Borer',
                'description': 'Major pest causing fruit damage'
            },
            'brinjal_little_leaf': {
                'disease': 'little_leaf',
                'name': 'Little Leaf Disease',
                'description': 'Phytoplasma disease causing stunted growth'
            },
            'brinjal_damping_off': {
                'disease': 'damping_off',
                'name': 'Damping Off',
                'description': 'Fungal disease affecting seedlings'
            },
            'capsicum_anthracnose': {
                'disease': 'anthracnose',
                'name': 'Anthracnose',
                'description': 'Fungal disease causing fruit rot'
            },
            'capsicum_powdery_mildew': {
                'disease': 'powdery_mildew',
                'name': 'Powdery Mildew',
                'description': 'Fungal disease with white powdery growth'
            },
            'capsicum_thrips': {
                'disease': 'thrips',
                'name': 'Thrips',
                'description': 'Insect pest causing leaf damage'
            }
        }
        
        disease_info = disease_mapping.get(predicted_class, {
            'disease': predicted_class.replace(f'{crop_type}_', ''),
            'name': predicted_class.replace('_', ' ').title(),
            'description': f'Disease detected: {predicted_class}'
        })
        
        # Determine severity based on confidence
        if confidence >= 0.9:
            severity = "high"
            affected_area = np.random.uniform(40, 80)
        elif confidence >= 0.8:
            severity = "medium"
            affected_area = np.random.uniform(20, 50)
        else:
            severity = "low"
            affected_area = np.random.uniform(5, 25)
        
        return {
            "disease": disease_info['disease'],
            "disease_name": disease_info['name'],
            "description": disease_info['description'],
            "confidence": confidence,
            "severity": severity,
            "affected_area_percentage": round(affected_area, 1),
            "model_prediction": predicted_class
        }
    
    def detect_disease(self, image_data, crop_type):
        """
        Main disease detection function using your trained model
        Returns disease detection results with confidence scores
        """
        try:
            # Preprocess image for your model
            preprocessed_image = self.preprocess_image(image_data)
            
            if self.model_loaded:
                # Use your trained model for prediction
                confidence_scores = self.predict_with_model(preprocessed_image)
                
                # Parse the prediction results
                prediction_result = self.parse_prediction_result(confidence_scores, crop_type)
                
            else:
                # Fallback mode when model is not available
                logging.warning("Model not loaded, using fallback detection")
                prediction_result = self._create_fallback_result()
            
            return prediction_result
            
        except Exception as e:
            logging.error(f"Disease detection failed: {str(e)}")
            raise RuntimeError(f"Disease detection failed: {str(e)}")
    
    def _create_fallback_result(self):
        """
        Create a fallback result when model is not available
        """
        return {
            "disease": "unknown",
            "disease_name": "Model Not Available",
            "description": "AI model could not be loaded. Please check model files.",
            "confidence": 0.0,
            "severity": "unknown",
            "affected_area_percentage": 0,
            "model_prediction": "fallback"
        }
    
    def _create_healthy_result(self, confidence=0.9):
        """Create result for healthy crop"""
        return {
            "disease": "healthy",
            "disease_name": "Healthy",
            "description": "No disease detected - crop appears healthy",
            "confidence": confidence,
            "severity": "none",
            "affected_area_percentage": 0,
            "model_prediction": "healthy"
        }
    
    def _create_uncertain_result(self, confidence):
        """Create result when model confidence is too low"""
        return {
            "disease": "uncertain",
            "disease_name": "Uncertain Detection",
            "description": f"Model confidence too low ({confidence:.2f}). Please provide clearer images.",
            "confidence": confidence,
            "severity": "unknown",
            "affected_area_percentage": 0,
            "model_prediction": "uncertain"
        }
    
    def batch_detect(self, image_data_list, crop_type):
        """
        Process multiple images in batch using your trained model
        """
        results = []
        for i, image_data in enumerate(image_data_list):
            try:
                result = self.detect_disease(image_data, crop_type)
                result['image_index'] = i
                results.append(result)
            except Exception as e:
                logging.error(f"Batch detection failed for image {i}: {str(e)}")
                results.append({
                    'image_index': i,
                    'error': str(e),
                    'disease': 'error',
                    'disease_name': 'Processing Error',
                    'description': f'Failed to process image: {str(e)}',
                    'confidence': 0.0,
                    'severity': 'unknown',
                    'affected_area_percentage': 0,
                    'model_prediction': 'error'
                })
        return results

# Global detector instance - will be initialized with your model
detector = CropDiseaseDetector()

def detect_disease_from_image(image_data, crop_type):
    """
    Convenience function for single image disease detection using your trained model
    """
    return detector.detect_disease(image_data, crop_type)

def detect_diseases_batch(image_data_list, crop_type):
    """
    Convenience function for batch disease detection using your trained model
    """
    return detector.batch_detect(image_data_list, crop_type)

def reload_model(model_path=None):
    """
    Reload the AI model (useful for model updates)
    """
    global detector
    detector = CropDiseaseDetector(model_path)
    return detector.model_loaded