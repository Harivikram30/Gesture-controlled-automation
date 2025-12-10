# 🔧 Troubleshooting Guide
## Virtual AI LED Controller - Solutions to Common Issues

---

## 📑 Table of Contents

1. [Installation Issues](#installation-issues)
2. [Webcam Problems](#webcam-problems)
3. [Gesture Detection Issues](#gesture-detection-issues)
4. [GUI Problems](#gui-problems)
5. [Performance Issues](#performance-issues)
6. [Voice Feedback Issues](#voice-feedback-issues)
7. [Advanced Troubleshooting](#advanced-troubleshooting)

---

## 1. Installation Issues

### ❌ "pip not recognized" or "pip is not a command"

**Problem:** Python/pip not in PATH

**Solutions:**

**Windows:**
```bash
# Use py launcher
py -m pip install opencv-python mediapipe pyttsx3

# Or use full path
C:\Python39\Scripts\pip install opencv-python mediapipe pyttsx3
```

**Mac/Linux:**
```bash
# Use python3
python3 -m pip install opencv-python mediapipe pyttsx3

# Or use pip3
pip3 install opencv-python mediapipe pyttsx3
```

### ❌ "ModuleNotFoundError: No module named 'cv2'"

**Problem:** OpenCV not installed

**Solutions:**
```bash
# Uninstall any existing opencv packages
pip uninstall opencv-python opencv-contrib-python opencv-python-headless

# Install correct version
pip install opencv-python

# Verify installation
python -c "import cv2; print(cv2.__version__)"
```

### ❌ "ERROR: Could not build wheels for mediapipe"

**Problem:** Incompatible Python version or missing build tools

**Solutions:**

1. **Check Python Version:**
   ```bash
   python --version
   # Should be 3.7-3.11 (MediaPipe may not support 3.12+ yet)
   ```

2. **Use Pre-built Wheel:**
   ```bash
   pip install --upgrade pip
   pip install mediapipe --no-cache-dir
   ```

3. **Windows - Install Visual C++ Redistributable:**
   - Download from: https://aka.ms/vs/17/release/vc_redist.x64.exe

4. **Mac - Install Xcode Command Line Tools:**
   ```bash
   xcode-select --install
   ```

### ❌ "Permission Denied" errors

**Problem:** Insufficient permissions

**Solutions:**

**Windows (Admin mode):**
```bash
# Right-click Command Prompt → "Run as Administrator"
pip install opencv-python mediapipe pyttsx3
```

**Mac/Linux:**
```bash
# Use --user flag
pip install --user opencv-python mediapipe pyttsx3

# Or use sudo (not recommended)
sudo pip install opencv-python mediapipe pyttsx3
```

---

## 2. Webcam Problems

### ❌ Webcam window doesn't open

**Problem:** Camera not detected or in use

**Solutions:**

1. **Check if camera is working:**
   ```bash
   # Windows: Open Camera app
   # Mac: Open Photo Booth
   # Linux: cheese or guvcview
   ```

2. **Try different camera index:**
   
   Edit `virtual_led_controller.py` (line ~300):
   ```python
   # Try different values: 0, 1, 2, etc.
   cap = cv2.VideoCapture(1)  # Change 0 to 1
   ```

3. **Check camera permissions:**
   - **Windows:** Settings → Privacy → Camera → Allow apps
   - **Mac:** System Preferences → Security & Privacy → Camera
   - **Linux:** Check `/dev/video0` permissions

4. **Close other camera apps:**
   - Zoom, Skype, Teams, etc. might be using camera
   - Close all video conferencing apps
   - Restart computer if needed

### ❌ Black screen in webcam window

**Problem:** Camera blocked or driver issue

**Solutions:**

1. **Check physical camera:**
   - Remove any camera cover/sticker
   - Check if camera LED is on
   - Try external webcam if built-in fails

2. **Update camera drivers:**
   - **Windows:** Device Manager → Cameras → Update driver
   - **Mac:** Update macOS
   - **Linux:** `sudo apt update && sudo apt upgrade`

3. **Test with different resolution:**
   
   Edit `virtual_led_controller.py` (line ~302):
   ```python
   cap = cv2.VideoCapture(0)
   cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)   # Lower resolution
   cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
   ```

### ❌ "Failed to capture frame from webcam" message

**Problem:** Camera stream interrupted

**Solutions:**

1. **Check USB connection** (for external cameras)
2. **Reduce frame size** (see above)
3. **Add delay between frames:**
   
   Edit `virtual_led_controller.py` (line ~410):
   ```python
   # After cv2.waitKey(1)
   time.sleep(0.01)  # Add small delay
   ```

---

## 3. Gesture Detection Issues

### ❌ No gestures detected at all

**Problem:** Detection threshold too strict or hand not visible

**Solutions:**

1. **Lower confidence threshold:**
   
   Edit `virtual_led_controller.py` (line ~60):
   ```python
   CONFIDENCE_THRESHOLD = 0.5  # Default: 0.7
   ```

2. **Reduce debounce frames:**
   ```python
   DEBOUNCE_FRAMES = 2  # Default: 5
   ```

3. **Improve lighting:**
   - Use bright room light
   - Face toward light source
   - Avoid backlit situations

4. **Check hand position:**
   - Keep hand 1-2 feet from camera
   - Show full palm and fingers
   - Keep hand within frame bounds

5. **Verify MediaPipe is working:**
   - Check if green dots appear on your hand
   - If no dots, MediaPipe isn't detecting hand

### ❌ Wrong gestures detected

**Problem:** Similar gesture patterns or lighting issues

**Solutions:**

1. **Make more distinct gestures:**
   - Fully extend or close fingers
   - Hold steady for full second
   - Avoid partial gestures

2. **Increase confidence threshold:**
   ```python
   CONFIDENCE_THRESHOLD = 0.8  # Default: 0.7
   ```

3. **Add more specific conditions:**
   
   Edit gesture detection logic in `detect_gesture()` function:
   ```python
   # Add additional checks for your specific gesture
   if thumb_extended_up and fingers_extended == 0:
       # Additional verification
       if landmarks[THUMB_TIP].y < landmarks[WRIST].y - 0.1:
           return "thumb_up"
   ```

### ❌ Gestures keep flickering/toggling rapidly

**Problem:** Hand jitter or sensitivity too high

**Solutions:**

1. **Increase debounce frames:**
   ```python
   DEBOUNCE_FRAMES = 10  # Default: 5
   ```

2. **Hold hand more steady:**
   - Brace arm on table/desk
   - Keep hand still while making gesture

3. **Add cooldown period:**
   
   Add to `process_gesture_action()` function:
   ```python
   import time
   
   last_action_time = 0
   COOLDOWN_SECONDS = 1.0
   
   def process_gesture_action(gesture):
       global last_gesture, last_action_time
       
       current_time = time.time()
       if current_time - last_action_time < COOLDOWN_SECONDS:
           return  # Too soon, ignore
       
       if gesture and gesture in GESTURE_TO_LED:
           if gesture != last_gesture:
               toggle_led(GESTURE_TO_LED[gesture])
               last_gesture = gesture
               last_action_time = current_time
   ```

### ❌ Only detects some gestures, not others

**Problem:** Specific gesture logic issues

**Solutions:**

1. **Add debug prints:**
   
   In `detect_gesture()` function:
   ```python
   print(f"Thumb up: {thumb_extended_up}, Fingers: {fingers_extended}")
   print(f"Index: {index_extended}, Middle: {middle_extended}")
   ```

2. **Check landmark visibility:**
   - Ensure all fingers visible to camera
   - Don't hide fingers behind palm

3. **Adjust gesture conditions:**
   - Review detection logic for specific gesture
   - May need to tune distance thresholds

---

## 4. GUI Problems

### ❌ GUI window doesn't appear

**Problem:** Tkinter not installed or display issue

**Solutions:**

1. **Test Tkinter:**
   ```bash
   python -m tkinter
   # Should open a simple window
   ```

2. **Install Tkinter:**
   
   **Windows/Mac:** Usually included with Python
   
   **Linux:**
   ```bash
   sudo apt-get install python3-tk
   # or
   sudo yum install python3-tkinter
   ```

3. **Check display settings:**
   - **Linux:** Ensure `DISPLAY` variable is set
   - **Remote Desktop:** May need X11 forwarding

### ❌ LEDs not updating visually

**Problem:** Update loop issue or thread problem

**Solutions:**

1. **Check console for errors:**
   - Look for Python error messages
   - May indicate thread crash

2. **Verify LED states updating:**
   
   Add print in `toggle_led()`:
   ```python
   print(f"LED {led_id} is now {led_states[led_id]}")
   ```

3. **Increase update frequency:**
   
   In `LEDController.update_leds()`:
   ```python
   self.root.after(30, self.update_leds)  # Default: 50
   ```

### ❌ GUI is laggy or slow

**Problem:** Too many updates or slow rendering

**Solutions:**

1. **Disable glow effect:**
   ```python
   LED_GLOW_EFFECT = False  # Line ~65
   ```

2. **Reduce LED size:**
   ```python
   LED_SIZE = 80  # Default: 100
   ```

3. **Increase update interval:**
   ```python
   self.root.after(100, self.update_leds)  # Slower updates
   ```

4. **Reduce window size:**
   ```python
   WINDOW_WIDTH = 600   # Default: 800
   WINDOW_HEIGHT = 400  # Default: 600
   ```

### ❌ LEDs appear misaligned or cut off

**Problem:** Window too small or layout issue

**Solutions:**

1. **Increase window size:**
   ```python
   WINDOW_WIDTH = 1000
   WINDOW_HEIGHT = 700
   ```

2. **Adjust LED layout:**
   
   In `LEDController.__init__()`:
   ```python
   # Change grid layout
   rows = 2  # Instead of 3
   cols = 3  # Instead of 2
   ```

---

## 5. Performance Issues

### ❌ High CPU usage

**Problem:** Continuous processing loops

**Solutions:**

1. **Add frame delay:**
   ```python
   # In webcam processing loop
   time.sleep(0.01)
   ```

2. **Reduce camera resolution:**
   ```python
   cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
   cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
   ```

3. **Use simpler MediaPipe model:**
   ```python
   with mp_hands.Hands(
       model_complexity=0,  # Use lite model
       # ...
   ```

### ❌ Application freezes

**Problem:** Thread deadlock or blocking operation

**Solutions:**

1. **Check for blocking operations:**
   - Long voice synthesis
   - File I/O operations
   - Network calls

2. **Use threading for voice:**
   ```python
   def speak_async(text):
       threading.Thread(target=lambda: voice_engine.say(text), daemon=True).start()
   ```

3. **Add timeout for operations:**
   - Limit voice synthesis time
   - Add try-except blocks

### ❌ Memory leak / increasing RAM usage

**Problem:** Resources not being released

**Solutions:**

1. **Ensure proper cleanup:**
   - Camera release: `cap.release()`
   - Window destruction: `cv2.destroyAllWindows()`

2. **Clear gesture history periodically:**
   ```python
   if len(gesture_history) > 100:
       gesture_history.clear()
   ```

---

## 6. Voice Feedback Issues

### ❌ No voice feedback

**Problem:** pyttsx3 not installed or disabled

**Solutions:**

1. **Install pyttsx3:**
   ```bash
   pip install pyttsx3
   ```

2. **Check if enabled:**
   - Look for "Voice feedback: ENABLED" in startup messages
   - If DISABLED, check imports

3. **Test pyttsx3 separately:**
   ```python
   import pyttsx3
   engine = pyttsx3.init()
   engine.say("Test")
   engine.runAndWait()
   ```

### ❌ Voice too slow/fast

**Problem:** Voice rate setting

**Solutions:**

Edit voice settings (line ~120):
```python
voice_engine.setProperty('rate', 200)  # Default: 150 (higher = faster)
voice_engine.setProperty('volume', 1.0)  # 0.0 to 1.0
```

### ❌ Voice causes lag

**Problem:** Blocking voice synthesis

**Solutions:**

1. **Use async voice:**
   ```python
   def toggle_led(led_id):
       # ... existing code ...
       
       if VOICE_ENABLED:
           def speak():
               voice_engine.say(message)
               voice_engine.runAndWait()
           threading.Thread(target=speak, daemon=True).start()
   ```

2. **Disable voice:**
   ```python
   VOICE_ENABLED = False  # At top of file
   ```

---

## 7. Advanced Troubleshooting

### Debugging Mode

Enable detailed logging:

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('debug.log'),
        logging.StreamHandler()
    ]
)

# Add logging statements
logging.debug(f"Gesture detected: {gesture}")
logging.debug(f"LED states: {led_states}")
```

### Check System Information

Create `system_check.py`:

```python
import sys
import cv2
import mediapipe as mp

print("=== System Check ===")
print(f"Python: {sys.version}")
print(f"OpenCV: {cv2.__version__}")
print(f"MediaPipe: {mp.__version__}")

# Test camera
cap = cv2.VideoCapture(0)
ret, frame = cap.read()
print(f"Camera working: {ret}")
if ret:
    print(f"Resolution: {frame.shape}")
cap.release()

# Test Tkinter
try:
    import tkinter
    print("Tkinter: OK")
except:
    print("Tkinter: FAILED")

# Test pyttsx3
try:
    import pyttsx3
    print("pyttsx3: OK")
except:
    print("pyttsx3: NOT INSTALLED")
```

Run: `python system_check.py`

### Performance Profiling

Add timing measurements:

```python
import time

def profile_function(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {(end-start)*1000:.2f}ms")
        return result
    return wrapper

@profile_function
def detect_gesture(hand_landmarks):
    # ... existing code ...
```

### Clean Reinstall

If all else fails:

```bash
# Uninstall everything
pip uninstall opencv-python mediapipe pyttsx3 -y

# Clear pip cache
pip cache purge

# Reinstall
pip install --no-cache-dir opencv-python mediapipe pyttsx3

# Verify
python -c "import cv2, mediapipe; print('Success!')"
```

---

## 🆘 Still Having Issues?

### Checklist Before Asking for Help:

- [ ] Python 3.7-3.11 installed
- [ ] All packages installed without errors
- [ ] Webcam works in other applications
- [ ] Checked all relevant sections above
- [ ] Tried clean reinstall
- [ ] Checked console for error messages
- [ ] Tested system_check.py script

### When Reporting Issues:

Include:
1. Python version (`python --version`)
2. OS and version (Windows 10, macOS 12, Ubuntu 22.04, etc.)
3. Package versions (`pip list`)
4. Full error message
5. What you've tried already

---

## ✅ Quick Reference

| Symptom | Most Likely Fix |
|---------|-----------------|
| Import errors | `pip install -r requirements.txt` |
| No webcam | Try `cv2.VideoCapture(1)` |
| No gestures | Lower `CONFIDENCE_THRESHOLD = 0.5` |
| Flickering LEDs | Increase `DEBOUNCE_FRAMES = 10` |
| No GUI | Install Tkinter: `sudo apt install python3-tk` |
| Laggy | Disable `LED_GLOW_EFFECT = False` |
| No voice | `pip install pyttsx3` |
| High CPU | Add `time.sleep(0.01)` in loops |

---

**Good luck! Most issues can be solved by checking the solutions above.** 🔧✨
