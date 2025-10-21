#!/bin/bash
# LaptopTester Development Setup Script

echo "🚀 LaptopTester Development Environment Setup"
echo "============================================="
echo

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check Python version
check_python() {
    echo -e "${BLUE}[INFO]${NC} Checking Python installation..."
    
    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
    elif command -v python &> /dev/null; then
        PYTHON_CMD="python"
    else
        echo -e "${RED}[ERROR]${NC} Python is not installed. Please install Python 3.8+"
        exit 1
    fi
    
    PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
    echo -e "${GREEN}[OK]${NC} Found Python $PYTHON_VERSION"
    
    # Check if Python version is 3.8+
    if $PYTHON_CMD -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)" 2>/dev/null; then
        echo -e "${GREEN}[OK]${NC} Python version is compatible"
    else
        echo -e "${RED}[ERROR]${NC} Python 3.8+ is required. Found: $PYTHON_VERSION"
        exit 1
    fi
}

# Create virtual environment
setup_venv() {
    echo -e "${BLUE}[INFO]${NC} Setting up virtual environment..."
    
    if [ -d "venv" ]; then
        echo -e "${YELLOW}[WARN]${NC} Virtual environment already exists"
        read -p "Do you want to recreate it? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            rm -rf venv
        else
            echo -e "${BLUE}[INFO]${NC} Using existing virtual environment"
            return
        fi
    fi
    
    $PYTHON_CMD -m venv venv
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}[OK]${NC} Virtual environment created successfully"
    else
        echo -e "${RED}[ERROR]${NC} Failed to create virtual environment"
        exit 1
    fi
}

# Activate virtual environment
activate_venv() {
    echo -e "${BLUE}[INFO]${NC} Activating virtual environment..."
    
    if [ -f "venv/bin/activate" ]; then
        source venv/bin/activate
        echo -e "${GREEN}[OK]${NC} Virtual environment activated"
    else
        echo -e "${RED}[ERROR]${NC} Virtual environment not found"
        exit 1
    fi
}

# Install dependencies
install_deps() {
    echo -e "${BLUE}[INFO]${NC} Installing dependencies..."
    
    # Upgrade pip first
    pip install --upgrade pip
    
    # Install requirements
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}[OK]${NC} Dependencies installed successfully"
        else
            echo -e "${RED}[ERROR]${NC} Failed to install some dependencies"
            echo -e "${YELLOW}[WARN]${NC} You may need to install system packages for some libraries"
        fi
    else
        echo -e "${RED}[ERROR]${NC} requirements.txt not found"
        exit 1
    fi
}

# Setup development tools
setup_dev_tools() {
    echo -e "${BLUE}[INFO]${NC} Installing development tools..."
    
    pip install black flake8 pytest pytest-cov
    
    echo -e "${GREEN}[OK]${NC} Development tools installed"
}

# Create necessary directories
create_dirs() {
    echo -e "${BLUE}[INFO]${NC} Creating necessary directories..."
    
    mkdir -p logs
    mkdir -p exports
    mkdir -p temp
    
    echo -e "${GREEN}[OK]${NC} Directories created"
}

# Validate installation
validate_setup() {
    echo -e "${BLUE}[INFO]${NC} Validating installation..."
    
    $PYTHON_CMD -c "
import sys
try:
    import customtkinter
    import psutil
    import cv2
    import pygame
    import numpy
    print('✅ All core dependencies imported successfully')
except ImportError as e:
    print(f'❌ Missing dependency: {e}')
    sys.exit(1)
"
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}[OK]${NC} Installation validated successfully"
    else
        echo -e "${RED}[ERROR]${NC} Validation failed"
        exit 1
    fi
}

# Main setup process
main() {
    echo "Starting setup process..."
    echo
    
    check_python
    setup_venv
    activate_venv
    install_deps
    setup_dev_tools
    create_dirs
    validate_setup
    
    echo
    echo -e "${GREEN}🎉 Setup completed successfully!${NC}"
    echo
    echo "To start development:"
    echo "1. Activate virtual environment: source venv/bin/activate"
    echo "2. Run the application: python laptoptester.py"
    echo "3. Run tests: pytest"
    echo "4. Format code: black laptoptester.py"
    echo "5. Lint code: flake8 laptoptester.py"
    echo
    echo "Happy coding! 🚀"
}

# Run main function
main