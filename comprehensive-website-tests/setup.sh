#!/bin/bash

# Comprehensive Test Suite Setup Script
# =====================================

echo "🚀 Setting up Comprehensive Hackathon Website Test Suite"
echo "========================================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to print status
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check prerequisites
print_status "Checking prerequisites..."

if ! command_exists python3; then
    print_error "Python 3 is required but not installed."
    echo "Please install Python 3.8 or higher"
    exit 1
fi

if ! command_exists pip; then
    print_error "pip is required but not installed."
    echo "Please install pip"
    exit 1
fi

print_success "Prerequisites check passed"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    print_status "Creating virtual environment..."
    python3 -m venv venv
    print_success "Virtual environment created"
else
    print_warning "Virtual environment already exists"
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
print_status "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
print_status "Installing Python dependencies..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    print_success "Python dependencies installed"
else
    print_error "requirements.txt not found"
    exit 1
fi

# Install Playwright browsers
print_status "Installing Playwright browsers..."
playwright install

if [ $? -eq 0 ]; then
    print_success "Playwright browsers installed"
else
    print_warning "Playwright browser installation may have failed"
fi

# Create reports directory
print_status "Creating reports directory..."
mkdir -p reports
print_success "Reports directory created"

# Make scripts executable
print_status "Making scripts executable..."
chmod +x run_tests.py
print_success "Scripts made executable"

# Verify installation
print_status "Verifying installation..."

echo ""
echo "🧪 Running quick verification test..."
python3 -c "
import sys
import pytest
import playwright
from playwright.sync_api import Playwright
print(f'✅ Python {sys.version}')
print(f'✅ pytest {pytest.__version__}')
print(f'✅ Playwright {playwright.__version__}')
print('✅ All imports successful')
"

if [ $? -eq 0 ]; then
    print_success "Installation verification passed"
else
    print_error "Installation verification failed"
    exit 1
fi

echo ""
echo "========================================================"
echo -e "${GREEN}🎉 Setup completed successfully!${NC}"
echo "========================================================"
echo ""
echo "📋 Next Steps:"
echo "1. Ensure your hackathon website is running:"
echo "   - Frontend: http://localhost:5173"
echo "   - Backend:  http://localhost:3000"
echo ""
echo "2. Run the test suite:"
echo -e "   ${BLUE}./run_tests.py${NC}                    # Run all tests"
echo -e "   ${BLUE}./run_tests.py --quick${NC}            # Run quick smoke tests"
echo -e "   ${BLUE}./run_tests.py --headed${NC}           # Run with browser UI"
echo -e "   ${BLUE}./run_tests.py --test 'landing'${NC}   # Run specific tests"
echo ""
echo "3. View reports in the 'reports/' directory"
echo ""
echo "📚 For more options, see README.md or run:"
echo -e "   ${BLUE}./run_tests.py --help${NC}"
echo ""
echo "🚀 Happy testing!"
