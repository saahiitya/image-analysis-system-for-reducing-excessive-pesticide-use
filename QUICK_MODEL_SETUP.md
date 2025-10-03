# 🚀 Quick Model Integration - CropGuard AI

## 📋 5-Minute Setup Checklist

### Step 1: Run Setup Script
```bash
python3 setup_model.py
```

### Step 2: Add Your Model Files
Copy your trained model to:
```
models/crop_disease_model/
├── model.h5        # (TensorFlow/Keras)
├── model.pt        # (PyTorch) 
├── model.pkl       # (Scikit-learn)
└── class_names.txt # Your model's output classes
```

### Step 3: Update Class Names
Edit `models/crop_disease_model/class_names.txt` with your model's actual classes:
```
healthy
tomato_early_blight
tomato_late_blight
brinjal_fruit_borer
capsicum_thrips
# ... your other classes
```

### Step 4: Configure AI Engine
Edit `backend/models/ai_engine.py`:

#### For TensorFlow/Keras:
```python
# Line 13: Uncomment
import tensorflow as tf

# Line 51: Uncomment  
self.model = tf.keras.models.load_model(model_path)

# Line 141: Uncomment
predictions = self.model.predict(preprocessed_image)
confidence_scores = predictions[0]
```

#### For PyTorch:
```python
# Line 14: Uncomment
import torch

# Line 54: Uncomment
self.model = torch.load(model_path, map_location='cpu')
self.model.eval()

# Line 145: Uncomment
with torch.no_grad():
    input_tensor = torch.FloatTensor(preprocessed_image)
    predictions = self.model(input_tensor)
    confidence_scores = torch.nn.functional.softmax(predictions, dim=1)[0].numpy()
```

#### For Scikit-learn:
```python
# Line 15: Uncomment
import joblib

# Line 57: Uncomment
self.model = joblib.load(model_path)

# Line 151: Uncomment
flattened_image = preprocessed_image.reshape(1, -1)
predictions = self.model.predict_proba(flattened_image)
confidence_scores = predictions[0]
```

### Step 5: Update Preprocessing (if needed)
In `preprocess_image` method, adjust normalization to match your training:

```python
# For ImageNet preprocessing:
image_array = image_array / 255.0
mean = np.array([0.485, 0.456, 0.406])
std = np.array([0.229, 0.224, 0.225])
image_array = (image_array - mean) / std

# For simple 0-1 normalization:
image_array = image_array.astype(np.float32) / 255.0
```

### Step 6: Remove Placeholder Code
In `predict_with_model` method, **remove this line**:
```python
# DELETE THIS LINE:
confidence_scores = np.random.dirichlet(np.ones(len(self.class_names)))
```

### Step 7: Test Integration
```bash
cd backend
python3 -c "
from models.ai_engine import detector
print('Model loaded:', detector.model_loaded)
print('Classes:', detector.class_names)
"
```

### Step 8: Start the Application
```bash
./scripts/start.sh
```

## 🎯 That's It!

Your trained model is now integrated with CropGuard AI! 

- **Web Interface:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs
- **Test API:** `python3 scripts/demo.py`

## 🔧 Common Issues

**Model not loading?**
- Check file paths and permissions
- Verify model file format
- Install required dependencies

**Wrong predictions?**
- Update class_names.txt
- Check preprocessing normalization
- Verify input image size

**Need help?** Check `MODEL_INTEGRATION_GUIDE.md` for detailed instructions.

---

**Your AI model is now powering precision agriculture! 🌱🤖**