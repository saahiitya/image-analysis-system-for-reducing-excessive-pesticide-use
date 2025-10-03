#!/bin/bash

# CropGuard AI Installation Script

echo "🌱 CropGuard AI Installation Script"
echo "=================================================="

# Check system requirements
echo "🔍 Checking system requirements..."

# Check Python version
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    echo "✅ Python $PYTHON_VERSION found"
else
    echo "❌ Python 3 is required but not installed."
    echo "Please install Python 3.8 or higher from https://python.org"
    exit 1
fi

# Check pip
if command -v pip3 &> /dev/null; then
    echo "✅ pip3 found"
elif command -v pip &> /dev/null; then
    echo "✅ pip found"
else
    echo "❌ pip is required but not installed."
    echo "Please install pip: python3 -m ensurepip --upgrade"
    exit 1
fi

# Create project structure
echo "📁 Creating project structure..."
mkdir -p backend/{models,api}
mkdir -p frontend/static/{css,js,images}
mkdir -p scripts
mkdir -p docs
mkdir -p tests
mkdir -p logs

echo "✅ Project structure created"

# Set up virtual environment (optional but recommended)
read -p "🐍 Create Python virtual environment? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv cropguard_env
    
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
        source cropguard_env/Scripts/activate
    else
        source cropguard_env/bin/activate
    fi
    
    echo "✅ Virtual environment created and activated"
    echo "💡 To activate later, run: source cropguard_env/bin/activate"
fi

# Install dependencies
echo "📦 Installing Python dependencies..."
cd backend
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    echo "Please check your internet connection and try again"
    exit 1
fi

cd ..

# Set permissions
echo "🔧 Setting file permissions..."
chmod +x scripts/*.sh

# Create configuration file
echo "⚙️ Creating configuration..."
if [ ! -f backend/config.py ]; then
    echo "❌ Configuration file missing. Please ensure all files are properly copied."
    exit 1
fi

echo "✅ Configuration ready"

# Final setup
echo "🎯 Final setup..."

# Test import
cd backend
python3 -c "
try:
    import main
    print('✅ Application imports successfully')
except Exception as e:
    print(f'❌ Import failed: {e}')
    exit(1)
"

if [ $? -ne 0 ]; then
    echo "❌ Installation verification failed"
    exit 1
fi

cd ..

echo "=================================================="
echo "🎉 CropGuard AI installed successfully!"
echo ""
echo "🚀 To start the application:"
echo "   ./scripts/start.sh"
echo ""
echo "🌐 The application will be available at:"
echo "   http://localhost:8000"
echo ""
echo "📖 API documentation will be available at:"
echo "   http://localhost:8000/docs"
echo ""
echo "📱 Features available:"
echo "   ✅ Camera integration for image capture"
echo "   ✅ AI-powered disease detection"
echo "   ✅ Pesticide recommendations with Indian pricing"
echo "   ✅ Weather integration"
echo "   ✅ Environmental impact tracking"
echo ""
echo "💡 For support, check the README.md file"
echo "=================================================="