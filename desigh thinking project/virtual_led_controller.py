"""
=============================================================================
CUSTOMIZABLE MULTI-GESTURE VIRTUAL AI LED CONTROLLER
=============================================================================

A professional, laptop-only project that detects hand gestures via webcam
and controls multiple virtual LEDs in real-time using OpenCV, MediaPipe, and Tkinter.

Perfect for: Hackathons, Academic Projects, Portfolio, Demonstrations

Author: AI Assistant
Date: November 5, 2025
Version: 1.0

=============================================================================
INSTALLATION INSTRUCTIONS:
=============================================================================
1. Install required libraries:
   pip install opencv-python mediapipe pyttsx3

2. Run the project:
   python virtual_led_controller.py

3. Exit:
   Press 'q' in the webcam window to quit safely

=============================================================================
CUSTOMIZATION GUIDE:
=============================================================================
To add your own gestures:
1. Define the gesture logic in detect_gesture() function
2. Add the gesture-to-LED mapping in GESTURE_TO_LED dictionary
3. Add more LEDs in LED_CONFIG dictionary if needed
4. The system will automatically handle the new mappings!

Example: To add "peace sign" gesture that controls LED5:
- Add detection logic in detect_gesture()
- Add "peace_sign": "LED5" to GESTURE_TO_LED
- System handles the rest automatically!

=============================================================================
"""

import os
import sys
import warnings

# Suppress all warnings (TensorFlow, protobuf, MediaPipe deprecations)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['MEDIAPIPE_DISABLE_GPU'] = '1'
warnings.filterwarnings('ignore', category=DeprecationWarning)
warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore')

print("=" * 70)
print("🚀 VIRTUAL GESTURE CONTROLLER - STARTING UP")
print("=" * 70)
print("⚠️  FIRST TIME LOADING: This may take 1-3 minutes")
print("⚠️  Please be patient while libraries load...")
print("=" * 70)
print()

import cv2
# Import only vision components from mediapipe to avoid audio dependencies
print("🔄 Loading MediaPipe (this is the slow part)...")
from mediapipe.python.solutions import hands as mp_hands
from mediapipe.python.solutions import drawing_utils as mp_drawing
from mediapipe.python.solutions import drawing_styles as mp_drawing_styles
print("✓ MediaPipe loaded!")

import tkinter as tk
from tkinter import ttk
import threading
import time
from collections import deque
import math

# Optional: Voice feedback (comment out if not needed)
VOICE_ENABLED = False  # Disabled for stability

# =============================================================================
# CONFIGURATION SECTION - CUSTOMIZE YOUR PROJECT HERE
# =============================================================================

# Device Configuration: Define all devices here
# Types: led, fan, door_lock, tv
DEVICE_CONFIG = {
    "LED1": {"type": "led", "color_on": "#FF0000", "color_off": "#330000", "label": "💡 Red LED"},
    "LED2": {"type": "led", "color_on": "#00FF00", "color_off": "#003300", "label": "💡 Green LED"},
    "FAN1": {"type": "fan", "color_on": "#00BBFF", "color_off": "#223344", "label": "🌀 Virtual Fan"},
    "LOCK1": {"type": "door_lock", "color_on": "#00FF00", "color_off": "#FF0000", "label": "🔐 Door Lock"},
    "TV1": {"type": "tv", "color_on": "#4488FF", "color_off": "#1a1a1a", "label": "📺 Smart TV"},
}

# Keep LED_CONFIG for backward compatibility
LED_CONFIG = DEVICE_CONFIG

# Gesture-to-Device Mapping (5 precise gestures for 5 devices)
GESTURE_TO_LED = {
    'thumb_up': 'LED1',      # Thumbs up → Red LED
    'thumb_down': 'LED2',    # Thumbs down → Green LED
    'three_fingers': 'FAN1', # Three fingers (index+middle+ring) → Fan
    'index_up': 'LOCK1',     # Index finger only → Door Lock
    'peace_sign': 'TV1'      # Two fingers (index+middle) → TV
}

# Debounce settings to prevent flickering
DEBOUNCE_FRAMES = 3  # Number of consecutive frames needed to confirm gesture (reduced for faster response)
CONFIDENCE_THRESHOLD = 0.6  # Minimum detection confidence (lowered for better detection)

# GUI Settings
WINDOW_TITLE = "♿ Accessible Gesture Controller"
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 700
DEVICE_SIZE = 110  # Size of device displays
LED_SIZE = DEVICE_SIZE  # Backward compatibility
LED_GLOW_EFFECT = True  # Enable glow effect on LEDs

# TV channel data for animation
TV_CHANNELS = ["News 24", "Sports HD", "Movies", "Music TV", "Nature"]
TV_CHANNEL_INDEX = {'TV1': 0}  # Current channel for each TV
RGB_COLORS = ["#FF0000", "#FF7F00", "#FFFF00", "#00FF00", "#0000FF", "#4B0082", "#9400D3"]  # Rainbow colors for RGB strip
RGB_COLOR_INDEX = 0  # Current RGB color index

# =============================================================================
# GLOBAL VARIABLES
# =============================================================================

# =============================================================================
# GESTURE CUSTOMIZATION - Load/Save Custom Mappings
# =============================================================================

import json
import os

CONFIG_FILE = "gesture_config.json"

def load_custom_gestures():
    """Load custom gesture mappings from config file."""
    global GESTURE_TO_LED
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                custom_config = json.load(f)
                GESTURE_TO_LED.update(custom_config.get('gestures', {}))
                print(f"✓ Loaded custom gesture mappings from {CONFIG_FILE}")
        except Exception as e:
            print(f"⚠ Could not load config: {e}")

def save_custom_gestures():
    """Save current gesture mappings to config file."""
    try:
        config_data = {
            'gestures': GESTURE_TO_LED,
            'info': 'Gesture to Device Mapping - Edit to customize'
        }
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config_data, f, indent=4)
        print(f"✓ Saved gesture mappings to {CONFIG_FILE}")
    except Exception as e:
        print(f"⚠ Could not save config: {e}")

# Load custom gestures if config file exists
load_custom_gestures()

# Device states (all start as OFF, door locks start as LOCKED which is False)
led_states = {device_id: False for device_id in DEVICE_CONFIG.keys()}

# Gesture debounce queue
gesture_history = deque(maxlen=DEBOUNCE_FRAMES)

# Voice engine setup (disabled)
voice_engine = None

# Threading control
running = True
last_gesture = None

# =============================================================================
# GESTURE DETECTION FUNCTIONS
# =============================================================================

def calculate_distance(point1, point2):
    """Calculate Euclidean distance between two points."""
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

def calculate_distance(point1, point2):
    """Calculate Euclidean distance between two landmarks."""
    import math
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2 + (point1.z - point2.z)**2)

def calculate_angle(point1, point2, point3):
    """Calculate angle at point2 formed by point1-point2-point3."""
    import math
    vector1 = [point1.x - point2.x, point1.y - point2.y, point1.z - point2.z]
    vector2 = [point3.x - point2.x, point3.y - point2.y, point3.z - point2.z]
    
    # Calculate dot product and magnitudes
    dot_product = sum(v1 * v2 for v1, v2 in zip(vector1, vector2))
    magnitude1 = math.sqrt(sum(v**2 for v in vector1))
    magnitude2 = math.sqrt(sum(v**2 for v in vector2))
    
    if magnitude1 * magnitude2 == 0:
        return 0
    
    # Calculate angle in degrees
    cos_angle = dot_product / (magnitude1 * magnitude2)
    cos_angle = max(-1, min(1, cos_angle))  # Clamp to [-1, 1]
    angle = math.degrees(math.acos(cos_angle))
    return angle

def is_finger_extended(landmarks, finger_tip_id, finger_pip_id, finger_mcp_id, threshold=140):
    """
    Enhanced finger extension detection using angle calculation.
    Checks if finger is straight (angle > threshold degrees).
    
    Args:
        landmarks: MediaPipe hand landmarks
        finger_tip_id: ID of finger tip
        finger_pip_id: ID of finger PIP joint
        finger_mcp_id: ID of finger MCP joint
        threshold: Minimum angle for considering finger extended (default 140°)
    
    Returns:
        bool: True if finger is extended
    """
    angle = calculate_angle(
        landmarks[finger_mcp_id],
        landmarks[finger_pip_id],
        landmarks[finger_tip_id]
    )
    # More lenient: just check if finger is relatively straight
    return angle > threshold

def is_thumb_extended_up(landmarks):
    """Check if thumb is extended upward with high precision."""
    THUMB_TIP, THUMB_IP, THUMB_MCP, WRIST = 4, 3, 2, 0
    
    # Thumb tip should be above thumb IP joint
    tip_above_ip = landmarks[THUMB_TIP].y < landmarks[THUMB_IP].y
    # Thumb should be extended outward (x-distance check)
    thumb_out = abs(landmarks[THUMB_TIP].x - landmarks[WRIST].x) > 0.05
    
    return tip_above_ip and thumb_out

def is_thumb_extended_down(landmarks):
    """Check if thumb is extended downward with high precision."""
    THUMB_TIP, THUMB_IP, INDEX_PIP = 4, 3, 6
    
    # Thumb tip should be below thumb IP joint
    tip_below_ip = landmarks[THUMB_TIP].y > landmarks[THUMB_IP].y
    # Thumb should be below index PIP
    tip_below_index = landmarks[THUMB_TIP].y > landmarks[INDEX_PIP].y
    
    return tip_below_ip and tip_below_index

def detect_gesture(hand_landmarks):
    """
    PRECISION GESTURE DETECTION for accessibility.
    Designed for people with limited mobility - high accuracy, low false positives.
    
    Gestures:
    1. THUMB UP → Red LED (thumb extended up, all fingers closed)
    2. THUMB DOWN → Green LED (thumb extended down, all fingers closed)
    3. INDEX UP → Door Lock (only index finger extended)
    4. PEACE SIGN → TV (index + middle fingers extended)
    5. THREE FINGERS → Fan (index + middle + ring extended)
    
    Args:
        hand_landmarks: MediaPipe hand landmarks
    
    Returns:
        str: Gesture name or None
    """
    landmarks = hand_landmarks.landmark
    
    # MediaPipe landmark IDs
    THUMB_TIP, THUMB_IP, THUMB_MCP = 4, 3, 2
    INDEX_TIP, INDEX_PIP, INDEX_MCP = 8, 6, 5
    MIDDLE_TIP, MIDDLE_PIP, MIDDLE_MCP = 12, 10, 9
    RING_TIP, RING_PIP, RING_MCP = 16, 14, 13
    PINKY_TIP, PINKY_PIP, PINKY_MCP = 20, 18, 17
    WRIST = 0
    
    # High-precision finger extension detection
    thumb_up = is_thumb_extended_up(landmarks)
    thumb_down = is_thumb_extended_down(landmarks)
    index_extended = is_finger_extended(landmarks, INDEX_TIP, INDEX_PIP, INDEX_MCP, threshold=140)
    middle_extended = is_finger_extended(landmarks, MIDDLE_TIP, MIDDLE_PIP, MIDDLE_MCP, threshold=140)
    ring_extended = is_finger_extended(landmarks, RING_TIP, RING_PIP, RING_MCP, threshold=140)
    pinky_extended = is_finger_extended(landmarks, PINKY_TIP, PINKY_PIP, PINKY_MCP, threshold=140)
    
    # Count extended fingers (excluding thumb)
    fingers_extended = sum([index_extended, middle_extended, ring_extended, pinky_extended])
    
    # ===== GESTURE 1: THUMB UP (Red LED) =====
    # Only thumb extended upward, all other fingers closed
    if thumb_up and fingers_extended == 0 and not thumb_down:
        return "thumb_up"
    
    # ===== GESTURE 2: THUMB DOWN (Green LED) =====
    # Only thumb extended downward, all other fingers closed
    if thumb_down and fingers_extended == 0 and not thumb_up:
        return "thumb_down"
    
    # ===== GESTURE 3: INDEX FINGER UP (Door Lock) =====
    # Only index finger extended, thumb can be tucked or out
    if index_extended and not middle_extended and not ring_extended and not pinky_extended:
        return "index_up"
    
    # ===== GESTURE 4: PEACE SIGN / TWO FINGERS (TV) =====
    # Index and middle fingers extended, ring and pinky closed
    if index_extended and middle_extended and not ring_extended and not pinky_extended:
        return "peace_sign"
    
    # ===== GESTURE 5: THREE FINGERS (Fan) =====
    # Index, middle, and ring fingers extended, pinky closed
    if index_extended and middle_extended and ring_extended and not pinky_extended:
        return "three_fingers"
    
    return None

def debounce_gesture(gesture):
    """
    Apply debounce logic to prevent flickering from hand jitter.
    Only confirms gesture if detected consistently across multiple frames.
    
    Args:
        gesture: Currently detected gesture
    
    Returns:
        str: Confirmed gesture or None
    """
    gesture_history.append(gesture)
    
    if len(gesture_history) < DEBOUNCE_FRAMES:
        return None
    
    # Check if all recent frames show the same gesture
    if all(g == gesture for g in gesture_history):
        return gesture
    
    return None

# =============================================================================
# DEVICE CONTROL FUNCTIONS
# =============================================================================

def toggle_led(led_id):
    """
    Toggle the state of a specific device (LED, Fan, Door Lock, TV).
    
    Args:
        led_id: ID of the device to toggle
    """
    global led_states, TV_CHANNEL_INDEX
    
    if led_id in led_states:
        device_type = DEVICE_CONFIG[led_id].get('type', 'led')
        
        # Special handling for TV - cycles through channels when ON
        if device_type == 'tv':
            if not led_states[led_id]:
                led_states[led_id] = True
                TV_CHANNEL_INDEX[led_id] = 0
                print(f"✓ {DEVICE_CONFIG[led_id]['label']} is now ON (Channel: {TV_CHANNELS[0]})")
            else:
                TV_CHANNEL_INDEX[led_id] = (TV_CHANNEL_INDEX[led_id] + 1) % len(TV_CHANNELS)
                channel = TV_CHANNELS[TV_CHANNEL_INDEX[led_id]]
                print(f"✓ {DEVICE_CONFIG[led_id]['label']} - Channel: {channel}")
        else:
            led_states[led_id] = not led_states[led_id]
            state = "ON" if led_states[led_id] else "OFF"
            
            # Special labels for door lock
            if device_type == 'door_lock':
                state = "UNLOCKED" if led_states[led_id] else "LOCKED"
            
            print(f"✓ {DEVICE_CONFIG[led_id]['label']} is now {state}")

def process_gesture_action(gesture):
    """
    Process detected gesture and trigger corresponding LED action.
    
    Args:
        gesture: Detected gesture name
    """
    global last_gesture
    
    if gesture and gesture in GESTURE_TO_LED:
        # Only trigger if it's a new gesture (not repeated)
        if gesture != last_gesture:
            led_id = GESTURE_TO_LED[gesture]
            toggle_led(led_id)
            last_gesture = gesture
    elif gesture is None:
        # Reset when no gesture detected
        last_gesture = None

# =============================================================================
# WEBCAM PROCESSING THREAD
# =============================================================================

def webcam_processing_thread():
    """
    Main webcam processing thread - ULTRA STABLE VERSION.
    No freezing, no hangs - just pure frame processing.
    """
    global running
    
    print("🔄 Initializing webcam...")
    
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ ERROR: Cannot open webcam!")
        running = False
        return
    
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    print("✓ Webcam ready")
    print("🔄 Starting hand detection...")
    
    # Minimal window creation
    window_name = 'Virtual LED Controller - Webcam Feed'
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    
    hands = None
    try:
        hands = mp_hands.Hands(
            model_complexity=0,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
            max_num_hands=1
        )
        print("✓ Hand detection ready!")
        print("🎉 Running! Show your hand\n")
    except Exception as e:
        print(f"❌ Failed to load hand detection: {e}")
        cap.release()
        cv2.destroyAllWindows()
        running = False
        return
    
    frame_count = 0
    display_frame = None
    
    while running:
        try:
            # Read frame - if fails, skip
            ret, frame = cap.read()
            if not ret or frame is None:
                continue
            
            frame_count += 1
            frame = cv2.flip(frame, 1)
            h, w = frame.shape[:2]
            
            # Convert color ONLY when needed
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Process gesture (wrapped in try-except)
            try:
                results = hands.process(rgb)
                if results.multi_hand_landmarks:
                    for landmark in results.multi_hand_landmarks:
                        mp_drawing.draw_landmarks(frame, landmark, mp_hands.HAND_CONNECTIONS,
                                                mp_drawing_styles.get_default_hand_landmarks_style(),
                                                mp_drawing_styles.get_default_hand_connections_style())
                        
                        gesture = detect_gesture(landmark)
                        confirmed = debounce_gesture(gesture)
                        if confirmed:
                            process_gesture_action(confirmed)
                            cv2.putText(frame, f"Gesture: {confirmed.replace('_', ' ').title()}",
                                      (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            except:
                pass
            
            # Draw device states - fast version
            y = 70
            for dev_id, state in led_states.items():
                dev_type = DEVICE_CONFIG[dev_id].get('type', 'led')
                if dev_type == 'door_lock':
                    status = "UNLOCKED" if state else "LOCKED"
                    color = (0, 255, 0) if state else (0, 0, 255)
                else:
                    status = "ON" if state else "OFF"
                    color = (0, 255, 0) if state else (0, 0, 255)
                cv2.putText(frame, f"{DEVICE_CONFIG[dev_id]['label']}: {status}",
                          (10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                y += 25
            
            cv2.putText(frame, "Press 'q' to quit", (10, h - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
            # Display
            cv2.imshow(window_name, frame)
            
            # Non-blocking key check
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q') or key == 27:  # q or ESC
                break
                
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"⚠ Minor error: {e}")
            continue
    
    # Cleanup
    running = False
    try:
        cap.release()
        cv2.destroyAllWindows()
    except:
        pass
    if hands:
        hands.close()
    print("✓ Webcam closed")

# =============================================================================
# GUI FUNCTIONS
# =============================================================================

class LEDController:
    """
    Main GUI class for LED visualization and control.
    Creates a professional-looking interface with animated LEDs.
    """
    
    def __init__(self, root):
        """Initialize the Device Controller GUI."""
        self.root = root
        self.root.title(WINDOW_TITLE)
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.configure(bg='#1a1a1a')
        self.root.resizable(False, False)
        
        # Animation state
        self.animation_angle = 0
        
        # Create main frame
        self.main_frame = tk.Frame(root, bg='#1a1a1a')
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title and Settings Frame
        title_frame = tk.Frame(self.main_frame, bg='#1a1a1a')
        title_frame.pack(pady=(0, 10))
        
        title_label = tk.Label(
            title_frame,
            text="♿ Accessible Gesture Controller",
            font=('Arial', 22, 'bold'),
            bg='#1a1a1a',
            fg='#00FF00'
        )
        title_label.pack(side=tk.LEFT, padx=10)
        
        settings_btn = tk.Button(
            title_frame,
            text="⚙ Customize Gestures",
            font=('Arial', 10, 'bold'),
            bg='#2a2a2a',
            fg='#00FF00',
            command=self.show_settings,
            relief=tk.RAISED,
            padx=10,
            pady=5
        )
        settings_btn.pack(side=tk.LEFT, padx=10)
        
        # Subtitle
        subtitle_label = tk.Label(
            self.main_frame,
            text="Precision Control for Limited Mobility",
            font=('Arial', 11),
            bg='#1a1a1a',
            fg='#888888'
        )
        subtitle_label.pack(pady=(0, 30))
        
        # Create LED display area
        self.led_frame = tk.Frame(self.main_frame, bg='#1a1a1a')
        self.led_frame.pack(expand=True)
        
        # Create canvases for each device
        self.led_canvases = {}
        self.led_labels = {}
        self.glow_animation_ids = {}
        self.animation_angle = 0  # For animations
        
        # Calculate device layout (3 rows x 2 columns for 5 devices)
        rows = 3
        cols = 2
        device_ids = list(DEVICE_CONFIG.keys())
        
        for idx, device_id in enumerate(device_ids):
            row = idx // cols
            col = idx % cols
            
            # Create frame for each device
            device_container = tk.Frame(self.led_frame, bg='#1a1a1a')
            device_container.grid(row=row, column=col, padx=30, pady=15)
            
            # Device label
            label = tk.Label(
                device_container,
                text=DEVICE_CONFIG[device_id]['label'],
                font=('Arial', 12, 'bold'),
                bg='#1a1a1a',
                fg='#FFFFFF'
            )
            label.pack()
            
            # Device canvas
            canvas = tk.Canvas(
                device_container,
                width=DEVICE_SIZE,
                height=DEVICE_SIZE,
                bg='#1a1a1a',
                highlightthickness=0
            )
            canvas.pack(pady=(5, 5))
            
            # Status label
            device_type = DEVICE_CONFIG[device_id].get('type', 'led')
            if device_type == 'door_lock':
                status_text = "LOCKED"
            else:
                status_text = "OFF"
            
            status_label = tk.Label(
                device_container,
                text=status_text,
                font=('Arial', 10, 'bold'),
                bg='#1a1a1a',
                fg='#FF0000'
            )
            status_label.pack()
            
            self.led_canvases[device_id] = canvas
            self.led_labels[device_id] = status_label
        
        # Instructions panel
        instruction_frame = tk.Frame(self.main_frame, bg='#2a2a2a', relief=tk.RIDGE, bd=2)
        instruction_frame.pack(fill=tk.X, pady=(20, 0))
        
        instructions_text = "♿ Accessibility Mode | 👍Thumb Up=LED1 | 👎Thumb Down=LED2 | ☝Index=Lock | ✌Two Fingers=TV | 🤟Three Fingers=Fan"
        instruction_label = tk.Label(
            instruction_frame,
            text=instructions_text,
            font=('Arial', 9, 'bold'),
            bg='#2a2a2a',
            fg='#00FF00',
            pady=10
        )
        instruction_label.pack()
        
        # Start GUI update loop
        self.update_leds()
    
    def draw_device(self, canvas, device_id, state, size=DEVICE_SIZE):
        """
        Draw device visualization based on device type.
        
        Args:
            canvas: Tkinter canvas to draw on
            device_id: ID of the device
            state: Current state (ON/OFF)
            size: Size of the display
        """
        canvas.delete("all")
        center = size // 2
        device_type = DEVICE_CONFIG[device_id].get('type', 'led')
        color = DEVICE_CONFIG[device_id]['color_on'] if state else DEVICE_CONFIG[device_id]['color_off']
        
        if device_type == 'led':
            # Draw LED with glow effect
            if state and LED_GLOW_EFFECT:
                for i in range(3):
                    radius = center - (i * 8)
                    canvas.create_oval(center - radius, center - radius, center + radius, center + radius, fill=color, outline='')
            radius = center - 10
            canvas.create_oval(center - radius, center - radius, center + radius, center + radius, fill=color, outline='#555555', width=2)
        
        elif device_type == 'fan':
            # Draw rotating fan blades
            if state:
                for i in range(3):
                    blade_angle = self.animation_angle + (i * 120)
                    import math
                    x1 = center + math.cos(math.radians(blade_angle)) * 10
                    y1 = center + math.sin(math.radians(blade_angle)) * 10
                    x2 = center + math.cos(math.radians(blade_angle)) * (center - 10)
                    y2 = center + math.sin(math.radians(blade_angle)) * (center - 10)
                    canvas.create_line(x1, y1, x2, y2, fill=color, width=6)
            canvas.create_oval(center - 30, center - 30, center + 30, center + 30, outline=color, width=3)
            canvas.create_oval(center - 5, center - 5, center + 5, center + 5, fill=color)
        
        elif device_type == 'buzzer':
            # Draw speaker/buzzer with sound waves
            canvas.create_rectangle(center - 20, center - 25, center + 20, center + 25, fill=color, outline='#555555', width=2)
            if state:
                for i in range(1, 4):
                    canvas.create_arc(center + 20, center - i*10, center + 20 + i*15, center + i*10, 
                                    start=270, extent=180, outline=color, width=2, style='arc')
        
        elif device_type == 'rgb_strip':
            # Draw RGB LED strip
            strip_width = size - 20
            led_count = 5
            led_spacing = strip_width // led_count
            for i in range(led_count):
                x = 10 + i * led_spacing
                canvas.create_rectangle(x, center - 10, x + led_spacing - 5, center + 10, 
                                      fill=color if state else DEVICE_CONFIG[device_id]['color_off'], 
                                      outline='#555555', width=1)
        
        elif device_type == 'door_lock':
            # Draw lock/unlock symbol
            if state:  # Unlocked (open)
                canvas.create_arc(center - 15, center - 30, center + 15, center - 10, 
                                start=180, extent=180, outline=color, width=4, style='arc')
                canvas.create_rectangle(center - 20, center - 10, center + 20, center + 20, 
                                      fill=color, outline='#555555', width=2)
                canvas.create_oval(center - 3, center, center + 3, center + 6, fill='#1a1a1a')
            else:  # Locked (closed)
                canvas.create_arc(center - 15, center - 35, center + 15, center - 5, 
                                start=0, extent=180, outline=color, width=4, style='arc')
                canvas.create_rectangle(center - 20, center - 10, center + 20, center + 20, 
                                      fill=color, outline='#555555', width=2)
                canvas.create_oval(center - 3, center, center + 3, center + 6, fill='#1a1a1a')
        
        elif device_type == 'tv':
            # Draw TV with screen and frame
            # TV frame (bezel)
            canvas.create_rectangle(5, 5, size-5, size-5, fill='#333333', outline='#666666', width=3)
            
            if state:  # TV ON - show channel
                # Screen background
                canvas.create_rectangle(15, 15, size-15, size-25, fill='#000055', outline='')
                # Channel text
                channel_idx = TV_CHANNEL_INDEX.get(device_id, 0)
                channel_name = TV_CHANNELS[channel_idx]
                canvas.create_text(center, center - 10, text=channel_name, 
                                 fill=color, font=('Arial', 10, 'bold'))
                # Animated scan lines for TV effect
                for i in range(5):
                    y = 20 + (i * 15) + (self.animation_angle // 10) % 15
                    if y < size - 25:
                        canvas.create_line(15, y, size-15, y, fill='#ffffff', width=1)
                # Power indicator LED
                canvas.create_oval(center - 3, size - 15, center + 3, size - 9, fill='#00FF00')
            else:  # TV OFF - show static
                # Dark screen with static noise pattern
                canvas.create_rectangle(15, 15, size-15, size-25, fill='#1a1a1a', outline='')
                # Random static dots
                import random
                random.seed(int(self.animation_angle / 10))
                for _ in range(30):
                    x = random.randint(15, size-15)
                    y = random.randint(15, size-25)
                    gray = random.choice(['#333333', '#555555', '#777777'])
                    canvas.create_rectangle(x, y, x+2, y+2, fill=gray, outline='')
                # Power indicator LED (red when off)
                canvas.create_oval(center - 3, size - 15, center + 3, size - 9, fill='#FF0000')
    
    def draw_led(self, canvas, color, size=LED_SIZE, glow=False):
        """Legacy function - calls draw_device for backward compatibility"""
        canvas.delete("all")
        center = size // 2
        if glow and LED_GLOW_EFFECT:
            for i in range(3):
                radius = center - (i * 8)
                canvas.create_oval(center - radius, center - radius, center + radius, center + radius, fill=color, outline='')
        radius = center - 10
        canvas.create_oval(center - radius, center - radius, center + radius, center + radius, fill=color, outline='#555555', width=2)
    
    def show_settings(self):
        """Open settings window to customize gesture mappings."""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("⚙ Customize Gestures")
        settings_window.geometry("600x500")
        settings_window.configure(bg='#1a1a1a')
        
        # Title
        title = tk.Label(
            settings_window,
            text="Gesture Customization",
            font=('Arial', 18, 'bold'),
            bg='#1a1a1a',
            fg='#00FF00'
        )
        title.pack(pady=20)
        
        # Info text
        info = tk.Label(
            settings_window,
            text="Current gesture mappings. Edit gesture_config.json to customize.",
            font=('Arial', 10),
            bg='#1a1a1a',
            fg='#AAAAAA'
        )
        info.pack(pady=5)
        
        # Mappings frame
        mappings_frame = tk.Frame(settings_window, bg='#2a2a2a', relief=tk.RIDGE, bd=2)
        mappings_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)
        
        # Display current mappings
        row = 0
        for gesture, device_id in GESTURE_TO_LED.items():
            device_name = DEVICE_CONFIG[device_id]['label']
            
            gesture_label = tk.Label(
                mappings_frame,
                text=f"🖐 {gesture.replace('_', ' ').title()}",
                font=('Arial', 12, 'bold'),
                bg='#2a2a2a',
                fg='#FFFFFF',
                width=20,
                anchor='w'
            )
            gesture_label.grid(row=row, column=0, padx=10, pady=8, sticky='w')
            
            arrow_label = tk.Label(
                mappings_frame,
                text="→",
                font=('Arial', 14, 'bold'),
                bg='#2a2a2a',
                fg='#00FF00'
            )
            arrow_label.grid(row=row, column=1, padx=5, pady=8)
            
            device_label = tk.Label(
                mappings_frame,
                text=device_name,
                font=('Arial', 12),
                bg='#2a2a2a',
                fg='#FFD700',
                width=20,
                anchor='w'
            )
            device_label.grid(row=row, column=2, padx=10, pady=8, sticky='w')
            
            row += 1
        
        # Buttons
        button_frame = tk.Frame(settings_window, bg='#1a1a1a')
        button_frame.pack(pady=10)
        
        save_btn = tk.Button(
            button_frame,
            text="💾 Save to File",
            font=('Arial', 11, 'bold'),
            bg='#00AA00',
            fg='#FFFFFF',
            command=lambda: [save_custom_gestures(), settings_window.focus()],
            padx=15,
            pady=8
        )
        save_btn.pack(side=tk.LEFT, padx=10)
        
        close_btn = tk.Button(
            button_frame,
            text="✖ Close",
            font=('Arial', 11, 'bold'),
            bg='#AA0000',
            fg='#FFFFFF',
            command=settings_window.destroy,
            padx=15,
            pady=8
        )
        close_btn.pack(side=tk.LEFT, padx=10)
        
        # Help text
        help_text = tk.Label(
            settings_window,
            text="To customize: Edit gesture_config.json file and restart the application",
            font=('Arial', 9, 'italic'),
            bg='#1a1a1a',
            fg='#888888'
        )
        help_text.pack(pady=5)
    
    def update_leds(self):
        """Update all LED displays based on current states."""
        for led_id, state in led_states.items():
            if led_id in self.led_canvases:
                canvas = self.led_canvases[led_id]
                label = self.led_labels[led_id]
                device_type = DEVICE_CONFIG[led_id].get('type', 'led')
                
                # Draw device with appropriate visualization
                self.draw_device(canvas, led_id, state)
                
                # Update status label based on device type
                if device_type == 'door_lock':
                    if state:
                        label.config(text="UNLOCKED", fg='#00FF00')
                    else:
                        label.config(text="LOCKED", fg='#FF0000')
                elif device_type == 'tv':
                    if state:
                        channel_idx = TV_CHANNEL_INDEX.get(led_id, 0)
                        label.config(text=f"📺 {TV_CHANNELS[channel_idx]}", fg='#00FF00')
                    else:
                        label.config(text="OFF", fg='#FF0000')
                else:
                    if state:
                        label.config(text="ON", fg='#00FF00')
                    else:
                        label.config(text="OFF", fg='#FF0000')
        
        # Update animation angle for rotating devices (fan)
        self.animation_angle = (self.animation_angle + 15) % 360
        
        # Schedule next update
        if running:
            self.root.after(50, self.update_leds)
    
    def on_closing(self):
        """Handle window close event."""
        global running
        running = False
        self.root.destroy()

def start_gui():
    """Start the Tkinter GUI."""
    root = tk.Tk()
    app = LEDController(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    """
    Main function to start the application.
    Launches webcam processing and GUI in separate threads.
    """
    print("=" * 75)
    print("♿ ACCESSIBLE GESTURE CONTROLLER - FOR LIMITED MOBILITY")
    print("=" * 75)
    print("✓ Starting application with precision gesture detection...")
    print(f"✓ Detected {len(DEVICE_CONFIG)} devices: ", end="")
    device_types = {}
    for d in DEVICE_CONFIG.values():
        dtype = d.get('type', 'led')
        device_types[dtype] = device_types.get(dtype, 0) + 1
    print(", ".join([f"{count} {dtype.upper()}" for dtype, count in device_types.items()]))
    print(f"✓ Loaded {len(GESTURE_TO_LED)} precise gesture mappings")
    print("✓ Voice feedback:", "ENABLED" if VOICE_ENABLED else "DISABLED")
    print(f"✓ Config file: {CONFIG_FILE}", "(Custom)" if os.path.exists(CONFIG_FILE) else "(Default)")
    print("\n📋 GESTURE MAPPINGS (High Precision):")
    gestures_info = {
        'thumb_up': '👍 Thumb Up',
        'thumb_down': '👎 Thumb Down', 
        'index_up': '☝ Index Finger',
        'peace_sign': '✌ Two Fingers',
        'three_fingers': '🤟 Three Fingers'
    }
    for gesture, device_id in GESTURE_TO_LED.items():
        gesture_display = gestures_info.get(gesture, gesture.replace('_', ' ').title())
        device_info = DEVICE_CONFIG[device_id]['label']
        print(f"   {gesture_display:20} → {device_info}")
    print("\n⚠ Press 'q' in webcam window to quit")
    print("💡 Click 'Customize Gestures' button to change mappings")
    print("=" * 75)
    print()
    
    # Start webcam processing in separate thread
    webcam_thread = threading.Thread(target=webcam_processing_thread, daemon=True)
    webcam_thread.start()
    
    # Start GUI in main thread
    start_gui()
    
    # Cleanup
    global running
    running = False
    print("\n✓ Application closed successfully")
    print("=" * 70)

if __name__ == "__main__":
    main()
