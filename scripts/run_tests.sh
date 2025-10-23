#!/bin/bash

# CropGuard AI Platform Test Runner

echo "🧪 Running CropGuard AI Platform Tests..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✅ $2${NC}"
    else
        echo -e "${RED}❌ $2${NC}"
    fi
}

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}⚠️ Virtual environment not found. Creating one...${NC}"
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install test dependencies
echo "📦 Installing test dependencies..."
pip install pytest pytest-asyncio httpx pillow

# Run backend tests
echo ""
echo "🔬 Running Backend Tests..."
cd backend
python -m pytest tests/ -v
backend_exit_code=$?
cd ..

print_status $backend_exit_code "Backend Tests"

# Run frontend tests
echo ""
echo "🔬 Running Frontend Tests..."
npm test -- --coverage --watchAll=false
frontend_exit_code=$?

print_status $frontend_exit_code "Frontend Tests"

# Run linting
echo ""
echo "🔍 Running Code Quality Checks..."

# Python linting (if flake8 is available)
if command -v flake8 &> /dev/null; then
    echo "Checking Python code style..."
    flake8 backend/ --max-line-length=100 --exclude=venv,__pycache__
    python_lint_exit_code=$?
    print_status $python_lint_exit_code "Python Code Style"
else
    echo -e "${YELLOW}⚠️ flake8 not installed, skipping Python linting${NC}"
fi

# JavaScript linting
if [ -f "node_modules/.bin/eslint" ]; then
    echo "Checking JavaScript code style..."
    npm run lint 2>/dev/null || echo -e "${YELLOW}⚠️ ESLint not configured${NC}"
fi

# Summary
echo ""
echo "📊 Test Summary:"
echo "=================="

if [ $backend_exit_code -eq 0 ] && [ $frontend_exit_code -eq 0 ]; then
    echo -e "${GREEN}🎉 All tests passed!${NC}"
    exit 0
else
    echo -e "${RED}💥 Some tests failed.${NC}"
    echo "Backend tests: $([ $backend_exit_code -eq 0 ] && echo "PASSED" || echo "FAILED")"
    echo "Frontend tests: $([ $frontend_exit_code -eq 0 ] && echo "PASSED" || echo "FAILED")"
    exit 1
fi