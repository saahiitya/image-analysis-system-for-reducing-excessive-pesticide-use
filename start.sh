#!/bin/bash

# CropGuard AI Startup Script

echo "🌱 Starting CropGuard AI - Precision Pesticide Management Platform"
echo "=================================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check if pip is installed
if ! command -v pip &> /dev/null && ! command -v pip3 &> /dev/null; then
    echo "❌ pip is not installed. Please install pip."
    exit 1
fi

# Install dependencies
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies. Please check your Python environment."
    exit 1
fi

echo "✅ Dependencies installed successfully!"

# Create static directory if it doesn't exist
mkdir -p static

echo "🚀 Starting the application..."
echo "📱 The application will be available at: http://localhost:8000"
echo "📸 Make sure to allow camera access for full functionality"
echo "=================================================="

# Start the FastAPI application
python3 main.py