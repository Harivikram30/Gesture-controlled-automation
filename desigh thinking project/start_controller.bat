@echo off
echo ====================================================================
echo    VIRTUAL GESTURE CONTROLLER - STARTUP
echo ====================================================================
echo.
echo IMPORTANT: First time loading takes 1-3 minutes
echo Please wait patiently while MediaPipe and TensorFlow initialize...
echo.
echo You will see TWO windows when ready:
echo   1. Webcam window (shows hand tracking)
echo   2. Device control panel (shows LED/Fan/Lock/TV status)
echo.
echo Press 'q' in the webcam window to quit
echo ====================================================================
echo.
python virtual_led_controller.py
pause
