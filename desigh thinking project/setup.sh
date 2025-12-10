#!/bin/bash
# ============================================================================
# Virtual AI LED Controller - Linux/Mac Setup Script
# ============================================================================
# This script automates the installation process for Linux and Mac users
# ============================================================================

echo ""
echo "============================================================================"
echo "   VIRTUAL AI LED CONTROLLER - SETUP SCRIPT"
echo "============================================================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Python is installed
echo "[1/5] Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}[ERROR]${NC} Python 3 is not installed!"
    echo ""
    echo "Please install Python 3.7 or higher:"
    echo "  Ubuntu/Debian: sudo apt install python3 python3-pip"
    echo "  Mac: brew install python3"
    echo "  or download from: https://www.python.org/downloads/"
    exit 1
fi

python3 --version
echo -e "${GREEN}[OK]${NC} Python found!"
echo ""

# Check Python version
echo "[2/5] Verifying Python version..."
if ! python3 -c "import sys; exit(0 if sys.version_info >= (3,7) else 1)" 2>/dev/null; then
    echo -e "${RED}[ERROR]${NC} Python 3.7 or higher is required!"
    python3 --version
    exit 1
fi
echo -e "${GREEN}[OK]${NC} Python version is compatible!"
echo ""

# Upgrade pip
echo "[3/5] Upgrading pip..."
python3 -m pip install --upgrade pip
if [ $? -eq 0 ]; then
    echo -e "${GREEN}[OK]${NC} pip upgraded!"
else
    echo -e "${YELLOW}[WARNING]${NC} Failed to upgrade pip, continuing anyway..."
fi
echo ""

# Install required packages
echo "[4/5] Installing required packages..."
echo "This may take a few minutes..."
echo ""

echo "Installing opencv-python..."
pip3 install opencv-python
if [ $? -ne 0 ]; then
    echo -e "${RED}[ERROR]${NC} Failed to install opencv-python!"
    exit 1
fi

echo "Installing mediapipe..."
pip3 install mediapipe
if [ $? -ne 0 ]; then
    echo -e "${RED}[ERROR]${NC} Failed to install mediapipe!"
    exit 1
fi

echo "Installing pyttsx3 (voice feedback)..."
pip3 install pyttsx3
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}[WARNING]${NC} Failed to install pyttsx3 - voice feedback will be disabled"
else
    echo -e "${GREEN}[OK]${NC} pyttsx3 installed!"
fi

echo ""
echo -e "${GREEN}[OK]${NC} All core packages installed successfully!"
echo ""

# Check for Tkinter (Linux only)
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Checking Tkinter installation (required for GUI)..."
    if ! python3 -c "import tkinter" 2>/dev/null; then
        echo -e "${YELLOW}[WARNING]${NC} Tkinter not found!"
        echo ""
        echo "Installing Tkinter..."
        if command -v apt-get &> /dev/null; then
            sudo apt-get install -y python3-tk
        elif command -v yum &> /dev/null; then
            sudo yum install -y python3-tkinter
        else
            echo -e "${RED}[ERROR]${NC} Could not install Tkinter automatically."
            echo "Please install manually: sudo apt-get install python3-tk"
        fi
    else
        echo -e "${GREEN}[OK]${NC} Tkinter is installed!"
    fi
    echo ""
fi

# Verify installation
echo "[5/5] Verifying installation..."
python3 -c "import cv2, mediapipe; print('[OK] OpenCV version:', cv2.__version__); print('[OK] MediaPipe version:', mediapipe.__version__)"
if [ $? -ne 0 ]; then
    echo -e "${RED}[ERROR]${NC} Package verification failed!"
    exit 1
fi
echo ""

# Test webcam
echo "Testing webcam access..."
python3 -c "import cv2; cap = cv2.VideoCapture(0); ret, _ = cap.read(); cap.release(); exit(0 if ret else 1)" 2>/dev/null
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}[WARNING]${NC} Could not access webcam!"
    echo "Please ensure:"
    echo "  - Webcam is connected"
    echo "  - No other application is using it"
    echo "  - Camera permissions are enabled"
    echo ""
else
    echo -e "${GREEN}[OK]${NC} Webcam access successful!"
    echo ""
fi

# Success message
echo "============================================================================"
echo "   INSTALLATION COMPLETE!"
echo "============================================================================"
echo ""
echo "Your Virtual AI LED Controller is ready to use!"
echo ""
echo "To run the application:"
echo "  python3 virtual_led_controller.py"
echo ""
echo "To run the demo (without webcam):"
echo "  python3 demo.py"
echo ""
echo "Documentation:"
echo "  README.md              - Full documentation"
echo "  QUICK_START.md         - Getting started guide"
echo "  CUSTOMIZATION_GUIDE.md - How to customize"
echo "  TROUBLESHOOTING.md     - Solutions to common issues"
echo ""
echo "============================================================================"
echo ""

# Ask if user wants to run the application
read -p "Would you like to run the application now? (y/n): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "Starting Virtual AI LED Controller..."
    echo "Press 'q' in the webcam window to exit."
    echo ""
    python3 virtual_led_controller.py
else
    echo ""
    echo "Setup complete! Run 'python3 virtual_led_controller.py' when ready."
fi
