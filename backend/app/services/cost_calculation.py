"""
Cost Calculation Service for pesticide treatments
"""

import logging
from typing import Dict, List, Optional
import math

logger = logging.getLogger(__name__)

class CostCalculationService:
    """
    Service for calculating pesticide costs and dosages based on farm size and disease severity
    """
    
    def __init__(self):
        self.pesticide_prices = {}
        self.load_pricing_data()
    
    def load_pricing_data(self):
        """
        Load pesticide pricing and dosage data
        """
        self.pesticide_prices = {
            'Copper Hydroxide': {
                'price_per_kg': 450,
                'dosage_per_hectare': 2.5,
                'water_ratio': 500,  # liters of water per kg
                'coverage_per_liter': 0.1  # hectares per liter of spray solution
            },
            'Streptomycin': {
                'price_per_kg': 1200,
                'dosage_per_hectare': 0.5,
                'water_ratio': 800,
                'coverage_per_liter': 0.1
            },
            'Mancozeb': {
                'price_per_kg': 520,
                'dosage_per_hectare': 2.5,
                'water_ratio': 400,
                'coverage_per_liter': 0.1
            },
            'Chlorothalonil': {
                'price_per_kg': 680,
                'dosage_per_hectare': 2.0,
                'water_ratio': 500,
                'coverage_per_liter': 0.1
            },
            'Metalaxyl': {
                'price_per_kg': 950,
                'dosage_per_hectare': 1.5,
                'water_ratio': 600,
                'coverage_per_liter': 0.1
            },
            'Copper Sulfate': {
                'price_per_kg': 380,
                'dosage_per_hectare': 3.0,
                'water_ratio': 400,
                'coverage_per_liter': 0.1
            },
            'Carbendazim': {
                'price_per_kg': 850,
                'dosage_per_hectare': 1.0,
                'water_ratio': 600,
                'coverage_per_liter': 0.1
            },
            'Propiconazole': {
                'price_per_kg': 1500,
                'dosage_per_hectare': 0.5,
                'water_ratio': 800,
                'coverage_per_liter': 0.1
            },
            'Sulfur': {
                'price_per_kg': 200,
                'dosage_per_hectare': 3.0,
                'water_ratio': 300,
                'coverage_per_liter': 0.1
            },
            'Cymoxanil': {
                'price_per_kg': 1200,
                'dosage_per_hectare': 0.5,
                'water_ratio': 700,
                'coverage_per_liter': 0.1
            },
            'Fosetyl-Al': {
                'price_per_kg': 780,
                'dosage_per_hectare': 2.5,
                'water_ratio': 500,
                'coverage_per_liter': 0.1
            },
            'Triadimefon': {
                'price_per_kg': 2000,
                'dosage_per_hectare': 0.25,
                'water_ratio': 1000,
                'coverage_per_liter': 0.1
            },
            'Metalaxyl + Mancozeb': {
                'price_per_kg': 850,
                'dosage_per_hectare': 2.0,
                'water_ratio': 500,
                'coverage_per_liter': 0.1
            },
            'Bleaching Powder': {
                'price_per_kg': 150,
                'dosage_per_hectare': 10.0,
                'water_ratio': 100,
                'coverage_per_liter': 0.1
            }
        }
        
        # Regional price variations (multipliers)
        self.regional_multipliers = {
            'north': 1.0,
            'south': 1.1,
            'east': 0.95,
            'west': 1.05,
            'central': 1.0,
            'default': 1.0
        }
        
        logger.info("Cost calculation data loaded successfully")
    
    async def calculate_treatment_cost(
        self,
        pesticides: List[str],
        farm_size: float,
        severity: str,
        location: str = ""
    ) -> Dict:
        """
        Calculate the total cost and dosage for pesticide treatment
        
        Args:
            pesticides: List of recommended pesticides
            farm_size: Size of farm in hectares
            severity: Disease severity (mild, moderate, severe)
            location: Farm location for regional pricing
            
        Returns:
            Dictionary containing cost calculations and recommendations
        """
        try:
            if not pesticides:
                return self.get_default_cost_calculation(farm_size)
            
            # Use primary pesticide for main calculation
            primary_pesticide = pesticides[0]
            
            # Get pesticide data
            pesticide_data = self.pesticide_prices.get(primary_pesticide)
            if not pesticide_data:
                return self.get_default_cost_calculation(farm_size)
            
            # Calculate base dosage
            base_dosage_per_hectare = pesticide_data['dosage_per_hectare']
            
            # Adjust dosage based on severity
            severity_multiplier = self.get_severity_multiplier(severity)
            adjusted_dosage_per_hectare = base_dosage_per_hectare * severity_multiplier
            
            # Calculate total amount needed
            total_amount_kg = adjusted_dosage_per_hectare * farm_size
            
            # Get regional price
            regional_multiplier = self.get_regional_multiplier(location)
            price_per_kg = pesticide_data['price_per_kg'] * regional_multiplier
            
            # Calculate total cost
            total_cost = total_amount_kg * price_per_kg
            
            # Calculate water requirements
            water_per_kg = pesticide_data['water_ratio']
            total_water_needed = total_amount_kg * water_per_kg
            
            # Calculate application details
            applications_needed = self.get_applications_needed(severity)
            cost_per_application = total_cost / applications_needed
            
            # Calculate savings compared to excessive use
            traditional_usage_multiplier = 1.5  # Farmers often use 50% more than needed
            potential_savings = total_cost * (traditional_usage_multiplier - 1)
            
            # Environmental impact calculations
            reduced_pesticide = total_amount_kg * (traditional_usage_multiplier - 1)
            
            return {
                'pesticide_name': primary_pesticide,
                'amount_per_hectare': f"{adjusted_dosage_per_hectare:.2f} kg/ha",
                'total_amount_needed': f"{total_amount_kg:.2f} kg",
                'cost_per_liter': f"₹{price_per_kg:.2f}/kg",
                'cost_estimate': f"₹{total_cost:.2f}",
                'water_needed': f"{total_water_needed:.0f} L",
                'applications_needed': applications_needed,
                'cost_per_application': f"₹{cost_per_application:.2f}",
                'potential_savings': f"₹{potential_savings:.2f}",
                'reduction_percentage': round(((traditional_usage_multiplier - 1) / traditional_usage_multiplier) * 100, 1),
                'environmental_benefit': f"{reduced_pesticide:.2f} kg pesticide saved",
                'application_instructions': self.get_application_instructions(
                    primary_pesticide, adjusted_dosage_per_hectare, water_per_kg
                ),
                'cost_breakdown': self.get_cost_breakdown(
                    primary_pesticide, total_amount_kg, price_per_kg, applications_needed
                )
            }
            
        except Exception as e:
            logger.error(f"Error calculating treatment cost: {str(e)}")
            return self.get_default_cost_calculation(farm_size)
    
    def get_severity_multiplier(self, severity: str) -> float:
        """
        Get dosage multiplier based on disease severity
        """
        multipliers = {
            'mild': 0.8,      # Reduce dosage for mild infections
            'moderate': 1.0,   # Standard dosage
            'severe': 1.3,     # Increase dosage for severe infections
            'healthy': 0.0     # No treatment needed
        }
        
        return multipliers.get(severity.lower(), 1.0)
    
    def get_regional_multiplier(self, location: str) -> float:
        """
        Get price multiplier based on location
        """
        if not location:
            return self.regional_multipliers['default']
        
        location_lower = location.lower()
        
        # Simple region detection based on location string
        if any(state in location_lower for state in ['punjab', 'haryana', 'delhi', 'rajasthan', 'up', 'uttarakhand']):
            return self.regional_multipliers['north']
        elif any(state in location_lower for state in ['karnataka', 'tamil nadu', 'kerala', 'andhra', 'telangana']):
            return self.regional_multipliers['south']
        elif any(state in location_lower for state in ['west bengal', 'odisha', 'bihar', 'jharkhand', 'assam']):
            return self.regional_multipliers['east']
        elif any(state in location_lower for state in ['maharashtra', 'gujarat', 'goa', 'rajasthan']):
            return self.regional_multipliers['west']
        else:
            return self.regional_multipliers['central']
    
    def get_applications_needed(self, severity: str) -> int:
        """
        Get number of applications needed based on severity
        """
        applications = {
            'mild': 2,
            'moderate': 3,
            'severe': 4,
            'healthy': 0
        }
        
        return applications.get(severity.lower(), 3)
    
    def get_application_instructions(self, pesticide: str, dosage: float, water_ratio: float) -> str:
        """
        Get detailed application instructions
        """
        instructions = f"""
        Application Instructions for {pesticide}:
        
        1. Dosage: {dosage:.2f} kg per hectare
        2. Water: Mix with {water_ratio} liters of water per kg of pesticide
        3. Spray volume: 400-500 liters per hectare
        4. Nozzle: Use flat fan nozzle for uniform coverage
        5. Timing: Apply during early morning (6-10 AM) or evening (4-7 PM)
        6. Weather: Avoid application during windy or rainy conditions
        7. Safety: Wear protective equipment during application
        8. Re-entry: Wait 24 hours before entering treated area
        """
        
        return instructions.strip()
    
    def get_cost_breakdown(self, pesticide: str, amount: float, price_per_kg: float, applications: int) -> Dict:
        """
        Get detailed cost breakdown
        """
        total_cost = amount * price_per_kg
        
        return {
            'pesticide_cost': f"₹{total_cost:.2f}",
            'amount_needed': f"{amount:.2f} kg",
            'price_per_kg': f"₹{price_per_kg:.2f}",
            'applications': applications,
            'cost_per_application': f"₹{total_cost/applications:.2f}",
            'additional_costs': {
                'labor': f"₹{applications * 500:.2f}",  # Estimated labor cost
                'fuel': f"₹{applications * 200:.2f}",   # Estimated fuel cost
                'equipment': f"₹{applications * 100:.2f}"  # Equipment wear
            },
            'total_treatment_cost': f"₹{total_cost + (applications * 800):.2f}"
        }
    
    def get_default_cost_calculation(self, farm_size: float) -> Dict:
        """
        Get default cost calculation when specific data is not available
        """
        # Use Copper Hydroxide as default
        default_pesticide = 'Copper Hydroxide'
        default_data = self.pesticide_prices[default_pesticide]
        
        dosage = default_data['dosage_per_hectare'] * farm_size
        cost = dosage * default_data['price_per_kg']
        water = dosage * default_data['water_ratio']
        
        return {
            'pesticide_name': default_pesticide,
            'amount_per_hectare': f"{default_data['dosage_per_hectare']:.2f} kg/ha",
            'total_amount_needed': f"{dosage:.2f} kg",
            'cost_per_liter': f"₹{default_data['price_per_kg']:.2f}/kg",
            'cost_estimate': f"₹{cost:.2f}",
            'water_needed': f"{water:.0f} L",
            'applications_needed': 3,
            'cost_per_application': f"₹{cost/3:.2f}",
            'potential_savings': f"₹{cost * 0.3:.2f}",
            'reduction_percentage': 30.0,
            'environmental_benefit': f"{dosage * 0.3:.2f} kg pesticide saved",
            'application_instructions': self.get_application_instructions(
                default_pesticide, default_data['dosage_per_hectare'], default_data['water_ratio']
            ),
            'cost_breakdown': self.get_cost_breakdown(
                default_pesticide, dosage, default_data['price_per_kg'], 3
            )
        }
    
    def calculate_seasonal_cost(self, crop_type: str, farm_size: float, location: str = "") -> Dict:
        """
        Calculate estimated seasonal pesticide costs for planning
        """
        try:
            # Estimate seasonal treatments based on crop type
            seasonal_treatments = {
                'tomato': 6,      # Tomatoes need frequent treatments
                'brinjal': 4,     # Moderate treatment frequency
                'capsicum': 5     # Regular treatments needed
            }
            
            treatments_per_season = seasonal_treatments.get(crop_type, 5)
            
            # Use average pesticide cost
            avg_cost_per_kg = 600  # Average pesticide cost
            avg_dosage_per_hectare = 2.0  # Average dosage
            
            regional_multiplier = self.get_regional_multiplier(location)
            
            seasonal_pesticide_amount = avg_dosage_per_hectare * farm_size * treatments_per_season
            seasonal_cost = seasonal_pesticide_amount * avg_cost_per_kg * regional_multiplier
            
            # Add other costs
            labor_cost = treatments_per_season * 500 * farm_size
            fuel_cost = treatments_per_season * 200 * farm_size
            equipment_cost = treatments_per_season * 100 * farm_size
            
            total_seasonal_cost = seasonal_cost + labor_cost + fuel_cost + equipment_cost
            
            return {
                'crop_type': crop_type,
                'farm_size': f"{farm_size} hectares",
                'treatments_per_season': treatments_per_season,
                'pesticide_cost': f"₹{seasonal_cost:.2f}",
                'labor_cost': f"₹{labor_cost:.2f}",
                'fuel_cost': f"₹{fuel_cost:.2f}",
                'equipment_cost': f"₹{equipment_cost:.2f}",
                'total_seasonal_cost': f"₹{total_seasonal_cost:.2f}",
                'cost_per_hectare': f"₹{total_seasonal_cost/farm_size:.2f}/ha",
                'monthly_average': f"₹{total_seasonal_cost/6:.2f}/month"
            }
            
        except Exception as e:
            logger.error(f"Error calculating seasonal cost: {str(e)}")
            return {}
    
    def compare_pesticide_costs(self, pesticides: List[str], farm_size: float) -> List[Dict]:
        """
        Compare costs of different pesticide options
        """
        try:
            comparisons = []
            
            for pesticide in pesticides:
                if pesticide in self.pesticide_prices:
                    data = self.pesticide_prices[pesticide]
                    
                    amount_needed = data['dosage_per_hectare'] * farm_size
                    cost = amount_needed * data['price_per_kg']
                    
                    comparisons.append({
                        'pesticide': pesticide,
                        'amount_needed': f"{amount_needed:.2f} kg",
                        'cost': f"₹{cost:.2f}",
                        'cost_per_hectare': f"₹{cost/farm_size:.2f}/ha",
                        'effectiveness_rating': self.get_effectiveness_rating(pesticide)
                    })
            
            # Sort by cost
            comparisons.sort(key=lambda x: float(x['cost'].replace('₹', '').replace(',', '')))
            
            return comparisons
            
        except Exception as e:
            logger.error(f"Error comparing pesticide costs: {str(e)}")
            return []
    
    def get_effectiveness_rating(self, pesticide: str) -> str:
        """
        Get effectiveness rating for pesticide (simplified)
        """
        ratings = {
            'Streptomycin': 'High',
            'Metalaxyl': 'High',
            'Propiconazole': 'High',
            'Chlorothalonil': 'Medium-High',
            'Mancozeb': 'Medium',
            'Copper Hydroxide': 'Medium',
            'Carbendazim': 'Medium',
            'Copper Sulfate': 'Medium-Low',
            'Sulfur': 'Low-Medium'
        }
        
        return ratings.get(pesticide, 'Medium')