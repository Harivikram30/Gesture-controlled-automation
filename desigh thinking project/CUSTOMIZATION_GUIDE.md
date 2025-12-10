# 🎨 Customization Guide
## Customizable Multi-Gesture Virtual AI LED Controller

This guide will help you customize and extend the Virtual AI LED Controller to suit your specific needs.

---

## 📑 Table of Contents

1. [Adding New Gestures](#adding-new-gestures)
2. [Adding More LEDs](#adding-more-leds)
3. [Customizing LED Colors](#customizing-led-colors)
4. [Adjusting Detection Settings](#adjusting-detection-settings)
5. [Modifying GUI Layout](#modifying-gui-layout)
6. [Advanced Customizations](#advanced-customizations)

---

## 1. Adding New Gestures

### Understanding Gesture Detection

Gestures are detected by analyzing the positions of hand landmarks provided by MediaPipe. Each hand has 21 landmarks:

```
Landmark IDs:
- 0: Wrist
- 1-4: Thumb (1=CMC, 2=MCP, 3=IP, 4=TIP)
- 5-8: Index (5=MCP, 6=PIP, 7=DIP, 8=TIP)
- 9-12: Middle (9=MCP, 10=PIP, 11=DIP, 12=TIP)
- 13-16: Ring (13=MCP, 14=PIP, 15=DIP, 16=TIP)
- 17-20: Pinky (17=MCP, 18=PIP, 19=DIP, 20=TIP)
```

### Step-by-Step: Adding a "Spock" Gesture

Let's add the Vulcan salute (index+middle together, ring+pinky together):

#### Step 1: Add Detection Logic

In `virtual_led_controller.py`, locate the `detect_gesture()` function (around line 150) and add:

```python
def detect_gesture(hand_landmarks):
    # ... existing code ...
    
    # Gesture: SPOCK (Vulcan Salute)
    # Index and middle extended together, ring and pinky extended together
    if (index_extended and middle_extended and 
        ring_extended and pinky_extended):
        
        # Check if index and middle are close (together)
        index_middle_dist = calculate_distance(
            landmarks[INDEX_TIP],
            landmarks[MIDDLE_TIP]
        )
        
        # Check if ring and pinky are close (together)
        ring_pinky_dist = calculate_distance(
            landmarks[RING_TIP],
            landmarks[PINKY_TIP]
        )
        
        # Check if there's a gap between middle and ring
        middle_ring_dist = calculate_distance(
            landmarks[MIDDLE_TIP],
            landmarks[RING_TIP]
        )
        
        if (index_middle_dist < 0.1 and 
            ring_pinky_dist < 0.1 and 
            middle_ring_dist > 0.15):
            return "spock"
    
    # ... rest of code ...
```

#### Step 2: Add Gesture Mapping

At the top of the file (around line 50), add to `GESTURE_TO_LED`:

```python
GESTURE_TO_LED = {
    "thumb_up": "LED1",
    "thumb_down": "LED2",
    "index_up": "LED3",
    "fist": "LED4",
    "peace_sign": "LED5",
    "open_palm": "LED6",
    "spock": "LED7",  # New gesture
}
```

#### Step 3: Add New LED (if needed)

Add to `LED_CONFIG`:

```python
LED_CONFIG = {
    # ... existing LEDs ...
    "LED7": {
        "color_on": "#00FF00",
        "color_off": "#003300",
        "label": "Spock LED"
    },
}
```

### Example Gestures You Can Add

#### "Three Fingers" Gesture
```python
if index_extended and middle_extended and ring_extended and not pinky_extended:
    return "three_fingers"
```

#### "Pinky Up" Gesture
```python
if pinky_extended and not index_extended and not middle_extended and not ring_extended:
    return "pinky_up"
```

#### "Thumbs Up + Index" Gesture
```python
if thumb_extended_up and index_extended and fingers_extended == 1:
    return "thumb_index_up"
```

#### "Rock On" Gesture
```python
if index_extended and pinky_extended and not middle_extended and not ring_extended:
    return "rock_on"
```

---

## 2. Adding More LEDs

### Basic LED Addition

1. Add to `LED_CONFIG`:
```python
"LED8": {
    "color_on": "#FF1493",      # Deep pink when ON
    "color_off": "#330011",      # Dark when OFF
    "label": "LED 8"
},
```

2. Map a gesture to it:
```python
GESTURE_TO_LED = {
    # ... existing mappings ...
    "my_gesture": "LED8",
}
```

### Adjusting Layout

If you add many LEDs, modify the GUI layout in `LEDController.__init__()`:

```python
# Change from 3 rows x 2 cols to 4 rows x 2 cols
rows = 4
cols = 2
```

Or for 3 columns:
```python
rows = 3
cols = 3
```

---

## 3. Customizing LED Colors

### Color Schemes

#### Neon Theme
```python
LED_CONFIG = {
    "LED1": {"color_on": "#39FF14", "color_off": "#0A3304", "label": "Neon Green"},
    "LED2": {"color_on": "#FF073A", "color_off": "#330108", "label": "Neon Red"},
    "LED3": {"color_on": "#BC13FE", "color_off": "#250333", "label": "Neon Purple"},
}
```

#### Pastel Theme
```python
LED_CONFIG = {
    "LED1": {"color_on": "#FFB3BA", "color_off": "#332326", "label": "Pastel Pink"},
    "LED2": {"color_on": "#BAFFC9", "color_off": "#233328", "label": "Pastel Green"},
    "LED3": {"color_on": "#BAE1FF", "color_off": "#232D33", "label": "Pastel Blue"},
}
```

#### Monochrome Theme
```python
LED_CONFIG = {
    "LED1": {"color_on": "#FFFFFF", "color_off": "#333333", "label": "White"},
    "LED2": {"color_on": "#CCCCCC", "color_off": "#2A2A2A", "label": "Light Gray"},
    "LED3": {"color_on": "#999999", "color_off": "#222222", "label": "Gray"},
}
```

### RGB LED Effect

Create color-changing LEDs:

```python
import random

def get_random_color():
    """Generate random RGB color."""
    r = random.randint(100, 255)
    g = random.randint(100, 255)
    b = random.randint(100, 255)
    return f"#{r:02x}{g:02x}{b:02x}"

# In toggle_led function:
def toggle_led(led_id):
    if led_states[led_id]:
        # When turning ON, use random color
        LED_CONFIG[led_id]['color_on'] = get_random_color()
    # ... rest of code ...
```

---

## 4. Adjusting Detection Settings

### Sensitivity Settings

Located at the top of `virtual_led_controller.py` (around line 60):

```python
# Make detection MORE sensitive (responds faster, may be jittery)
DEBOUNCE_FRAMES = 3              # Default: 5
CONFIDENCE_THRESHOLD = 0.5       # Default: 0.7

# Make detection LESS sensitive (more stable, slower response)
DEBOUNCE_FRAMES = 8              # Default: 5
CONFIDENCE_THRESHOLD = 0.85      # Default: 0.7
```

### Hand Detection Settings

In `webcam_processing_thread()` function:

```python
with mp_hands.Hands(
    model_complexity=1,              # 0=lite, 1=full (default: 0)
    min_detection_confidence=0.5,    # Lower = easier to detect
    min_tracking_confidence=0.5,     # Lower = smoother tracking
    max_num_hands=2                  # Detect multiple hands
) as hands:
```

---

## 5. Modifying GUI Layout

### Changing Window Size

```python
WINDOW_WIDTH = 1000   # Default: 800
WINDOW_HEIGHT = 700   # Default: 600
```

### Changing LED Size

```python
LED_SIZE = 120  # Default: 100
```

### Changing Color Scheme

```python
# In LEDController.__init__():
self.root.configure(bg='#000000')  # Pure black background

# For frames:
self.main_frame = tk.Frame(root, bg='#000000')

# For labels:
title_label = tk.Label(
    self.main_frame,
    text="🎮 Virtual AI LED Controller",
    font=('Arial', 24, 'bold'),
    bg='#000000',         # Background
    fg='#00FFFF'          # Text color (cyan)
)
```

### Disable Glow Effect

```python
LED_GLOW_EFFECT = False  # Default: True
```

---

## 6. Advanced Customizations

### Adding LED Patterns

Create LED sequences or patterns:

```python
def led_pattern_wave():
    """Create a wave pattern across LEDs."""
    led_ids = list(LED_CONFIG.keys())
    for led_id in led_ids:
        led_states[led_id] = True
        time.sleep(0.2)
        led_states[led_id] = False

# Trigger on specific gesture:
if confirmed_gesture == "open_palm":
    led_pattern_wave()
```

### Adding Sound Effects

Instead of voice feedback, add sound effects:

```python
# Install: pip install playsound
from playsound import playsound

def toggle_led(led_id):
    # ... existing code ...
    if led_states[led_id]:
        playsound('on_sound.mp3', False)
    else:
        playsound('off_sound.mp3', False)
```

### Gesture Combo System

Detect gesture sequences:

```python
gesture_sequence = []
MAX_SEQUENCE_LENGTH = 3

def process_gesture_sequence(gesture):
    """Detect gesture combinations."""
    gesture_sequence.append(gesture)
    
    if len(gesture_sequence) > MAX_SEQUENCE_LENGTH:
        gesture_sequence.pop(0)
    
    # Check for specific sequence
    if gesture_sequence == ["fist", "peace_sign", "open_palm"]:
        print("Secret combo activated!")
        # Toggle all LEDs
        for led_id in led_states:
            led_states[led_id] = True
```

### Logging System

Add gesture logging for debugging:

```python
import logging
from datetime import datetime

logging.basicConfig(
    filename='gesture_log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

def process_gesture_action(gesture):
    logging.info(f"Gesture detected: {gesture}")
    # ... rest of code ...
```

### Configuration File Support

Create external configuration:

**config.json:**
```json
{
    "leds": {
        "LED1": {
            "color_on": "#00FF00",
            "color_off": "#003300",
            "label": "LED 1"
        }
    },
    "gestures": {
        "thumb_up": "LED1",
        "fist": "LED2"
    },
    "settings": {
        "debounce_frames": 5,
        "confidence_threshold": 0.7
    }
}
```

**Loading config:**
```python
import json

def load_config():
    with open('config.json', 'r') as f:
        return json.load(f)

config = load_config()
LED_CONFIG = config['leds']
GESTURE_TO_LED = config['gestures']
```

---

## 🎯 Quick Tips

1. **Test One Change at a Time**: Make one modification and test before adding more
2. **Use Print Statements**: Add `print()` in `detect_gesture()` to debug
3. **Start Simple**: Begin with basic gestures before complex ones
4. **Check Landmark Positions**: Print landmark coordinates to understand hand pose
5. **Adjust Thresholds**: Fine-tune distance thresholds for your specific gestures

---

## 🐛 Common Issues

### Gesture Not Detected
- **Solution**: Lower `CONFIDENCE_THRESHOLD` or `DEBOUNCE_FRAMES`
- Add debug prints in `detect_gesture()`

### LEDs Don't Update
- **Solution**: Check gesture name matches exactly in `GESTURE_TO_LED`
- Ensure LED ID exists in `LED_CONFIG`

### GUI Laggy
- **Solution**: Reduce LED_SIZE or disable glow effects
- Increase `self.root.after(50, ...)` value to 100

---

## 📚 Resources

- [MediaPipe Hand Landmarks](https://google.github.io/mediapipe/solutions/hands.html)
- [OpenCV Python Tutorials](https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html)
- [Tkinter Documentation](https://docs.python.org/3/library/tkinter.html)

---

## ✨ Share Your Customizations!

Created something cool? Share it with the community!

Happy customizing! 🎨
