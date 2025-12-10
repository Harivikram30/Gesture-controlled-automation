# ♿ Accessible Gesture Controller

## 🎯 Project Overview
A precision gesture-controlled device system designed specifically for people with **limited mobility**. This project uses computer vision and AI to detect hand gestures with high accuracy, allowing users to control virtual devices (LEDs, Fan, Door Lock, TV) through simple, distinct hand gestures.

## ✨ Key Features

### 🤖 High-Precision Gesture Detection
- **Enhanced accuracy** with angle-based finger detection
- **5 distinct, easy-to-perform gestures**
- **Debounce system** to prevent accidental triggers
- **Real-time feedback** with visual and optional voice confirmation

### 📱 5 Controllable Devices
1. **💡 Red LED** - Controlled by Thumbs Up gesture
2. **💡 Green LED** - Controlled by Thumbs Down gesture
3. **🌀 Virtual Fan** - Rotating blade animation, controlled by Three Fingers
4. **🔐 Door Lock** - Lock/unlock visualization, controlled by Index Finger
5. **📺 Smart TV** - Channel switching with animations, controlled by Two Fingers (Peace Sign)

### ⚙️ Customizable Gestures
- **GUI Settings Panel** - Click "Customize Gestures" button to view mappings
- **JSON Configuration** - Edit `gesture_config.json` to remap gestures
- **Save/Load System** - Persist custom configurations across sessions

### 🎨 Professional Animations
- **LED Glow Effects** - Pulsing glow when LEDs are active
- **Rotating Fan Blades** - Smooth 360° rotation animation
- **TV Screen Effects** - Static noise when OFF, channel display with scan lines when ON
- **Lock Animation** - Open/closed padlock visualization
- **Color-Coded Status** - Green for ON/UNLOCKED, Red for OFF/LOCKED

## 🎮 Gesture Controls

| Gesture | Description | Controls | Note |
|---------|-------------|----------|------|
| 👍 **Thumbs Up** | Thumb extended up, other fingers closed | Red LED (LED1) | Toggle ON/OFF |
| 👎 **Thumbs Down** | Thumb extended down, other fingers closed | Green LED (LED2) | Toggle ON/OFF |
| ☝ **Index Finger** | Only index finger extended | Door Lock (LOCK1) | Lock/Unlock |
| ✌ **Peace Sign** | Index + middle fingers extended | Smart TV (TV1) | ON/OFF + Channel Change |
| 🤟 **Three Fingers** | Index + middle + ring extended | Virtual Fan (FAN1) | Toggle ON/OFF |

## 📋 System Requirements

### Hardware
- **Webcam** (built-in laptop camera works fine)
- **Processor** Intel i3 or equivalent (for real-time processing)
- **RAM** 4GB minimum, 8GB recommended

### Software
- **Python 3.7+**
- **Windows/Linux/Mac** compatible

## 🚀 Installation

### Step 1: Install Dependencies
```cmd
pip install opencv-python mediapipe==0.10.13 pyttsx3
```

**Note:** We use MediaPipe 0.10.13 specifically to avoid TensorFlow slow-loading issues in newer versions.

### Step 2: Run the Application
```cmd
python virtual_led_controller.py
```

### Step 3: Wait for Initialization
- First run may take **30-60 seconds** to load MediaPipe models
- Webcam window and GUI window will appear automatically
- Look for the message "✓ Hand detection initialized"

## 🎯 How to Use

1. **Start the Application**
   - Run `python virtual_led_controller.py`
   - Two windows will appear: Webcam feed and Device Control GUI

2. **Position Your Hand**
   - Show your hand to the webcam
   - Green landmarks will appear on your hand when detected
   - Keep hand steady for 1-2 seconds

3. **Perform Gestures**
   - Make the desired gesture (see table above)
   - Hold for ~1 second for detection
   - Device will toggle with visual + audio feedback
   - Gesture name appears on webcam feed

4. **Customize Gestures** (Optional)
   - Click "⚙ Customize Gestures" button in GUI
   - View current mappings
   - Click "💾 Save to File" to create `gesture_config.json`
   - Edit JSON file to remap gestures
   - Restart application to load changes

5. **Exit**
   - Press **'q'** in webcam window to quit safely

## 📂 Project Structure

```
desigh thinking project/
│
├── virtual_led_controller.py   # Main application (1000+ lines)
├── gesture_config.json          # Custom gesture mappings
├── requirements.txt             # Dependencies list
└── README_ACCESSIBLE.md         # This file
```

## ⚙️ Configuration

### Gesture Customization
Edit `gesture_config.json`:
```json
{
    "gestures": {
        "thumb_up": "LED1",
        "thumb_down": "LED2",
        "three_fingers": "FAN1",
        "index_up": "LOCK1",
        "peace_sign": "TV1"
    }
}
```

You can remap any gesture to any device!

### Adjustable Settings (in code)
- `DEBOUNCE_FRAMES = 5` - Frames needed to confirm gesture (higher = more stable)
- `CONFIDENCE_THRESHOLD = 0.7` - Hand detection confidence (0.0-1.0)
- `LED_GLOW_EFFECT = True` - Enable/disable LED glow animation
- `VOICE_ENABLED = True` - Text-to-speech feedback

## 🔧 Troubleshooting

### Issue: Application takes 2-3 minutes to start
**Solution:** This is normal on first run. MediaPipe loads AI models. Subsequent runs are faster.

### Issue: Webcam not detected
**Solution:**
- Check if webcam is being used by another application
- Try changing camera index in code: `cv2.VideoCapture(0)` → `cv2.VideoCapture(1)`

### Issue: Gestures not detected
**Solution:**
- Ensure good lighting
- Keep hand 30-50cm from camera
- Hold gesture steady for 1-2 seconds
- Check webcam shows green hand landmarks

### Issue: False gesture triggers
**Solution:**
- Increase `DEBOUNCE_FRAMES` to 7 or 10
- Increase `CONFIDENCE_THRESHOLD` to 0.8
- Make gestures more distinct

### Issue: GUI window not visible
**Solution:**
- Check if window opened on another monitor
- Alt+Tab to find windows
- Window may be loading behind other windows

## 💡 Tips for Best Performance

1. **Lighting** - Use good, even lighting (not backlighting)
2. **Background** - Plain, contrasting background works best
3. **Distance** - Keep hand 30-50cm from camera
4. **Steadiness** - Hold gesture for full 1-2 seconds
5. **Distinctness** - Make clear, exaggerated gestures
6. **Camera** - Face camera directly, not at an angle

## 🎓 Educational Value

This project demonstrates:
- **Computer Vision** with OpenCV
- **AI/Machine Learning** with MediaPipe hand tracking
- **GUI Development** with Tkinter
- **Multi-threading** for concurrent webcam and GUI updates
- **Event-driven Programming** with gesture callbacks
- **Accessibility Design** for limited mobility users
- **Configuration Management** with JSON
- **Real-time Animation** and visual feedback

## 🌟 Accessibility Features

- **Large, clear gestures** - Easy to perform with limited mobility
- **Visual feedback** - Color-coded status indicators
- **Audio feedback** - Optional voice confirmation
- **Customizable mappings** - Adapt to user's abilities
- **Debounce protection** - Prevents accidental triggers
- **High precision** - Angle-based detection for accuracy

## 📝 Future Enhancements

- [ ] Add more device types (lights, AC, music player)
- [ ] Voice command integration
- [ ] Mobile app for remote control
- [ ] Gesture training mode for custom gestures
- [ ] Multi-hand support
- [ ] Gesture history and analytics
- [ ] Cloud sync for configurations

## 📄 License

MIT License - Free to use, modify, and distribute

## 👨‍💻 Credits

- **MediaPipe** by Google - Hand tracking AI
- **OpenCV** - Computer vision library
- **Tkinter** - Python GUI framework

## 🤝 Support

For questions, issues, or suggestions:
- Check code comments for detailed explanations
- Review TROUBLESHOOTING section above
- Modify `DEBOUNCE_FRAMES` and `CONFIDENCE_THRESHOLD` for your needs

---

**Made with ❤️ for accessibility and inclusion**

*Empowering people with limited mobility through gesture control technology*
