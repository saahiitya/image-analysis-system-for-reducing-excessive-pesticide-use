#!/usr/bin/env python3
"""
Model Setup Script for CropGuard AI
This script helps you set up your trained model with the platform
"""

import os
import sys
import shutil
from pathlib import Path

def create_model_directory():
    """Create the models directory structure"""
    model_dir = Path("models/crop_disease_model")
    model_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"✅ Created model directory: {model_dir}")
    return model_dir

def create_class_names_template(model_dir):
    """Create a template class_names.txt file"""
    class_names_file = model_dir / "class_names.txt"
    
    if not class_names_file.exists():
        default_classes = [
            "healthy",
            "tomato_early_blight",
            "tomato_late_blight", 
            "tomato_bacterial_wilt",
            "brinjal_fruit_borer",
            "brinjal_little_leaf",
            "brinjal_damping_off",
            "capsicum_anthracnose",
            "capsicum_powdery_mildew",
            "capsicum_thrips"
        ]
        
        with open(class_names_file, 'w') as f:
            for class_name in default_classes:
                f.write(f"{class_name}\n")
        
        print(f"✅ Created template class names file: {class_names_file}")
        print("📝 Please update this file with your actual model classes")
    else:
        print(f"ℹ️ Class names file already exists: {class_names_file}")

def create_model_readme(model_dir):
    """Create a README template for model documentation"""
    readme_file = model_dir / "README.md"
    
    if not readme_file.exists():
        readme_content = """# Crop Disease Detection Model

## Model Information
- **Framework:** [TensorFlow/PyTorch/Scikit-learn]
- **Architecture:** [Model architecture]
- **Input Size:** [e.g., 224x224x3]
- **Output Classes:** [Number of classes]
- **Training Dataset:** [Dataset information]

## Files
- `model.[h5/pt/pkl]` - The trained model file
- `class_names.txt` - List of output class names
- `README.md` - This documentation

## Performance
- **Accuracy:** [XX.X%]
- **Validation Loss:** [X.XXX]
- **Training Date:** [YYYY-MM-DD]

## Usage Notes
- Input images should be preprocessed to match training data
- Model expects RGB images
- Confidence threshold: 0.7 (configurable)

## Integration Status
- [ ] Model file placed in directory
- [ ] Class names updated
- [ ] Preprocessing configured
- [ ] Prediction method updated
- [ ] Testing completed
"""
        
        with open(readme_file, 'w') as f:
            f.write(readme_content)
        
        print(f"✅ Created model README: {readme_file}")
    else:
        print(f"ℹ️ Model README already exists: {readme_file}")

def check_model_files(model_dir):
    """Check for existing model files"""
    model_extensions = ['.h5', '.pt', '.pth', '.pkl', '.joblib']
    model_files = []
    
    for ext in model_extensions:
        files = list(model_dir.glob(f"*{ext}"))
        model_files.extend(files)
    
    # Also check for saved_model directory (TensorFlow)
    saved_model_dir = model_dir / "saved_model"
    if saved_model_dir.exists() and saved_model_dir.is_dir():
        model_files.append(saved_model_dir)
    
    if model_files:
        print(f"✅ Found model files:")
        for file in model_files:
            print(f"   - {file}")
    else:
        print("⚠️ No model files found. Please copy your trained model to:")
        print(f"   {model_dir}/")
        print("   Supported formats: .h5, .pt, .pth, .pkl, saved_model/")
    
    return len(model_files) > 0

def update_ai_engine_template():
    """Show instructions for updating the AI engine"""
    print("\n🔧 Next Steps - Update AI Engine:")
    print("1. Edit backend/models/ai_engine.py")
    print("2. Uncomment the import for your ML framework:")
    print("   - TensorFlow: import tensorflow as tf")
    print("   - PyTorch: import torch") 
    print("   - Scikit-learn: import joblib")
    print("3. Update the load_model() method")
    print("4. Update the predict_with_model() method")
    print("5. Adjust preprocessing in preprocess_image() method")
    print("\n📖 See MODEL_INTEGRATION_GUIDE.md for detailed instructions")

def test_integration():
    """Test if the model integration is working"""
    print("\n🧪 Testing Model Integration...")
    
    try:
        # Try to import and initialize the detector
        sys.path.append('backend')
        from backend.models.ai_engine import CropDiseaseDetector
        
        detector = CropDiseaseDetector()
        
        if detector.model_loaded:
            print("✅ Model loaded successfully!")
            print(f"   Classes: {len(detector.class_names)}")
            print(f"   Confidence threshold: {detector.confidence_threshold}")
            
            # Test with a dummy image
            from PIL import Image
            import io
            
            img = Image.new('RGB', (224, 224), color='green')
            img_bytes = io.BytesIO()
            img.save(img_bytes, format='JPEG')
            img_data = img_bytes.getvalue()
            
            result = detector.detect_disease(img_data, 'tomato')
            print(f"✅ Test prediction successful!")
            print(f"   Result: {result.get('disease_name', 'Unknown')}")
            print(f"   Confidence: {result.get('confidence', 0):.3f}")
            
        else:
            print("⚠️ Model not loaded. Please check:")
            print("   1. Model files are in the correct location")
            print("   2. AI engine is properly configured")
            print("   3. Dependencies are installed")
            
    except Exception as e:
        print(f"❌ Integration test failed: {str(e)}")
        print("Please check the MODEL_INTEGRATION_GUIDE.md for troubleshooting")

def main():
    """Main setup function"""
    print("🌱 CropGuard AI - Model Setup Script")
    print("=" * 50)
    
    # Create directory structure
    model_dir = create_model_directory()
    
    # Create template files
    create_class_names_template(model_dir)
    create_model_readme(model_dir)
    
    # Check for model files
    has_model = check_model_files(model_dir)
    
    # Show next steps
    if not has_model:
        print("\n📋 Setup Checklist:")
        print("1. ✅ Model directory created")
        print("2. ⏳ Copy your trained model file to models/crop_disease_model/")
        print("3. ⏳ Update class_names.txt with your model's classes")
        print("4. ⏳ Configure AI engine for your model framework")
        print("5. ⏳ Test the integration")
        
        update_ai_engine_template()
    else:
        print("\n📋 Setup Status:")
        print("1. ✅ Model directory created")
        print("2. ✅ Model files found")
        print("3. ✅ Template files created")
        print("4. ⏳ Configure AI engine (see MODEL_INTEGRATION_GUIDE.md)")
        print("5. ⏳ Test the integration")
        
        # Test the integration
        test_integration()
    
    print("\n" + "=" * 50)
    print("🚀 Setup complete! Check MODEL_INTEGRATION_GUIDE.md for detailed instructions.")

if __name__ == "__main__":
    main()