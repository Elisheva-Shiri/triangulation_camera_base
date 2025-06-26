#!/usr/bin/env python3
"""
Test script to verify installation and camera detection
"""

import sys
import cv2
import pygame
import numpy as np

def test_dependencies():
    """Test if all required dependencies are installed"""
    print("Testing dependencies...")
    
    try:
        import cv2
        print(f"✓ OpenCV version: {cv2.__version__}")
    except ImportError:
        print("✗ OpenCV not found. Install with: pip install opencv-python")
        return False
    
    try:
        import pygame
        print(f"✓ Pygame version: {pygame.version.ver}")
    except ImportError:
        print("✗ Pygame not found. Install with: pip install pygame")
        return False
    
    try:
        import numpy
        print(f"✓ NumPy version: {numpy.__version__}")
    except ImportError:
        print("✗ NumPy not found. Install with: pip install numpy")
        return False
    
    return True

def test_camera_detection():
    """Test camera detection"""
    print("\nTesting camera detection...")
    
    detected_cameras = []
    camera_index = 0
    
    while True:
        cap = cv2.VideoCapture(camera_index)
        if not cap.isOpened():
            break
        
        ret, frame = cap.read()
        if ret:
            detected_cameras.append(camera_index)
            print(f"✓ Camera {camera_index} detected")
            
            # Try to get camera properties
            width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
            height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
            fps = cap.get(cv2.CAP_PROP_FPS)
            print(f"  Resolution: {width:.0f}x{height:.0f}, FPS: {fps:.1f}")
        else:
            print(f"✗ Camera {camera_index} found but cannot read frames")
        
        cap.release()
        camera_index += 1
    
    if not detected_cameras:
        print("✗ No cameras detected!")
        return False
    
    print(f"\nTotal cameras detected: {len(detected_cameras)}")
    return True

def test_pygame_input():
    """Test pygame input handling"""
    print("\nTesting pygame input...")
    
    try:
        pygame.init()
        screen = pygame.display.set_mode((1, 1))
        pygame.display.set_caption("Test")
        
        # Test for a short time
        import time
        start_time = time.time()
        while time.time() - start_time < 2:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    print(f"✓ Key pressed: {event.key}")
        
        pygame.quit()
        print("✓ Pygame input test completed")
        return True
    except Exception as e:
        print(f"✗ Pygame test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("="*50)
    print("MULTI-CAMERA RECORDER - INSTALLATION TEST")
    print("="*50)
    
    # Test dependencies
    if not test_dependencies():
        print("\n❌ Dependency test failed. Please install missing packages.")
        sys.exit(1)
    
    # Test camera detection
    if not test_camera_detection():
        print("\n⚠️  Camera detection failed. Check camera connections.")
    
    # Test pygame
    if not test_pygame_input():
        print("\n⚠️  Pygame test failed. Check display settings.")
    
    print("\n" + "="*50)
    print("TEST COMPLETED")
    print("="*50)
    
    if test_dependencies():
        print("✅ Ready to run multi_camera_recorder.py")
        print("\nTo start recording:")
        print("  python multi_camera_recorder.py")
    else:
        print("❌ Please fix the issues above before running the recorder")

if __name__ == "__main__":
    main() 