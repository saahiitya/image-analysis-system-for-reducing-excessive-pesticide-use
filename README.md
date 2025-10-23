# CropGuard AI Platform

A comprehensive AI-powered crop disease detection and pesticide management platform for sustainable agriculture. This platform helps farmers identify crop diseases, get precise pesticide recommendations, and manage their treatments efficiently while reducing environmental impact.

## 🌟 Features

### Core Functionality
- **AI-Powered Disease Detection**: Advanced machine learning models for identifying diseases in tomato, brinjal, and capsicum crops
- **Smart Pesticide Recommendations**: Intelligent suggestions for the most effective treatments based on disease type, severity, and environmental conditions
- **Precision Dosage Calculation**: Accurate pesticide dosage calculations based on farm size, disease severity, and location-specific factors
- **Cost Optimization**: Real-time cost calculations and savings analysis to help farmers make economical decisions
- **Weather Integration**: Weather-based spraying recommendations and alerts

### User Interface
- **Farmer Dashboard**: Comprehensive overview of farm health, treatment history, and analytics
- **Mobile-Responsive Design**: Optimized for field use on smartphones and tablets
- **Image Upload & Camera Capture**: Easy crop image submission through drag-and-drop or camera
- **Treatment Tracker**: Monitor and track all pesticide applications and their effectiveness
- **Historical Analytics**: Visualize trends in crop health, costs, and treatment success rates

### Environmental Impact
- **Pesticide Reduction Tracking**: Monitor and visualize reductions in pesticide usage
- **Sustainable Practices**: Promote eco-friendly farming through optimized treatments
- **Cost Savings Analysis**: Track financial benefits of precision agriculture

## 🏗️ Architecture

### Backend (FastAPI)
- **Disease Detection Service**: AI models for crop disease identification
- **Pesticide Recommendation Engine**: Smart treatment suggestions
- **Cost Calculation Service**: Precise dosage and cost analysis
- **Database Management**: SQLite database for data persistence
- **Weather API Integration**: Real-time weather data for spraying recommendations

### Frontend (React)
- **Dashboard Component**: Analytics and overview
- **Crop Scanner**: Image upload and analysis interface
- **Treatment Tracker**: Treatment management and history
- **Weather Widget**: Real-time weather information
- **Responsive Design**: Mobile-first approach

### Database Schema
- **Crop Scans**: Store scan results and analysis data
- **Disease Information**: Comprehensive disease database
- **Pesticide Data**: Treatment options and pricing
- **Treatment History**: Track applications and effectiveness
- **User Profiles**: Farmer information and preferences

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Node.js 14+
- npm or yarn

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd cropguard-ai-platform
   ```

2. **Backend Setup**
   ```bash
   # Install Python dependencies
   pip install -r requirements.txt
   
   # Set up environment variables
   cp .env.example .env
   # Edit .env with your configuration
   
   # Initialize the database
   cd backend
   python database/init_db.py --with-samples
   ```

3. **Frontend Setup**
   ```bash
   # Install Node.js dependencies
   npm install
   ```

### Running the Application

1. **Start the Backend Server**
   ```bash
   cd backend
   python main.py
   ```
   The API will be available at `http://localhost:8000`

2. **Start the Frontend Development Server**
   ```bash
   npm start
   ```
   The application will be available at `http://localhost:3000`

### API Documentation
Once the backend is running, visit `http://localhost:8000/docs` for interactive API documentation.

## 📱 Usage

### For Farmers

1. **Scan Your Crops**
   - Navigate to the "Scan Crops" tab
   - Upload an image or use your camera to capture crop photos
   - Select crop type and enter farm details
   - Get instant AI-powered disease analysis

2. **View Recommendations**
   - Receive detailed treatment recommendations
   - See precise dosage calculations
   - Get cost estimates and savings analysis
   - Access weather-based spraying advice

3. **Track Treatments**
   - Record pesticide applications
   - Monitor treatment effectiveness
   - View historical data and trends
   - Optimize future treatments

4. **Monitor Dashboard**
   - View farm health analytics
   - Track cost savings and pesticide reduction
   - Monitor weather conditions
   - Get smart recommendations

### Supported Crops
- **Tomato**: Early Blight, Late Blight, Bacterial Spot, Leaf Mold, Septoria Leaf Spot
- **Brinjal (Eggplant)**: Bacterial Wilt, Cercospora Leaf Spot, Damping Off
- **Capsicum (Bell Pepper)**: Bacterial Spot, Powdery Mildew, Anthracnose

## 🧪 AI Models

### Disease Detection
The platform uses deep learning models trained on thousands of crop images to identify diseases with high accuracy:
- **Convolutional Neural Networks (CNNs)** for image classification
- **Transfer Learning** from pre-trained models
- **Data Augmentation** for improved generalization
- **Confidence Scoring** for prediction reliability

### Pesticide Recommendation
Intelligent recommendation system considering:
- Disease type and severity
- Crop characteristics
- Environmental conditions
- Cost-effectiveness
- Environmental impact

### Cost Calculation
Precision agriculture algorithms for:
- Dosage optimization based on farm size
- Regional pricing variations
- Severity-adjusted treatments
- Environmental impact assessment

## 🌍 Environmental Impact

The platform promotes sustainable agriculture by:
- **Reducing Pesticide Usage**: Precision recommendations prevent overuse
- **Optimizing Applications**: Weather-based timing reduces waste
- **Tracking Savings**: Monitor environmental benefits
- **Education**: Promote best practices for sustainable farming

## 📊 Data Management

### Privacy & Security
- Local data storage with SQLite
- No sensitive data transmission
- User consent for data collection
- Secure API endpoints

### Data Analytics
- Treatment effectiveness tracking
- Cost-benefit analysis
- Seasonal trend analysis
- Comparative studies

## 🔧 Configuration

### Environment Variables
See `.env.example` for all available configuration options:
- Database settings
- API keys for weather services
- File upload limits
- Security settings

### Customization
- Add new crop types in the disease database
- Extend pesticide recommendations
- Customize regional pricing
- Add new weather providers

## 🧪 Testing

### Backend Tests
```bash
cd backend
python -m pytest tests/
```

### Frontend Tests
```bash
npm test
```

### Integration Tests
```bash
npm run test:integration
```

## 📈 Performance

### Optimization Features
- **Image Compression**: Automatic image optimization for faster uploads
- **Caching**: Intelligent caching for frequently accessed data
- **Lazy Loading**: Components load on demand
- **Database Indexing**: Optimized queries for large datasets

### Scalability
- **Microservices Architecture**: Easy to scale individual components
- **Database Migration Support**: Seamless upgrades
- **API Rate Limiting**: Prevent abuse and ensure stability
- **CDN Ready**: Static assets can be served from CDN

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

### Development Guidelines
- Follow PEP 8 for Python code
- Use ESLint for JavaScript code
- Write comprehensive tests
- Update documentation

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

### Documentation
- API Documentation: `http://localhost:8000/docs`
- User Guide: Available in the application
- Developer Guide: See `/docs` directory

### Community
- GitHub Issues: Report bugs and request features
- Discussions: Community support and ideas
- Email Support: support@cropguard-ai.com

## 🔮 Roadmap

### Upcoming Features
- **Mobile App**: Native iOS and Android applications
- **Satellite Integration**: Drone and satellite imagery analysis
- **IoT Sensors**: Integration with field sensors
- **Machine Learning**: Continuous model improvement
- **Multi-language**: Support for regional languages
- **Offline Mode**: Work without internet connectivity

### Advanced Analytics
- **Predictive Modeling**: Forecast disease outbreaks
- **Yield Prediction**: Estimate crop yields
- **Market Integration**: Price forecasting and market trends
- **Supply Chain**: Connect farmers with suppliers

## 🏆 Achievements

- **Sustainable Agriculture**: Promoting eco-friendly farming practices
- **Cost Reduction**: Helping farmers save on pesticide costs
- **Technology Access**: Making AI accessible to small-scale farmers
- **Environmental Protection**: Reducing chemical runoff and pollution

## 📞 Contact

- **Project Maintainer**: CropGuard AI Team
- **Email**: info@cropguard-ai.com
- **Website**: https://cropguard-ai.com
- **GitHub**: https://github.com/cropguard-ai/platform

---

**CropGuard AI Platform** - Empowering sustainable agriculture through artificial intelligence. 🌱🤖