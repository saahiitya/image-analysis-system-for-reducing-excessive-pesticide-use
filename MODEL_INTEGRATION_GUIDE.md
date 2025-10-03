# 🤖 Model Integration Guide - CropGuard AI

This guide will help you integrate your trained crop disease detection model with the CropGuard AI platform.

## 📁 Model File Structure

Create the following directory structure in your project root:

```
models/
├── crop_disease_model/          # Your model files go here
│   ├── model.h5                # For Keras/TensorFlow models
│   ├── model.pt                # For PyTorch models  
│   ├── model.pkl               # For scikit-learn models
│   └── class_names.txt         # List of class names (one per line)
└── README.md                   # Model documentation
```

## 🔧 Integration Steps

### Step 1: Place Your Model Files

1. **Create the models directory:**
   ```bash
   mkdir -p models/crop_disease_model
   ```

2. **Copy your trained model files:**
   - Place your model file in `models/crop_disease_model/`
   - Name it according to your framework:
     - TensorFlow/Keras: `model.h5` or `saved_model/`
     - PyTorch: `model.pt` or `model.pth`
     - Scikit-learn: `model.pkl`

3. **Create class names file:**
   Create `models/crop_disease_model/class_names.txt` with your model's output classes:
   ```
   healthy
   tomato_early_blight
   tomato_late_blight
   tomato_bacterial_wilt
   brinjal_fruit_borer
   brinjal_little_leaf
   brinjal_damping_off
   capsicum_anthracnose
   capsicum_powdery_mildew
   capsicum_thrips
   ```

### Step 2: Configure Model Loading

Edit `backend/models/ai_engine.py` and update the `load_model` method:

#### For TensorFlow/Keras Models:
```python
# Uncomment these lines in ai_engine.py:
import tensorflow as tf

# In load_model method:
self.model = tf.keras.models.load_model(model_path)
```

#### For PyTorch Models:
```python
# Uncomment these lines in ai_engine.py:
import torch

# In load_model method:
self.model = torch.load(model_path, map_location='cpu')
self.model.eval()
```

#### For Scikit-learn Models:
```python
# Uncomment these lines in ai_engine.py:
import joblib

# In load_model method:
self.model = joblib.load(model_path)
```

### Step 3: Update Preprocessing

Modify the `preprocess_image` method to match your training preprocessing:

```python
def preprocess_image(self, image_data, target_size=(224, 224)):
    # Update target_size to match your model's input
    # Update normalization to match your training
    
    # Example for ImageNet preprocessing:
    image_array = image_array / 255.0
    mean = np.array([0.485, 0.456, 0.406])
    std = np.array([0.229, 0.224, 0.225])
    image_array = (image_array - mean) / std
```

### Step 4: Update Prediction Logic

Modify the `predict_with_model` method:

#### For TensorFlow/Keras:
```python
def predict_with_model(self, preprocessed_image):
    if len(preprocessed_image.shape) == 3:
        preprocessed_image = np.expand_dims(preprocessed_image, axis=0)
    
    predictions = self.model.predict(preprocessed_image)
    confidence_scores = predictions[0]  # Remove batch dimension
    
    return confidence_scores
```

#### For PyTorch:
```python
def predict_with_model(self, preprocessed_image):
    import torch
    
    if len(preprocessed_image.shape) == 3:
        preprocessed_image = np.expand_dims(preprocessed_image, axis=0)
    
    with torch.no_grad():
        input_tensor = torch.FloatTensor(preprocessed_image)
        predictions = self.model(input_tensor)
        confidence_scores = torch.nn.functional.softmax(predictions, dim=1)[0].numpy()
    
    return confidence_scores
```

### Step 5: Update Class Mapping

Update the `disease_mapping` in `_parse_disease_class` method to match your model's output classes:

```python
disease_mapping = {
    'your_model_class_1': {
        'disease': 'early_blight',
        'name': 'Early Blight',
        'description': 'Fungal disease causing dark spots on leaves'
    },
    # Add all your model's classes here
}
```

## 🧪 Testing Your Integration

### Step 1: Test Model Loading
```bash
cd backend
python3 -c "
from models.ai_engine import detector
print('Model loaded:', detector.model_loaded)
print('Classes:', detector.class_names)
"
```

### Step 2: Test with Sample Image
```bash
python3 -c "
from models.ai_engine import detect_disease_from_image
from PIL import Image
import io

# Create a test image
img = Image.new('RGB', (224, 224), color='green')
img_bytes = io.BytesIO()
img.save(img_bytes, format='JPEG')
img_data = img_bytes.getvalue()

# Test detection
result = detect_disease_from_image(img_data, 'tomato')
print('Detection result:', result)
"
```

### Step 3: Run Full Demo
```bash
python3 scripts/demo.py --test analysis
```

## 📊 Model Performance Monitoring

The system automatically logs:
- Model loading status
- Prediction confidence scores
- Processing times
- Error rates

Check logs in the console output when running the application.

## 🔧 Troubleshooting

### Common Issues:

1. **Model Not Loading**
   - Check file paths and permissions
   - Verify model file format
   - Check dependency versions

2. **Prediction Errors**
   - Verify input preprocessing matches training
   - Check model input/output shapes
   - Ensure class names are correct

3. **Low Confidence Scores**
   - Adjust `confidence_threshold` in config
   - Review image preprocessing
   - Check model performance on validation data

### Debug Mode:
Enable detailed logging by setting in `backend/config.py`:
```python
DEBUG_MODE = True
LOG_LEVEL = "DEBUG"
```

## 🚀 Production Deployment

### Performance Optimization:
1. **Model Optimization:**
   - Use TensorFlow Lite for mobile deployment
   - Quantize models for faster inference
   - Consider ONNX for cross-platform compatibility

2. **Caching:**
   - Enable result caching for repeated images
   - Cache model predictions

3. **Batch Processing:**
   - Process multiple images in batches
   - Use GPU acceleration if available

### Security:
- Validate all input images
- Implement rate limiting
- Monitor for adversarial inputs

## 📝 Model Documentation Template

Create `models/README.md`:

```markdown
# Crop Disease Detection Model

## Model Details
- **Framework:** TensorFlow/PyTorch/Scikit-learn
- **Architecture:** ResNet50/VGG16/Custom CNN
- **Input Size:** 224x224x3
- **Output Classes:** 10 (healthy + 9 diseases)
- **Training Dataset:** [Dataset name and size]
- **Accuracy:** XX.X% on validation set

## Training Details
- **Training Date:** YYYY-MM-DD
- **Training Duration:** X hours
- **Hardware Used:** GPU/CPU specifications
- **Preprocessing:** Normalization, augmentation details

## Performance Metrics
- **Accuracy:** XX.X%
- **Precision:** XX.X%
- **Recall:** XX.X%
- **F1-Score:** XX.X%

## Class Distribution
- healthy: XX%
- tomato_early_blight: XX%
- [etc...]
```

## 🤝 Support

If you encounter issues during integration:

1. Check the console logs for error messages
2. Verify your model works independently
3. Test with the provided demo scripts
4. Review the preprocessing pipeline

The platform is designed to gracefully handle model loading failures and will fall back to a safe mode if needed.

---

**Ready to integrate your model?** Follow these steps and your trained AI model will be powering the CropGuard AI platform! 🌱🤖