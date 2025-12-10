"""
Configuration Example for Virtual LED Controller
=================================================

This file demonstrates how to create custom configurations
for the Virtual LED Controller. Copy this file and modify
it to create your own custom setup.

Usage:
1. Copy this file to 'config.py'
2. Modify the settings below
3. Import in main file: from config import *
"""

# =============================================================================
# EXAMPLE 1: Rainbow LED Configuration
# =============================================================================

RAINBOW_LED_CONFIG = {
    "LED1": {"color_on": "#FF0000", "color_off": "#330000", "label": "Red"},
    "LED2": {"color_on": "#FF7F00", "color_off": "#331900", "label": "Orange"},
    "LED3": {"color_on": "#FFFF00", "color_off": "#333300", "label": "Yellow"},
    "LED4": {"color_on": "#00FF00", "color_off": "#003300", "label": "Green"},
    "LED5": {"color_on": "#0000FF", "color_off": "#000033", "label": "Blue"},
    "LED6": {"color_on": "#4B0082", "color_off": "#0F001A", "label": "Indigo"},
    "LED7": {"color_on": "#9400D3", "color_off": "#1E002A", "label": "Violet"},
}

RAINBOW_GESTURE_MAP = {
    "thumb_up": "LED1",
    "thumb_down": "LED2",
    "index_up": "LED3",
    "fist": "LED4",
    "peace_sign": "LED5",
    "open_palm": "LED6",
    "rock_on": "LED7",
}

# =============================================================================
# EXAMPLE 2: Traffic Light Configuration
# =============================================================================

TRAFFIC_LED_CONFIG = {
    "LED1": {"color_on": "#FF0000", "color_off": "#330000", "label": "Red Light"},
    "LED2": {"color_on": "#FFFF00", "color_off": "#333300", "label": "Yellow Light"},
    "LED3": {"color_on": "#00FF00", "color_off": "#003300", "label": "Green Light"},
}

TRAFFIC_GESTURE_MAP = {
    "fist": "LED1",          # Stop
    "index_up": "LED2",      # Caution
    "open_palm": "LED3",     # Go
}

# =============================================================================
# EXAMPLE 3: Gaming Control Configuration
# =============================================================================

GAMING_LED_CONFIG = {
    "LED1": {"color_on": "#00FF00", "color_off": "#003300", "label": "Power"},
    "LED2": {"color_on": "#FF0000", "color_off": "#330000", "label": "Alert"},
    "LED3": {"color_on": "#0000FF", "color_off": "#000033", "label": "Shield"},
    "LED4": {"color_on": "#FFFF00", "color_off": "#333300", "label": "Boost"},
    "LED5": {"color_on": "#FF00FF", "color_off": "#330033", "label": "Special"},
}

GAMING_GESTURE_MAP = {
    "thumb_up": "LED1",      # Power On
    "fist": "LED2",          # Alert/Attack
    "peace_sign": "LED3",    # Shield
    "open_palm": "LED4",     # Boost
    "index_up": "LED5",      # Special Move
}

# =============================================================================
# EXAMPLE 4: Monochrome Minimalist Configuration
# =============================================================================

MONO_LED_CONFIG = {
    "LED1": {"color_on": "#FFFFFF", "color_off": "#333333", "label": "Light 1"},
    "LED2": {"color_on": "#CCCCCC", "color_off": "#2A2A2A", "label": "Light 2"},
    "LED3": {"color_on": "#999999", "color_off": "#222222", "label": "Light 3"},
    "LED4": {"color_on": "#666666", "color_off": "#1A1A1A", "label": "Light 4"},
}

MONO_GESTURE_MAP = {
    "thumb_up": "LED1",
    "index_up": "LED2",
    "peace_sign": "LED3",
    "open_palm": "LED4",
}

# =============================================================================
# EXAMPLE 5: Custom Sensitivity Settings
# =============================================================================

# High Sensitivity (Faster response, may be jittery)
HIGH_SENSITIVITY = {
    "DEBOUNCE_FRAMES": 2,
    "CONFIDENCE_THRESHOLD": 0.5,
}

# Medium Sensitivity (Balanced)
MEDIUM_SENSITIVITY = {
    "DEBOUNCE_FRAMES": 5,
    "CONFIDENCE_THRESHOLD": 0.7,
}

# Low Sensitivity (Very stable, slower response)
LOW_SENSITIVITY = {
    "DEBOUNCE_FRAMES": 10,
    "CONFIDENCE_THRESHOLD": 0.85,
}

# =============================================================================
# EXAMPLE 6: Custom GUI Settings
# =============================================================================

LARGE_SCREEN_GUI = {
    "WINDOW_WIDTH": 1200,
    "WINDOW_HEIGHT": 800,
    "LED_SIZE": 150,
}

SMALL_SCREEN_GUI = {
    "WINDOW_WIDTH": 600,
    "WINDOW_HEIGHT": 400,
    "LED_SIZE": 60,
}

PRESENTATION_GUI = {
    "WINDOW_WIDTH": 1920,
    "WINDOW_HEIGHT": 1080,
    "LED_SIZE": 200,
}

# =============================================================================
# EXAMPLE 7: Advanced Gesture Configuration
# =============================================================================

ADVANCED_GESTURES = {
    # Basic Gestures
    "thumb_up": "LED1",
    "thumb_down": "LED2",
    "index_up": "LED3",
    "fist": "LED4",
    
    # Advanced Gestures
    "peace_sign": "LED5",
    "three_fingers": "LED6",
    "four_fingers": "LED7",
    "open_palm": "LED8",
    
    # Expert Gestures (you'll need to implement these)
    "pinky_up": "LED9",
    "ok_sign": "LED10",
    "rock_on": "LED11",
    "call_me": "LED12",
}

# =============================================================================
# HOW TO USE THESE CONFIGURATIONS
# =============================================================================

"""
Method 1: Direct Import
------------------------
In virtual_led_controller.py, replace the existing config:

    from config_example import RAINBOW_LED_CONFIG, RAINBOW_GESTURE_MAP
    
    LED_CONFIG = RAINBOW_LED_CONFIG
    GESTURE_TO_LED = RAINBOW_GESTURE_MAP


Method 2: Copy and Paste
-------------------------
Copy the desired configuration from above and paste it directly
into virtual_led_controller.py, replacing the existing LED_CONFIG
and GESTURE_TO_LED dictionaries.


Method 3: Dynamic Loading
--------------------------
Create a config selector:

    def load_config(theme="default"):
        if theme == "rainbow":
            return RAINBOW_LED_CONFIG, RAINBOW_GESTURE_MAP
        elif theme == "traffic":
            return TRAFFIC_LED_CONFIG, TRAFFIC_GESTURE_MAP
        # ... etc
    
    LED_CONFIG, GESTURE_TO_LED = load_config("rainbow")
"""

# =============================================================================
# TIPS FOR CREATING YOUR OWN CONFIGURATION
# =============================================================================

"""
1. LED Colors:
   - Use hex color codes: #RRGGBB
   - Online tool: https://www.color-hex.com/
   - Ensure color_off is much darker than color_on

2. LED Count:
   - You can have 1 to 20+ LEDs
   - GUI adjusts automatically
   - More LEDs = smaller individual size

3. Gesture Names:
   - Use snake_case (lowercase with underscores)
   - Be descriptive: "thumb_up" not "g1"
   - Must match exactly in gesture detection function

4. Testing:
   - Start with 3-4 LEDs
   - Test each gesture individually
   - Adjust sensitivity if needed

5. Performance:
   - More LEDs = slightly slower GUI
   - Keep LED_SIZE reasonable (50-150)
   - Disable glow effect if laggy
"""
