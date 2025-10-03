"""
Disease and Pesticide Database for CropGuard AI
Contains comprehensive information about crop diseases and Indian pesticide recommendations
"""

DISEASE_DATABASE = {
    "tomato": {
        "early_blight": {
            "name": "Early Blight",
            "description": "Fungal disease causing dark spots on leaves",
            "symptoms": ["Dark spots on leaves", "Yellow halos around spots", "Leaf yellowing"],
            "severity_levels": {
                "low": {
                    "pesticides": [
                        {
                            "name": "Mancozeb 75% WP",
                            "dosage": "2-2.5g/L",
                            "cost_per_kg": 180,
                            "application_rate": "500-600L/hectare",
                            "active_ingredient": "Mancozeb",
                            "mode_of_action": "Protective fungicide"
                        },
                        {
                            "name": "Copper Oxychloride 50% WP",
                            "dosage": "2-3g/L",
                            "cost_per_kg": 120,
                            "application_rate": "500L/hectare",
                            "active_ingredient": "Copper Oxychloride",
                            "mode_of_action": "Contact fungicide"
                        }
                    ]
                },
                "medium": {
                    "pesticides": [
                        {
                            "name": "Propiconazole 25% EC",
                            "dosage": "1ml/L",
                            "cost_per_L": 850,
                            "application_rate": "600L/hectare",
                            "active_ingredient": "Propiconazole",
                            "mode_of_action": "Systemic fungicide"
                        },
                        {
                            "name": "Azoxystrobin 23% SC",
                            "dosage": "1ml/L",
                            "cost_per_L": 1200,
                            "application_rate": "500L/hectare",
                            "active_ingredient": "Azoxystrobin",
                            "mode_of_action": "Strobilurin fungicide"
                        }
                    ]
                },
                "high": {
                    "pesticides": [
                        {
                            "name": "Tebuconazole 25.9% EC",
                            "dosage": "1ml/L",
                            "cost_per_L": 950,
                            "application_rate": "600-700L/hectare",
                            "active_ingredient": "Tebuconazole",
                            "mode_of_action": "Systemic fungicide"
                        },
                        {
                            "name": "Difenoconazole 25% EC",
                            "dosage": "0.5ml/L",
                            "cost_per_L": 1100,
                            "application_rate": "600L/hectare",
                            "active_ingredient": "Difenoconazole",
                            "mode_of_action": "Systemic fungicide"
                        }
                    ]
                }
            }
        },
        "late_blight": {
            "name": "Late Blight",
            "description": "Serious fungal disease affecting leaves and fruits",
            "symptoms": ["Water-soaked lesions", "White fungal growth", "Fruit rot"],
            "severity_levels": {
                "low": {
                    "pesticides": [
                        {
                            "name": "Metalaxyl 8% + Mancozeb 64% WP",
                            "dosage": "2.5g/L",
                            "cost_per_kg": 320,
                            "application_rate": "500L/hectare",
                            "active_ingredient": "Metalaxyl + Mancozeb",
                            "mode_of_action": "Systemic + Contact"
                        }
                    ]
                },
                "medium": {
                    "pesticides": [
                        {
                            "name": "Cymoxanil 8% + Mancozeb 64% WP",
                            "dosage": "2g/L",
                            "cost_per_kg": 280,
                            "application_rate": "600L/hectare",
                            "active_ingredient": "Cymoxanil + Mancozeb",
                            "mode_of_action": "Systemic + Contact"
                        }
                    ]
                },
                "high": {
                    "pesticides": [
                        {
                            "name": "Dimethomorph 9% + Mancozeb 60% WP",
                            "dosage": "2g/L",
                            "cost_per_kg": 450,
                            "application_rate": "700L/hectare",
                            "active_ingredient": "Dimethomorph + Mancozeb",
                            "mode_of_action": "Systemic + Contact"
                        }
                    ]
                }
            }
        },
        "bacterial_wilt": {
            "name": "Bacterial Wilt",
            "description": "Bacterial infection causing plant wilting",
            "symptoms": ["Sudden wilting", "Vascular browning", "Plant death"],
            "severity_levels": {
                "low": {
                    "pesticides": [
                        {
                            "name": "Streptocycline 9% + Tetracycline 1% SP",
                            "dosage": "0.5g/L",
                            "cost_per_kg": 650,
                            "application_rate": "400L/hectare",
                            "active_ingredient": "Streptocycline + Tetracycline",
                            "mode_of_action": "Antibiotic"
                        }
                    ]
                },
                "medium": {
                    "pesticides": [
                        {
                            "name": "Copper Sulphate 25% WP",
                            "dosage": "2g/L",
                            "cost_per_kg": 150,
                            "application_rate": "500L/hectare",
                            "active_ingredient": "Copper Sulphate",
                            "mode_of_action": "Bactericide"
                        }
                    ]
                },
                "high": {
                    "pesticides": [
                        {
                            "name": "Kasugamycin 3% SL",
                            "dosage": "2ml/L",
                            "cost_per_L": 800,
                            "application_rate": "600L/hectare",
                            "active_ingredient": "Kasugamycin",
                            "mode_of_action": "Antibiotic fungicide"
                        }
                    ]
                }
            }
        }
    },
    "brinjal": {
        "fruit_borer": {
            "name": "Brinjal Fruit and Shoot Borer",
            "description": "Major pest causing fruit damage",
            "symptoms": ["Holes in fruits", "Shoot boring", "Larval presence"],
            "severity_levels": {
                "low": {
                    "pesticides": [
                        {
                            "name": "Bt (Bacillus thuringiensis)",
                            "dosage": "1-2g/L",
                            "cost_per_kg": 400,
                            "application_rate": "500L/hectare",
                            "active_ingredient": "Bacillus thuringiensis",
                            "mode_of_action": "Biological insecticide"
                        }
                    ]
                },
                "medium": {
                    "pesticides": [
                        {
                            "name": "Emamectin Benzoate 5% SG",
                            "dosage": "0.4g/L",
                            "cost_per_kg": 2200,
                            "application_rate": "500L/hectare",
                            "active_ingredient": "Emamectin Benzoate",
                            "mode_of_action": "Nerve poison"
                        }
                    ]
                },
                "high": {
                    "pesticides": [
                        {
                            "name": "Chlorantraniliprole 18.5% SC",
                            "dosage": "0.3ml/L",
                            "cost_per_L": 3200,
                            "application_rate": "600L/hectare",
                            "active_ingredient": "Chlorantraniliprole",
                            "mode_of_action": "Ryanodine receptor activator"
                        }
                    ]
                }
            }
        },
        "little_leaf": {
            "name": "Little Leaf Disease",
            "description": "Phytoplasma disease causing stunted growth",
            "symptoms": ["Small leaves", "Stunted growth", "Yellowing"],
            "severity_levels": {
                "low": {
                    "pesticides": [
                        {
                            "name": "Imidacloprid 17.8% SL",
                            "dosage": "0.5ml/L",
                            "cost_per_L": 850,
                            "application_rate": "400L/hectare",
                            "active_ingredient": "Imidacloprid",
                            "mode_of_action": "Neonicotinoid insecticide"
                        }
                    ]
                },
                "medium": {
                    "pesticides": [
                        {
                            "name": "Thiamethoxam 25% WG",
                            "dosage": "0.2g/L",
                            "cost_per_kg": 1800,
                            "application_rate": "500L/hectare",
                            "active_ingredient": "Thiamethoxam",
                            "mode_of_action": "Neonicotinoid insecticide"
                        }
                    ]
                },
                "high": {
                    "pesticides": [
                        {
                            "name": "Acetamiprid 20% SP",
                            "dosage": "0.2g/L",
                            "cost_per_kg": 1200,
                            "application_rate": "600L/hectare",
                            "active_ingredient": "Acetamiprid",
                            "mode_of_action": "Neonicotinoid insecticide"
                        }
                    ]
                }
            }
        },
        "damping_off": {
            "name": "Damping Off",
            "description": "Fungal disease affecting seedlings",
            "symptoms": ["Seedling collapse", "Root rot", "Stem lesions"],
            "severity_levels": {
                "low": {
                    "pesticides": [
                        {
                            "name": "Captan 70% + Hexaconazole 5% WP",
                            "dosage": "2g/L",
                            "cost_per_kg": 380,
                            "application_rate": "300L/hectare",
                            "active_ingredient": "Captan + Hexaconazole",
                            "mode_of_action": "Contact + Systemic fungicide"
                        }
                    ]
                },
                "medium": {
                    "pesticides": [
                        {
                            "name": "Carbendazim 12% + Mancozeb 63% WP",
                            "dosage": "2g/L",
                            "cost_per_kg": 220,
                            "application_rate": "400L/hectare",
                            "active_ingredient": "Carbendazim + Mancozeb",
                            "mode_of_action": "Systemic + Contact fungicide"
                        }
                    ]
                },
                "high": {
                    "pesticides": [
                        {
                            "name": "Fosetyl Aluminium 80% WP",
                            "dosage": "2.5g/L",
                            "cost_per_kg": 750,
                            "application_rate": "500L/hectare",
                            "active_ingredient": "Fosetyl Aluminium",
                            "mode_of_action": "Systemic fungicide"
                        }
                    ]
                }
            }
        }
    },
    "capsicum": {
        "anthracnose": {
            "name": "Anthracnose",
            "description": "Fungal disease causing fruit rot",
            "symptoms": ["Circular lesions", "Fruit rot", "Sunken spots"],
            "severity_levels": {
                "low": {
                    "pesticides": [
                        {
                            "name": "Mancozeb 75% WP",
                            "dosage": "2g/L",
                            "cost_per_kg": 180,
                            "application_rate": "500L/hectare",
                            "active_ingredient": "Mancozeb",
                            "mode_of_action": "Protective fungicide"
                        }
                    ]
                },
                "medium": {
                    "pesticides": [
                        {
                            "name": "Carbendazim 50% WP",
                            "dosage": "1g/L",
                            "cost_per_kg": 280,
                            "application_rate": "500L/hectare",
                            "active_ingredient": "Carbendazim",
                            "mode_of_action": "Systemic fungicide"
                        }
                    ]
                },
                "high": {
                    "pesticides": [
                        {
                            "name": "Azoxystrobin 23% SC",
                            "dosage": "1ml/L",
                            "cost_per_L": 1200,
                            "application_rate": "600L/hectare",
                            "active_ingredient": "Azoxystrobin",
                            "mode_of_action": "Strobilurin fungicide"
                        }
                    ]
                }
            }
        },
        "powdery_mildew": {
            "name": "Powdery Mildew",
            "description": "Fungal disease with white powdery growth",
            "symptoms": ["White powdery coating", "Leaf curling", "Stunted growth"],
            "severity_levels": {
                "low": {
                    "pesticides": [
                        {
                            "name": "Wettable Sulphur 80% WP",
                            "dosage": "2g/L",
                            "cost_per_kg": 120,
                            "application_rate": "400L/hectare",
                            "active_ingredient": "Sulphur",
                            "mode_of_action": "Contact fungicide"
                        }
                    ]
                },
                "medium": {
                    "pesticides": [
                        {
                            "name": "Triadimefon 25% WP",
                            "dosage": "1g/L",
                            "cost_per_kg": 450,
                            "application_rate": "500L/hectare",
                            "active_ingredient": "Triadimefon",
                            "mode_of_action": "Systemic fungicide"
                        }
                    ]
                },
                "high": {
                    "pesticides": [
                        {
                            "name": "Hexaconazole 5% EC",
                            "dosage": "2ml/L",
                            "cost_per_L": 680,
                            "application_rate": "600L/hectare",
                            "active_ingredient": "Hexaconazole",
                            "mode_of_action": "Systemic fungicide"
                        }
                    ]
                }
            }
        },
        "thrips": {
            "name": "Thrips",
            "description": "Insect pest causing leaf damage",
            "symptoms": ["Silver streaks on leaves", "Black spots", "Leaf curling"],
            "severity_levels": {
                "low": {
                    "pesticides": [
                        {
                            "name": "Fipronil 5% SC",
                            "dosage": "2ml/L",
                            "cost_per_L": 950,
                            "application_rate": "400L/hectare",
                            "active_ingredient": "Fipronil",
                            "mode_of_action": "Phenylpyrazole insecticide"
                        }
                    ]
                },
                "medium": {
                    "pesticides": [
                        {
                            "name": "Imidacloprid 17.8% SL",
                            "dosage": "0.5ml/L",
                            "cost_per_L": 850,
                            "application_rate": "500L/hectare",
                            "active_ingredient": "Imidacloprid",
                            "mode_of_action": "Neonicotinoid insecticide"
                        }
                    ]
                },
                "high": {
                    "pesticides": [
                        {
                            "name": "Spinosad 45% SC",
                            "dosage": "0.3ml/L",
                            "cost_per_L": 2800,
                            "application_rate": "600L/hectare",
                            "active_ingredient": "Spinosad",
                            "mode_of_action": "Biological insecticide"
                        }
                    ]
                }
            }
        }
    }
}

def get_disease_info(crop_type, disease_key):
    """Get disease information for a specific crop and disease"""
    return DISEASE_DATABASE.get(crop_type.lower(), {}).get(disease_key, None)

def get_all_diseases_for_crop(crop_type):
    """Get all diseases for a specific crop"""
    return list(DISEASE_DATABASE.get(crop_type.lower(), {}).keys())

def get_pesticide_recommendations(crop_type, disease_key, severity):
    """Get pesticide recommendations for specific disease and severity"""
    disease_info = get_disease_info(crop_type, disease_key)
    if disease_info:
        return disease_info.get("severity_levels", {}).get(severity, {}).get("pesticides", [])
    return []