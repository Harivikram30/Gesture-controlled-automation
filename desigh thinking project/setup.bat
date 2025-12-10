@echo off
REM ============================================================================
REM Virtual AI LED Controller - Windows Setup Script
REM ============================================================================
REM This script automates the installation process for Windows users
REM ============================================================================

echo.
echo ============================================================================
echo    VIRTUAL AI LED CONTROLLER - SETUP SCRIPT
echo ============================================================================
echo.

REM Check if Python is installed
echo [1/5] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH!
    echo.
    echo Please install Python 3.7 or higher from:
    echo https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation!
    pause
    exit /b 1
)

python --version
echo [OK] Python found!
echo.

REM Check Python version
echo [2/5] Verifying Python version...
python -c "import sys; exit(0 if sys.version_info >= (3,7) else 1)"
if errorlevel 1 (
    echo [ERROR] Python 3.7 or higher is required!
    python --version
    pause
    exit /b 1
)
echo [OK] Python version is compatible!
echo.

REM Upgrade pip
echo [3/5] Upgrading pip...
python -m pip install --upgrade pip
if errorlevel 1 (
    echo [WARNING] Failed to upgrade pip, continuing anyway...
) else (
    echo [OK] pip upgraded!
)
echo.

REM Install required packages
echo [4/5] Installing required packages...
echo This may take a few minutes...
echo.

echo Installing opencv-python...
pip install opencv-python
if errorlevel 1 (
    echo [ERROR] Failed to install opencv-python!
    pause
    exit /b 1
)

echo Installing mediapipe...
pip install mediapipe
if errorlevel 1 (
    echo [ERROR] Failed to install mediapipe!
    pause
    exit /b 1
)

echo Installing pyttsx3 (voice feedback)...
pip install pyttsx3
if errorlevel 1 (
    echo [WARNING] Failed to install pyttsx3 - voice feedback will be disabled
) else (
    echo [OK] pyttsx3 installed!
)

echo.
echo [OK] All core packages installed successfully!
echo.

REM Verify installation
echo [5/5] Verifying installation...
python -c "import cv2, mediapipe; print('[OK] OpenCV version:', cv2.__version__); print('[OK] MediaPipe version:', mediapipe.__version__)"
if errorlevel 1 (
    echo [ERROR] Package verification failed!
    pause
    exit /b 1
)
echo.

REM Test webcam
echo Testing webcam access...
python -c "import cv2; cap = cv2.VideoCapture(0); ret, _ = cap.read(); cap.release(); exit(0 if ret else 1)"
if errorlevel 1 (
    echo [WARNING] Could not access webcam!
    echo Please ensure:
    echo  - Webcam is connected
    echo  - No other application is using it
    echo  - Camera permissions are enabled
    echo.
) else (
    echo [OK] Webcam access successful!
    echo.
)

REM Success message
echo ============================================================================
echo    INSTALLATION COMPLETE!
echo ============================================================================
echo.
echo Your Virtual AI LED Controller is ready to use!
echo.
echo To run the application:
echo   python virtual_led_controller.py
echo.
echo To run the demo (without webcam):
echo   python demo.py
echo.
echo Documentation:
echo   README.md              - Full documentation
echo   QUICK_START.md         - Getting started guide
echo   CUSTOMIZATION_GUIDE.md - How to customize
echo   TROUBLESHOOTING.md     - Solutions to common issues
echo.
echo ============================================================================
echo.

REM Ask if user wants to run the application
set /p RUN_NOW="Would you like to run the application now? (Y/N): "
if /i "%RUN_NOW%"=="Y" (
    echo.
    echo Starting Virtual AI LED Controller...
    echo Press 'q' in the webcam window to exit.
    echo.
    python virtual_led_controller.py
) else (
    echo.
    echo Setup complete! Run 'python virtual_led_controller.py' when ready.
)

pause
