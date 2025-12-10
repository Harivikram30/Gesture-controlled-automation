"""
Quick Webcam Test - Run this first to check if your camera works
"""
import cv2
import time

def test_webcam():
    print("🔍 Testing webcam connection...")
    
    # Try different camera indices
    for camera_id in [0, 1, -1]:
        print(f"  Trying camera {camera_id}...")
        
        try:
            cap = cv2.VideoCapture(camera_id)
            
            if cap.isOpened():
                # Test if camera actually captures frames
                ret, frame = cap.read()
                if ret and frame is not None:
                    print(f"  ✅ Camera {camera_id} WORKING!")
                    
                    # Show a test window for 5 seconds
                    print("  📹 Opening test window for 5 seconds...")
                    
                    start_time = time.time()
                    while time.time() - start_time < 5:
                        ret, frame = cap.read()
                        if ret:
                            cv2.imshow(f'Camera Test - Camera {camera_id}', frame)
                            if cv2.waitKey(1) & 0xFF == ord('q'):
                                break
                    
                    cap.release()
                    cv2.destroyAllWindows()
                    
                    print(f"  ✅ Camera {camera_id} test successful!")
                    return camera_id
                else:
                    print(f"  ❌ Camera {camera_id} opened but no frames")
                    cap.release()
            else:
                print(f"  ❌ Camera {camera_id} failed to open")
                
        except Exception as e:
            print(f"  ⚠️ Camera {camera_id} error: {e}")
    
    print("❌ No working camera found!")
    print("\n💡 Troubleshooting:")
    print("  1. Close any other apps using the camera (Zoom, Teams, etc.)")
    print("  2. Check Windows Camera privacy settings")
    print("  3. Try unplugging and reconnecting USB cameras")
    print("  4. Restart your computer")
    return None

if __name__ == "__main__":
    working_camera = test_webcam()
    if working_camera is not None:
        print(f"\n🎉 SUCCESS: Camera {working_camera} is ready!")
        print("You can now run the main application: python virtual_led_controller.py")
    else:
        print("\n❌ FAILED: No working camera detected")