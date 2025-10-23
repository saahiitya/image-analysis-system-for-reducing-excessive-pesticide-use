#!/bin/bash

# CropGuard AI Platform Startup Script

echo "🌱 Starting CropGuard AI Platform..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 14 or higher."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install Python dependencies
echo "📥 Installing Python dependencies..."
pip install -r requirements.txt

# Install Node.js dependencies
echo "📥 Installing Node.js dependencies..."
npm install

# Initialize database
echo "🗄️ Initializing database..."
cd backend
python database/init_db.py --with-samples
cd ..

# Create necessary directories
mkdir -p backend/data/uploads
mkdir -p backend/data/processed
mkdir -p backend/models/disease_detection
mkdir -p backend/models/pesticide_recommendation

echo "✅ Setup completed successfully!"
echo ""
echo "🚀 To start the application:"
echo "   1. Backend: cd backend && python main.py"
echo "   2. Frontend: npm start"
echo ""
echo "📖 Documentation: http://localhost:8000/docs"
echo "🌐 Application: http://localhost:3000"