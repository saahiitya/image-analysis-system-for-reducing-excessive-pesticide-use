# 🌱 CropGuard AI - Precision Pesticide Management Platform

An AI-powered precision pesticide management platform tailored for brinjal (eggplant), tomato, and capsicum crops. The system provides automated disease detection, pesticide recommendations, and cost calculations in Indian Rupees.

## 🌟 Features

### Core Functionality
- **AI-Powered Disease Detection**: Advanced image analysis for crop disease identification
- **Camera Integration**: Direct camera access for real-time image capture
- **Multi-Crop Support**: Specialized for tomato, brinjal, and capsicum
- **Precision Dosage Calculation**: Exact pesticide amounts based on affected area and severity
- **Cost Optimization**: Pricing in Indian Rupees with cost-effective recommendations

### Smart Agriculture Features
- **Real-time Weather Integration**: Weather-based spraying recommendations
- **Location Services**: GPS-based location tracking
- **Environmental Impact Tracking**: Monitor pesticide reduction and cost savings
- **Interactive Dashboard**: Real-time analytics and treatment progress

### Disease Coverage
#### Tomato
- Early Blight
- Late Blight  
- Bacterial Wilt

#### Brinjal (Eggplant)
- Fruit and Shoot Borer
- Little Leaf Disease
- Damping Off

#### Capsicum (Bell Pepper)
- Anthracnose
- Powdery Mildew
- Thrips

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Modern web browser with camera support

### Installation

1. **Run the installation script**
   ```bash
   chmod +x scripts/install.sh
   ./scripts/install.sh
   ```

2. **Or install manually**
   ```bash
   cd backend
   pip3 install -r requirements.txt
   ```

3. **Start the application**
   ```bash
   ./scripts/start.sh
   ```
   
   Or manually:
   ```bash
   cd backend
   python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

4. **Access the application**
   Open your browser and navigate to `http://localhost:8000`

## 💡 How to Use

### 1. Select Crop Type
Choose from Tomato, Brinjal, or Capsicum from the dropdown menu.

### 2. Set Farm Area
Enter your farm area in hectares for accurate pesticide calculations.

### 3. Capture/Upload Images
- **Camera Option**: Click "📹 Open Camera" to access device camera
- **Upload Option**: Drag and drop images or click to browse files
- **Multiple Images**: Upload multiple images for comprehensive analysis

### 4. Get Location & Weather
- Click "📍 Get Location" to set your current location
- Click "🌤 Update Weather" for current weather conditions and spraying recommendations

### 5. AI Analysis
Click "🤖 Analyze with AI" to process images and receive:
- Disease identification with confidence levels
- Severity assessment
- Pesticide recommendations with exact dosages
- Cost calculations in Indian Rupees
- Water requirements

## 🔬 Technical Architecture

### Backend (FastAPI)
- **Image Processing**: PIL and OpenCV for image handling
- **AI Model**: Mock implementation (ready for TensorFlow/PyTorch integration)
- **Disease Database**: Comprehensive pesticide database with Indian market prices
- **API Endpoints**: RESTful APIs for analysis, weather, and statistics

### Frontend (HTML/CSS/JavaScript)
- **Responsive Design**: Mobile-first approach with modern UI
- **Camera API**: WebRTC integration for device camera access
- **Real-time Updates**: Dynamic dashboard with live statistics
- **Interactive Elements**: Drag-and-drop, animations, and user feedback

### Key Components
- **Disease Detection Engine**: Simulated AI with confidence scoring
- **Pesticide Calculator**: Precise dosage and cost calculations
- **Weather Service**: Mock weather API with spraying recommendations
- **Statistics Tracker**: Real-time dashboard analytics

## 📊 Pesticide Database

The system includes comprehensive pesticide information:
- **Indian Market Prices**: Updated pricing in INR
- **Dosage Guidelines**: Crop-specific application rates
- **Severity-based Recommendations**: Different treatments for low/medium/high severity
- **Cost Optimization**: Multiple options with cost comparison

### Example Pesticides
- Mancozeb 75% WP - ₹180/kg
- Propiconazole 25% EC - ₹850/L  
- Imidacloprid 17.8% SL - ₹850/L
- Azoxystrobin 23% SC - ₹1200/L

## 🌍 Environmental Impact

The platform promotes sustainable farming by:
- **Precision Application**: Reducing unnecessary pesticide use
- **Cost Savings**: Optimizing input costs for farmers
- **Environmental Protection**: Minimizing chemical runoff
- **Data-Driven Decisions**: Evidence-based treatment recommendations

## 🔧 API Documentation

### Main Endpoints

#### POST /api/v1/analyze-crop
Analyze crop images and get disease detection with pesticide recommendations.

**Parameters:**
- `crop_type`: string (tomato, brinjal, capsicum)
- `area_hectares`: float (farm area)
- `files`: array of image files

**Response:**
```json
{
  "status": "success",
  "crop_type": "Tomato",
  "area_hectares": 1.5,
  "total_images": 2,
  "summary": {
    "healthy_count": 1,
    "diseased_count": 1,
    "health_percentage": 50.0
  },
  "results": [...]
}
```

#### GET /api/v1/weather
Get current weather conditions and spraying recommendations.

#### GET /api/v1/scan-history
Get scan history and dashboard statistics.

#### GET /api/v1/crops
Get list of supported crops and their diseases.

#### GET /api/v1/health
Health check endpoint.

## 🧪 Testing

### Run Demo Script
```bash
python3 scripts/demo.py
```

### Run Specific Tests
```bash
python3 scripts/demo.py --test health
python3 scripts/demo.py --test analysis
```

### Manual Testing
1. Open `http://localhost:8000`
2. Upload test images
3. Select crop type and area
4. Click "Analyze with AI"
5. Review results and recommendations

## 📱 Mobile Compatibility

The platform is fully responsive and mobile-optimized:
- **Touch-friendly Interface**: Large buttons and touch targets
- **Camera Access**: Rear camera preference on mobile devices
- **Responsive Layout**: Adapts to different screen sizes
- **Offline Capability**: Core functionality works without internet

## 🛡️ Security Features

- **Input Validation**: File type and size restrictions
- **CORS Configuration**: Secure cross-origin requests
- **Error Handling**: Graceful error management
- **Data Privacy**: No persistent storage of user images

## 🚀 Future Enhancements

### Planned Features
- **Real AI Integration**: Deploy trained disease detection models
- **Satellite Imagery**: Integration with satellite data sources
- **IoT Sensors**: Environmental sensor data integration
- **Multi-language Support**: Regional language interfaces
- **Offline Mode**: Local processing capabilities
- **Farmer Community**: Social features and knowledge sharing

### Advanced Analytics
- **Predictive Modeling**: Disease outbreak predictions
- **Yield Optimization**: Harvest forecasting
- **Market Integration**: Real-time pesticide pricing
- **Compliance Tracking**: Regulatory compliance monitoring

## 🔧 Customization

### Adding New Crops
1. Update `DISEASE_DATABASE` in `backend/models/disease_db.py`
2. Add crop option in HTML dropdown
3. Include crop-specific diseases and pesticides

### Integrating Real AI Models
Replace the mock AI engine in `backend/models/ai_engine.py` with:
- TensorFlow/PyTorch model loading
- Image preprocessing pipelines
- Model inference and post-processing

### Weather API Integration
Replace mock weather service in `backend/api/utils.py` with real APIs like:
- OpenWeatherMap
- AccuWeather
- Local meteorological services

## 📞 Support

For technical support or feature requests:
- Create an issue in the repository
- Contact the development team
- Check documentation for troubleshooting

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please read the contributing guidelines and submit pull requests for any improvements.

---

**CropGuard AI** - Empowering farmers with AI-driven precision agriculture for sustainable crop protection. 🌱