import cv2
import numpy as np

def test_single_camera(camera_index):
    """Test a single camera"""
    print(f"Testing camera {camera_index}...")
    
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        print(f"❌ Camera {camera_index} could not be opened")
        return False
    
    # Try to read a frame
    ret, frame = cap.read()
    if not ret:
        print(f"❌ Camera {camera_index} could not read frames")
        cap.release()
        return False
    
    print(f"✅ Camera {camera_index} is working")
    print(f"   Frame size: {frame.shape}")
    
    # Show the camera for a few seconds
    print(f"Showing camera {camera_index} for 5 seconds...")
    print("Press 'q' in the window to stop early")
    
    for i in range(150):  # 5 seconds at 30fps
        ret, frame = cap.read()
        if ret:
            # Add text to frame
            cv2.putText(frame, f"Camera {camera_index}", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.putText(frame, "Press 'q' to stop", (10, 70), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            cv2.imshow(f'Camera {camera_index} Test', frame)
        
        # Check for quit
        if cv2.waitKey(33) & 0xFF == ord('q'):  # 33ms = ~30fps
            break
    
    cap.release()
    cv2.destroyAllWindows()
    return True

def main():
    """Test both cameras individually"""
    print("Camera Test")
    print("=" * 30)
    
    # Test integrated camera (0)
    print("\n1. Testing Integrated Camera (index 0)")
    integrated_works = test_single_camera(0)
    
    # Test USB camera (1)
    print("\n2. Testing USB Camera (index 1)")
    usb_works = test_single_camera(1)
    
    # Summary
    print("\n" + "=" * 30)
    print("TEST RESULTS:")
    print("=" * 30)
    print(f"Integrated Camera (0): {'✅ Working' if integrated_works else '❌ Failed'}")
    print(f"USB Camera (1): {'✅ Working' if usb_works else '❌ Failed'}")
    
    if integrated_works and usb_works:
        print("\n✅ Both cameras are working!")
        print("You can now run: python two_camera_stream.py")
    else:
        print("\n❌ Some cameras failed to work.")
        print("Check your camera connections and drivers.")

if __name__ == "__main__":
    main() 