"""
Pesticide Recommendation Service
"""

import json
import logging
from typing import Dict, List, Optional
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class PesticideRecommendationService:
    """
    Service for recommending appropriate pesticides based on disease and conditions
    """
    
    def __init__(self):
        self.pesticide_database = {}
        self.load_pesticide_data()
    
    def load_pesticide_data(self):
        """
        Load pesticide database with treatment recommendations
        """
        self.pesticide_database = {
            'tomato': {
                'Bacterial_spot': {
                    'primary_pesticides': ['Copper Hydroxide', 'Streptomycin'],
                    'alternative_pesticides': ['Copper Sulfate', 'Mancozeb'],
                    'application_method': 'Foliar spray',
                    'dosage_per_hectare': {
                        'Copper Hydroxide': 2.5,  # kg/ha
                        'Streptomycin': 0.5,      # kg/ha
                        'Copper Sulfate': 3.0,    # kg/ha
                        'Mancozeb': 2.0           # kg/ha
                    },
                    'price_per_kg': {
                        'Copper Hydroxide': 450,
                        'Streptomycin': 1200,
                        'Copper Sulfate': 380,
                        'Mancozeb': 520
                    },
                    'application_frequency': 'Every 7-10 days',
                    'safety_period': 7,  # days before harvest
                    'prevention_tips': [
                        'Use disease-free seeds',
                        'Avoid overhead irrigation',
                        'Maintain proper plant spacing',
                        'Remove infected plant debris'
                    ]
                },
                'Early_blight': {
                    'primary_pesticides': ['Mancozeb', 'Chlorothalonil'],
                    'alternative_pesticides': ['Copper Hydroxide', 'Metalaxyl'],
                    'application_method': 'Foliar spray',
                    'dosage_per_hectare': {
                        'Mancozeb': 2.5,
                        'Chlorothalonil': 2.0,
                        'Copper Hydroxide': 2.5,
                        'Metalaxyl': 1.5
                    },
                    'price_per_kg': {
                        'Mancozeb': 520,
                        'Chlorothalonil': 680,
                        'Copper Hydroxide': 450,
                        'Metalaxyl': 950
                    },
                    'application_frequency': 'Every 10-14 days',
                    'safety_period': 14,
                    'prevention_tips': [
                        'Crop rotation',
                        'Remove lower leaves touching soil',
                        'Improve air circulation',
                        'Avoid water stress'
                    ]
                },
                'Late_blight': {
                    'primary_pesticides': ['Metalaxyl + Mancozeb', 'Cymoxanil'],
                    'alternative_pesticides': ['Copper Hydroxide', 'Fosetyl-Al'],
                    'application_method': 'Foliar spray',
                    'dosage_per_hectare': {
                        'Metalaxyl + Mancozeb': 2.0,
                        'Cymoxanil': 0.5,
                        'Copper Hydroxide': 3.0,
                        'Fosetyl-Al': 2.5
                    },
                    'price_per_kg': {
                        'Metalaxyl + Mancozeb': 850,
                        'Cymoxanil': 1200,
                        'Copper Hydroxide': 450,
                        'Fosetyl-Al': 780
                    },
                    'application_frequency': 'Every 5-7 days during outbreak',
                    'safety_period': 21,
                    'prevention_tips': [
                        'Monitor weather conditions',
                        'Use resistant varieties',
                        'Ensure good drainage',
                        'Apply preventive sprays'
                    ]
                },
                'Leaf_Mold': {
                    'primary_pesticides': ['Chlorothalonil', 'Mancozeb'],
                    'alternative_pesticides': ['Copper Hydroxide', 'Propiconazole'],
                    'application_method': 'Foliar spray',
                    'dosage_per_hectare': {
                        'Chlorothalonil': 2.0,
                        'Mancozeb': 2.5,
                        'Copper Hydroxide': 2.5,
                        'Propiconazole': 0.5
                    },
                    'price_per_kg': {
                        'Chlorothalonil': 680,
                        'Mancozeb': 520,
                        'Copper Hydroxide': 450,
                        'Propiconazole': 1500
                    },
                    'application_frequency': 'Every 10-14 days',
                    'safety_period': 14,
                    'prevention_tips': [
                        'Improve greenhouse ventilation',
                        'Reduce humidity',
                        'Avoid overhead watering',
                        'Remove infected leaves'
                    ]
                },
                'Healthy': {
                    'primary_pesticides': [],
                    'alternative_pesticides': [],
                    'application_method': 'Preventive measures only',
                    'prevention_tips': [
                        'Maintain good plant hygiene',
                        'Regular monitoring',
                        'Proper nutrition',
                        'Adequate spacing'
                    ]
                }
            },
            'brinjal': {
                'Bacterial_wilt': {
                    'primary_pesticides': ['Streptomycin', 'Copper Hydroxide'],
                    'alternative_pesticides': ['Copper Sulfate', 'Bleaching Powder'],
                    'application_method': 'Soil drench and foliar spray',
                    'dosage_per_hectare': {
                        'Streptomycin': 0.5,
                        'Copper Hydroxide': 2.5,
                        'Copper Sulfate': 3.0,
                        'Bleaching Powder': 10.0
                    },
                    'price_per_kg': {
                        'Streptomycin': 1200,
                        'Copper Hydroxide': 450,
                        'Copper Sulfate': 380,
                        'Bleaching Powder': 150
                    },
                    'application_frequency': 'Every 15 days',
                    'safety_period': 14,
                    'prevention_tips': [
                        'Use resistant varieties',
                        'Soil solarization',
                        'Crop rotation',
                        'Avoid waterlogging'
                    ]
                },
                'Cercospora_leaf_spot': {
                    'primary_pesticides': ['Mancozeb', 'Chlorothalonil'],
                    'alternative_pesticides': ['Copper Hydroxide', 'Carbendazim'],
                    'application_method': 'Foliar spray',
                    'dosage_per_hectare': {
                        'Mancozeb': 2.5,
                        'Chlorothalonil': 2.0,
                        'Copper Hydroxide': 2.5,
                        'Carbendazim': 1.0
                    },
                    'price_per_kg': {
                        'Mancozeb': 520,
                        'Chlorothalonil': 680,
                        'Copper Hydroxide': 450,
                        'Carbendazim': 850
                    },
                    'application_frequency': 'Every 10-14 days',
                    'safety_period': 14,
                    'prevention_tips': [
                        'Remove infected leaves',
                        'Improve air circulation',
                        'Avoid overhead irrigation',
                        'Use clean seeds'
                    ]
                },
                'Healthy': {
                    'primary_pesticides': [],
                    'alternative_pesticides': [],
                    'application_method': 'Preventive measures only',
                    'prevention_tips': [
                        'Regular field inspection',
                        'Proper fertilization',
                        'Weed management',
                        'Integrated pest management'
                    ]
                }
            },
            'capsicum': {
                'Bacterial_spot': {
                    'primary_pesticides': ['Copper Hydroxide', 'Streptomycin'],
                    'alternative_pesticides': ['Copper Sulfate', 'Mancozeb'],
                    'application_method': 'Foliar spray',
                    'dosage_per_hectare': {
                        'Copper Hydroxide': 2.5,
                        'Streptomycin': 0.5,
                        'Copper Sulfate': 3.0,
                        'Mancozeb': 2.0
                    },
                    'price_per_kg': {
                        'Copper Hydroxide': 450,
                        'Streptomycin': 1200,
                        'Copper Sulfate': 380,
                        'Mancozeb': 520
                    },
                    'application_frequency': 'Every 7-10 days',
                    'safety_period': 7,
                    'prevention_tips': [
                        'Use certified seeds',
                        'Avoid water splash',
                        'Sanitize tools',
                        'Remove plant debris'
                    ]
                },
                'Powdery_mildew': {
                    'primary_pesticides': ['Sulfur', 'Propiconazole'],
                    'alternative_pesticides': ['Carbendazim', 'Triadimefon'],
                    'application_method': 'Foliar spray',
                    'dosage_per_hectare': {
                        'Sulfur': 3.0,
                        'Propiconazole': 0.5,
                        'Carbendazim': 1.0,
                        'Triadimefon': 0.25
                    },
                    'price_per_kg': {
                        'Sulfur': 200,
                        'Propiconazole': 1500,
                        'Carbendazim': 850,
                        'Triadimefon': 2000
                    },
                    'application_frequency': 'Every 10-14 days',
                    'safety_period': 14,
                    'prevention_tips': [
                        'Ensure good air circulation',
                        'Avoid excessive nitrogen',
                        'Monitor humidity levels',
                        'Use resistant varieties'
                    ]
                },
                'Anthracnose': {
                    'primary_pesticides': ['Mancozeb', 'Chlorothalonil'],
                    'alternative_pesticides': ['Copper Hydroxide', 'Carbendazim'],
                    'application_method': 'Foliar spray',
                    'dosage_per_hectare': {
                        'Mancozeb': 2.5,
                        'Chlorothalonil': 2.0,
                        'Copper Hydroxide': 2.5,
                        'Carbendazim': 1.0
                    },
                    'price_per_kg': {
                        'Mancozeb': 520,
                        'Chlorothalonil': 680,
                        'Copper Hydroxide': 450,
                        'Carbendazim': 850
                    },
                    'application_frequency': 'Every 10-14 days',
                    'safety_period': 14,
                    'prevention_tips': [
                        'Harvest fruits at proper maturity',
                        'Handle fruits carefully',
                        'Maintain field sanitation',
                        'Store in proper conditions'
                    ]
                },
                'Healthy': {
                    'primary_pesticides': [],
                    'alternative_pesticides': [],
                    'application_method': 'Preventive measures only',
                    'prevention_tips': [
                        'Regular monitoring',
                        'Balanced nutrition',
                        'Proper irrigation',
                        'Pest management'
                    ]
                }
            }
        }
        
        logger.info("Pesticide database loaded successfully")
    
    async def get_recommendations(
        self, 
        disease: str, 
        crop_type: str, 
        severity: str, 
        weather_conditions: str = ""
    ) -> Dict:
        """
        Get pesticide recommendations based on disease and conditions
        """
        try:
            crop_data = self.pesticide_database.get(crop_type, {})
            disease_data = crop_data.get(disease, {})
            
            if not disease_data:
                return self.get_default_recommendations(crop_type)
            
            # Adjust recommendations based on severity
            recommendations = self.adjust_for_severity(disease_data, severity)
            
            # Consider weather conditions
            recommendations = self.adjust_for_weather(recommendations, weather_conditions)
            
            # Add timing recommendations
            recommendations['timing'] = self.get_timing_recommendations(
                disease, severity, weather_conditions
            )
            
            # Add follow-up schedule
            recommendations['follow_up_schedule'] = self.get_follow_up_schedule(
                disease, severity
            )
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error getting pesticide recommendations: {str(e)}")
            return self.get_default_recommendations(crop_type)
    
    def adjust_for_severity(self, disease_data: Dict, severity: str) -> Dict:
        """
        Adjust pesticide recommendations based on disease severity
        """
        recommendations = disease_data.copy()
        
        if severity == 'severe':
            # For severe infections, prioritize stronger pesticides
            if len(recommendations.get('primary_pesticides', [])) > 1:
                # Recommend combination treatment for severe cases
                recommendations['application_method'] += ' (combination treatment recommended)'
                recommendations['application_frequency'] = 'Every 5-7 days until controlled'
            
        elif severity == 'mild':
            # For mild infections, prefer gentler options
            if recommendations.get('alternative_pesticides'):
                # Swap primary and alternative for mild cases
                primary = recommendations.get('primary_pesticides', [])
                alternative = recommendations.get('alternative_pesticides', [])
                
                # Prefer copper-based or organic options for mild cases
                copper_options = [p for p in primary + alternative if 'copper' in p.lower()]
                if copper_options:
                    recommendations['primary_pesticides'] = copper_options[:2]
        
        return recommendations
    
    def adjust_for_weather(self, recommendations: Dict, weather_conditions: str) -> Dict:
        """
        Adjust recommendations based on weather conditions
        """
        if not weather_conditions:
            return recommendations
        
        weather_lower = weather_conditions.lower()
        
        # Adjust for rainy conditions
        if any(word in weather_lower for word in ['rain', 'wet', 'humid']):
            recommendations['weather_note'] = 'Avoid application during rain. Apply systemic fungicides for better rain-fastness.'
            
        # Adjust for hot/dry conditions
        elif any(word in weather_lower for word in ['hot', 'dry', 'sunny']):
            recommendations['weather_note'] = 'Apply during cooler parts of day (early morning/evening). Increase water volume for better coverage.'
            
        # Adjust for windy conditions
        elif 'wind' in weather_lower:
            recommendations['weather_note'] = 'Avoid application during windy conditions to prevent drift. Use appropriate nozzles.'
        
        return recommendations
    
    def get_timing_recommendations(self, disease: str, severity: str, weather: str) -> List[str]:
        """
        Get timing recommendations for pesticide application
        """
        timing = []
        
        # Base timing recommendations
        if severity == 'severe':
            timing.append('Apply immediately upon detection')
            timing.append('Repeat application every 5-7 days')
        else:
            timing.append('Apply at first sign of symptoms')
            timing.append('Follow regular spray schedule')
        
        # Weather-based timing
        if 'rain' in weather.lower():
            timing.append('Apply after rain stops and leaves dry')
            timing.append('Check weather forecast for 24-hour rain-free period')
        else:
            timing.append('Best application time: Early morning (6-10 AM) or evening (4-7 PM)')
            timing.append('Avoid application during peak sun hours')
        
        # Disease-specific timing
        if 'blight' in disease.lower():
            timing.append('Apply preventively during favorable disease conditions')
        elif 'spot' in disease.lower():
            timing.append('Apply at 7-10 day intervals during disease season')
        
        return timing
    
    def get_follow_up_schedule(self, disease: str, severity: str) -> List[str]:
        """
        Get follow-up schedule recommendations
        """
        schedule = []
        
        if severity == 'severe':
            schedule = [
                'Monitor daily for first week',
                'Assess treatment effectiveness after 7 days',
                'Continue treatment every 5-7 days until controlled',
                'Switch to preventive schedule once controlled'
            ]
        elif severity == 'moderate':
            schedule = [
                'Monitor every 2-3 days',
                'Assess after 10 days',
                'Continue treatment every 10-14 days',
                'Reduce frequency as symptoms improve'
            ]
        else:  # mild
            schedule = [
                'Monitor weekly',
                'Assess after 14 days',
                'Apply preventive treatments as needed',
                'Continue monitoring throughout season'
            ]
        
        # Add disease-specific follow-up
        if disease.lower() == 'healthy':
            schedule = [
                'Continue regular monitoring',
                'Apply preventive measures',
                'Maintain good cultural practices'
            ]
        
        return schedule
    
    def get_default_recommendations(self, crop_type: str) -> Dict:
        """
        Get default recommendations when specific disease data is not available
        """
        return {
            'primary_pesticides': ['Copper Hydroxide', 'Mancozeb'],
            'alternative_pesticides': ['Chlorothalonil'],
            'application_method': 'Foliar spray',
            'prevention_tips': [
                'Regular field monitoring',
                'Maintain plant hygiene',
                'Proper irrigation management',
                'Use disease-free planting material'
            ],
            'timing': [
                'Apply at first sign of disease',
                'Best time: Early morning or evening'
            ],
            'follow_up_schedule': [
                'Monitor weekly',
                'Repeat application as needed'
            ]
        }
    
    def get_pesticide_details(self, pesticide_name: str, crop_type: str) -> Dict:
        """
        Get detailed information about a specific pesticide
        """
        try:
            # Search through all diseases for the pesticide
            crop_data = self.pesticide_database.get(crop_type, {})
            
            for disease, data in crop_data.items():
                dosage_info = data.get('dosage_per_hectare', {})
                price_info = data.get('price_per_kg', {})
                
                if pesticide_name in dosage_info:
                    return {
                        'name': pesticide_name,
                        'dosage_per_hectare': dosage_info[pesticide_name],
                        'price_per_kg': price_info.get(pesticide_name, 0),
                        'application_method': data.get('application_method', 'Foliar spray'),
                        'safety_period': data.get('safety_period', 14),
                        'frequency': data.get('application_frequency', 'Every 10-14 days')
                    }
            
            return {}
            
        except Exception as e:
            logger.error(f"Error getting pesticide details: {str(e)}")
            return {}