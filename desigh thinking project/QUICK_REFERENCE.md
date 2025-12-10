# ⚡ QUICK REFERENCE CARD
## Virtual AI LED Controller - Cheat Sheet

---

## 🚀 Quick Commands

```bash
# Installation
pip install opencv-python mediapipe pyttsx3

# Run Application
python virtual_led_controller.py

# Run Demo (no webcam)
python demo.py

# Exit Application
Press 'q' in webcam window
```

---

## 🎮 Default Gestures

| Gesture | LED | Key |
|---------|-----|-----|
| 👍 Thumb Up | LED 1 🟢 | Thumb up, fingers closed |
| 👎 Thumb Down | LED 2 🔴 | Thumb down, fingers closed |
| ☝ Index Up | LED 3 🔵 | Only index extended |
| ✊ Fist | LED 4 🟡 | All fingers closed |
| ✌ Peace | LED 5 🟣 | Index + middle up |
| 🖐 Open Palm | LED 6 🔷 | All fingers extended |

---

## 🔧 Quick Settings (in code)

```python
# File: virtual_led_controller.py

# --- Sensitivity ---
DEBOUNCE_FRAMES = 5        # Higher = more stable (line ~60)
CONFIDENCE_THRESHOLD = 0.7 # Higher = more accurate (line ~61)

# --- GUI ---
WINDOW_WIDTH = 800         # Window width (line ~64)
WINDOW_HEIGHT = 600        # Window height (line ~65)
LED_SIZE = 100             # LED circle size (line ~66)
LED_GLOW_EFFECT = True     # Glow animation (line ~67)

# --- Webcam ---
cap = cv2.VideoCapture(0)  # Camera index (line ~301)
# Try: 0, 1, 2 if webcam not found
```

---

## ➕ Add Custom Gesture (3 Steps)

### Step 1: Detect Gesture (line ~200)
```python
# In detect_gesture() function:
if <your_condition>:
    return "my_gesture"
```

### Step 2: Map to LED (line ~50)
```python
GESTURE_TO_LED = {
    # ... existing ...
    "my_gesture": "LED1",
}
```

### Step 3: Done! Run and test.

---

## 🎨 Add New LED (2 Steps)

### Step 1: Define LED (line ~40)
```python
LED_CONFIG = {
    # ... existing ...
    "LED7": {
        "color_on": "#FFA500",
        "color_off": "#332200",
        "label": "LED 7"
    },
}
```

### Step 2: Map Gesture (line ~50)
```python
GESTURE_TO_LED = {
    # ... existing ...
    "my_gesture": "LED7",
}
```

---

## 🎨 Color Codes Reference

```python
# Common Colors
"#FF0000" = Red
"#00FF00" = Green
"#0000FF" = Blue
"#FFFF00" = Yellow
"#FF00FF" = Magenta
"#00FFFF" = Cyan
"#FFA500" = Orange
"#800080" = Purple
"#FFFFFF" = White
"#000000" = Black
```

---

## 🐛 Quick Troubleshooting

| Problem | Quick Fix |
|---------|-----------|
| No webcam | `cv2.VideoCapture(1)` line ~301 |
| No gestures | `CONFIDENCE_THRESHOLD = 0.5` line ~61 |
| Flickering | `DEBOUNCE_FRAMES = 10` line ~60 |
| GUI slow | `LED_GLOW_EFFECT = False` line ~67 |
| No Tkinter | `sudo apt install python3-tk` (Linux) |

---

## 📂 File Reference

| File | Purpose |
|------|---------|
| `virtual_led_controller.py` | Main application |
| `README.md` | Full documentation |
| `QUICK_START.md` | 5-min start guide |
| `CUSTOMIZATION_GUIDE.md` | How to customize |
| `TROUBLESHOOTING.md` | Problem solutions |
| `PRESENTATION_GUIDE.md` | Demo guide |
| `demo.py` | Automated demo |
| `config_example.py` | Config examples |
| `requirements.txt` | Dependencies |
| `setup.bat/.sh` | Install scripts |

---

## 📋 Gesture Detection Tips

✅ **Do:**
- Keep hand 1-2 feet from camera
- Use good lighting
- Show full hand to camera
- Hold gesture steady (1 second)
- Wait for confirmation

❌ **Don't:**
- Move too fast
- Hide fingers
- Use in dim lighting
- Make partial gestures
- Rush between gestures

---

## 🔑 Key Code Locations

```
Line ~40:  LED_CONFIG
Line ~50:  GESTURE_TO_LED
Line ~60:  Sensitivity settings
Line ~150: detect_gesture() function
Line ~240: toggle_led() function
Line ~280: webcam_processing_thread()
Line ~400: LEDController class
```

---

## 📊 Performance Targets

- **FPS**: 30 (webcam)
- **Latency**: <100ms
- **CPU**: ~15-25%
- **RAM**: ~200-300 MB
- **Accuracy**: 95%+ (good light)

---

## 🎯 Demo Sequence

1. Start app: `python virtual_led_controller.py`
2. Show **Thumbs Up** → LED 1 ON
3. Show **Fist** → LED 4 ON
4. Show **Peace** → LED 5 ON
5. Show **Thumbs Up** → LED 1 OFF
6. Press **'q'** → Exit

---

## 💡 Quick Customization Examples

### Rainbow Theme
```python
LED_CONFIG = {
    "LED1": {"color_on": "#FF0000", ...},  # Red
    "LED2": {"color_on": "#FF7F00", ...},  # Orange
    "LED3": {"color_on": "#FFFF00", ...},  # Yellow
    "LED4": {"color_on": "#00FF00", ...},  # Green
    "LED5": {"color_on": "#0000FF", ...},  # Blue
    "LED6": {"color_on": "#8B00FF", ...},  # Violet
}
```

### High Sensitivity
```python
DEBOUNCE_FRAMES = 2
CONFIDENCE_THRESHOLD = 0.5
```

### Low Sensitivity (Very Stable)
```python
DEBOUNCE_FRAMES = 10
CONFIDENCE_THRESHOLD = 0.85
```

### Smaller Window
```python
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400
LED_SIZE = 70
```

---

## 🎓 Learning Path

1. **Run** the app → See it work
2. **Read** QUICK_START.md → Understand basics
3. **Try** gestures → Get comfortable
4. **Change** LED colors → Simple customization
5. **Add** gesture → Learn detection
6. **Extend** features → Advanced customization

---

## 🆘 Emergency Fixes

### App won't start
```bash
pip uninstall opencv-python mediapipe
pip install opencv-python mediapipe
```

### Webcam black screen
```python
# Try different camera
cap = cv2.VideoCapture(1)  # or 2, 3...
```

### Import errors
```bash
pip install -r requirements.txt
```

---

## ✨ Pro Tips

1. **Good Lighting**: Use bright, front lighting
2. **Hand Position**: 1-2 feet from camera
3. **Clear Gestures**: Fully extend/close fingers
4. **Steady Hand**: Hold gesture for 1 second
5. **Test First**: Try all gestures before demo

---

## 📞 Help Resources

- Code comments: Detailed explanations
- TROUBLESHOOTING.md: Common solutions
- CUSTOMIZATION_GUIDE.md: How-to guides
- README.md: Complete docs

---

## 🎬 5-Second Demo

```python
"Show hand → Make gesture → LED toggles → Repeat"
```

---

**Print this card for quick reference during development!** 📄✨

---

*Quick Reference v1.0 | Virtual AI LED Controller*
