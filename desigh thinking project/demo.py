"""
Demo Script for Virtual AI LED Controller
==========================================

This script runs an automated demo of the LED controller,
showcasing all features without requiring manual gestures.

Usage: python demo.py

Note: This simulates gestures programmatically for demonstration purposes.
"""

import time
import sys
from collections import deque

# Simulate the main application components
led_states = {
    "LED1": False,
    "LED2": False,
    "LED3": False,
    "LED4": False,
    "LED5": False,
    "LED6": False,
}

gesture_queue = deque([
    "thumb_up",
    "index_up",
    "peace_sign",
    "fist",
    "open_palm",
    "thumb_down",
])

gesture_descriptions = {
    "thumb_up": "👍 Thumbs Up",
    "thumb_down": "👎 Thumbs Down",
    "index_up": "☝ Index Finger Up",
    "fist": "✊ Closed Fist",
    "peace_sign": "✌ Peace Sign",
    "open_palm": "🖐 Open Palm",
}

led_names = {
    "LED1": "Green LED",
    "LED2": "Red LED",
    "LED3": "Blue LED",
    "LED4": "Yellow LED",
    "LED5": "Magenta LED",
    "LED6": "Cyan LED",
}

def print_banner():
    """Print demo banner."""
    print("\n" + "="*70)
    print("🎮 VIRTUAL AI LED CONTROLLER - AUTOMATED DEMO")
    print("="*70)
    print()

def print_led_states():
    """Print current LED states."""
    print("\n📊 Current LED States:")
    print("-" * 40)
    for led_id, state in led_states.items():
        status = "🟢 ON " if state else "⚫ OFF"
        print(f"  {led_names[led_id]:15} : {status}")
    print("-" * 40)

def simulate_gesture(gesture):
    """Simulate a gesture detection."""
    print(f"\n🤖 Simulating gesture: {gesture_descriptions[gesture]}")
    time.sleep(1)
    
    # Map gesture to LED
    gesture_to_led = {
        "thumb_up": "LED1",
        "thumb_down": "LED2",
        "index_up": "LED3",
        "fist": "LED4",
        "peace_sign": "LED5",
        "open_palm": "LED6",
    }
    
    led_id = gesture_to_led[gesture]
    
    # Toggle LED
    led_states[led_id] = not led_states[led_id]
    state_text = "ON" if led_states[led_id] else "OFF"
    
    print(f"✓ {led_names[led_id]} is now {state_text}")
    time.sleep(0.5)

def run_demo():
    """Run the automated demo."""
    print_banner()
    
    print("This demo simulates the gesture detection system.")
    print("In the real application, you would use your webcam and hands!\n")
    
    input("Press ENTER to start the demo...")
    
    # Show initial state
    print("\n📋 Step 1: Initial State")
    print("All LEDs are OFF")
    print_led_states()
    time.sleep(2)
    
    # Demonstrate each gesture
    print("\n📋 Step 2: Testing Each Gesture")
    print("Let's control each LED with a different gesture...\n")
    time.sleep(2)
    
    step = 3
    for gesture in gesture_queue:
        print(f"\n📋 Step {step}: {gesture_descriptions[gesture]}")
        simulate_gesture(gesture)
        print_led_states()
        time.sleep(1.5)
        step += 1
    
    # Toggle all off
    print(f"\n📋 Step {step}: Toggle All LEDs Off")
    print("Making the same gestures again to turn LEDs OFF...\n")
    time.sleep(2)
    
    step += 1
    for gesture in gesture_queue:
        print(f"\n📋 Step {step}: {gesture_descriptions[gesture]} (again)")
        simulate_gesture(gesture)
        print_led_states()
        time.sleep(1.5)
        step += 1
    
    # Final summary
    print("\n" + "="*70)
    print("✅ DEMO COMPLETE!")
    print("="*70)
    print("\n🎯 What you just saw:")
    print("  • 6 different hand gestures")
    print("  • Each gesture controls a specific LED")
    print("  • Gesture detected → LED toggles (ON/OFF)")
    print("  • Real-time visual feedback")
    print("\n🚀 To run the real application with webcam:")
    print("  python virtual_led_controller.py")
    print("\n📚 For more information:")
    print("  • README.md - Full documentation")
    print("  • QUICK_START.md - Getting started guide")
    print("  • CUSTOMIZATION_GUIDE.md - How to customize")
    print("\n" + "="*70)

if __name__ == "__main__":
    try:
        run_demo()
    except KeyboardInterrupt:
        print("\n\n⚠ Demo interrupted by user")
        print("Goodbye! 👋")
        sys.exit(0)
