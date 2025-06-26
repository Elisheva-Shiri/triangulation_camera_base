import cv2
import pygame
import os
import threading
import time
from datetime import datetime
import numpy as np

class MultiCameraRecorder:
    def __init__(self):
        self.cameras = {}
        self.camera_names = {}
        self.recording = False
        self.video_writers = {}
        self.fps = 30.0
        self.frame_size = (640, 480)
        
        # Initialize pygame for keyboard input
        pygame.init()
        self.screen = pygame.display.set_mode((1, 1))
        pygame.display.set_caption("Multi-Camera Recorder")
        
        # Create data directory if it doesn't exist
        if not os.path.exists('data'):
            os.makedirs('data')
    
    def detect_cameras(self):
        """Detect all available cameras"""
        print("Detecting cameras...")
        camera_index = 0
        detected_cameras = []
        
        while True:
            cap = cv2.VideoCapture(camera_index)
            if not cap.isOpened():
                break
            
            ret, frame = cap.read()
            if ret:
                detected_cameras.append(camera_index)
                print(f"Camera {camera_index} detected")
            
            cap.release()
            camera_index += 1
        
        return detected_cameras
    
    def get_camera_names(self, camera_indices):
        """Ask user to name each camera with better feedback"""
        print("\n" + "="*50)
        print("CAMERA NAMING PHASE")
        print("="*50)
        print("You will see each camera briefly. Enter a name for each one.")
        print("Press Enter after typing each name.")
        print("="*50)
        
        for i, camera_idx in enumerate(camera_indices):
            print(f"\nShowing Camera {camera_idx} ({i+1}/{len(camera_indices)})")
            
            cap = cv2.VideoCapture(camera_idx)
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.frame_size[0])
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.frame_size[1])
            
            # Show camera feed for 3 seconds with countdown
            for countdown in range(3, 0, -1):
                ret, frame = cap.read()
                if ret:
                    # Add countdown text to frame
                    display_frame = frame.copy()
                    cv2.putText(display_frame, f"Camera {camera_idx} - {countdown}", 
                               (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    cv2.putText(display_frame, "Enter name in terminal", 
                               (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                    cv2.imshow(f'Camera {camera_idx}', display_frame)
                    cv2.waitKey(1000)  # Show for 1 second
            
            cv2.destroyAllWindows()
            
            # Get user input for camera name
            while True:
                camera_name = input(f"Enter name for Camera {camera_idx} (e.g., 'front', 'side', 'top'): ").strip()
                if camera_name:
                    self.camera_names[camera_idx] = camera_name
                    print(f"✓ Camera {camera_idx} named: {camera_name}")
                    break
                else:
                    print("Please enter a valid name.")
            
            cap.release()
        
        print("\n" + "="*50)
        print("CAMERA NAMING COMPLETED")
        print("="*50)
        for camera_idx, name in self.camera_names.items():
            print(f"Camera {camera_idx}: {name}")
        print("="*50)
    
    def create_camera_folders(self):
        """Create folders for each camera in the data directory"""
        for camera_idx, camera_name in self.camera_names.items():
            folder_path = os.path.join('data', camera_name)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
                print(f"Created folder: {folder_path}")
    
    def initialize_cameras(self):
        """Initialize all cameras with optimized settings"""
        print("Initializing cameras...")
        for camera_idx in self.camera_names.keys():
            cap = cv2.VideoCapture(camera_idx)
            
            # Set camera properties for better performance
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.frame_size[0])
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.frame_size[1])
            cap.set(cv2.CAP_PROP_FPS, self.fps)
            cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Reduce buffer size for lower latency
            
            # Try to set additional properties for better performance
            cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
            
            self.cameras[camera_idx] = cap
            print(f"✓ Camera {camera_idx} ({self.camera_names[camera_idx]}) initialized")
    
    def start_recording(self, trial_name):
        """Start recording for all cameras"""
        if self.recording:
            print("Already recording!")
            return
        
        self.recording = True
        self.video_writers = {}
        
        # Create video writers for each camera
        for camera_idx, camera_name in self.camera_names.items():
            filename = f"{trial_name}_{camera_name}.mp4"
            filepath = os.path.join('data', camera_name, filename)
            
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            writer = cv2.VideoWriter(filepath, fourcc, self.fps, self.frame_size)
            self.video_writers[camera_idx] = writer
        
        print(f"🎥 Started recording trial: {trial_name}")
    
    def stop_recording(self):
        """Stop recording for all cameras"""
        if not self.recording:
            print("Not currently recording!")
            return
        
        self.recording = False
        
        # Release all video writers
        for writer in self.video_writers.values():
            writer.release()
        
        self.video_writers = {}
        print("⏹️  Recording stopped. Videos saved.")
    
    def display_cameras(self):
        """Display all camera feeds in a grid with improved performance"""
        if not self.cameras:
            return
        
        # Calculate grid layout
        num_cameras = len(self.cameras)
        cols = min(3, num_cameras)  # Max 3 columns
        rows = (num_cameras + cols - 1) // cols
        
        # Create display window
        display_width = self.frame_size[0] * cols
        display_height = self.frame_size[1] * rows
        display = np.zeros((display_height, display_width, 3), dtype=np.uint8)
        
        # Capture and place frames with error handling
        frames = {}
        for camera_idx, cap in self.cameras.items():
            try:
                ret, frame = cap.read()
                if ret and frame is not None:
                    frames[camera_idx] = frame
            except Exception as e:
                print(f"Error reading from camera {camera_idx}: {e}")
                continue
        
        # Arrange frames in grid
        for i, (camera_idx, frame) in enumerate(frames.items()):
            row = i // cols
            col = i % cols
            
            y_start = row * self.frame_size[1]
            y_end = y_start + self.frame_size[1]
            x_start = col * self.frame_size[0]
            x_end = x_start + self.frame_size[0]
            
            # Resize frame if necessary
            if frame.shape[:2] != self.frame_size[::-1]:
                frame = cv2.resize(frame, self.frame_size)
            
            display[y_start:y_end, x_start:x_end] = frame
            
            # Add camera name label
            camera_name = self.camera_names[camera_idx]
            cv2.putText(display, camera_name, 
                       (x_start + 10, y_start + 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            
            # Add recording indicator
            if self.recording:
                cv2.putText(display, "REC", 
                           (x_start + 10, y_start + 60), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        
        # Add status text
        status_text = f"Recording: {'ON' if self.recording else 'OFF'} | Press 's' to start, 'e' to stop, 'q' to quit"
        cv2.putText(display, status_text, (10, display_height - 20), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        cv2.imshow('Multi-Camera Recorder', display)
        
        # Write frames if recording
        if self.recording:
            for camera_idx, frame in frames.items():
                if camera_idx in self.video_writers:
                    try:
                        self.video_writers[camera_idx].write(frame)
                    except Exception as e:
                        print(f"Error writing to video for camera {camera_idx}: {e}")
    
    def handle_keyboard_input(self):
        """Handle keyboard input using pygame"""
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s and not self.recording:
                    trial_name = input("Enter trial name: ").strip()
                    if trial_name:
                        self.start_recording(trial_name)
                    else:
                        print("Please enter a valid trial name.")
                
                elif event.key == pygame.K_e and self.recording:
                    self.stop_recording()
                
                elif event.key == pygame.K_q:
                    return False
        
        return True
    
    def cleanup(self):
        """Clean up resources"""
        self.stop_recording()
        
        for cap in self.cameras.values():
            cap.release()
        
        cv2.destroyAllWindows()
        pygame.quit()
    
    def run(self):
        """Main run loop with improved flow"""
        try:
            # Detect cameras
            camera_indices = self.detect_cameras()
            
            if not camera_indices:
                print("No cameras detected!")
                return
            
            print(f"Found {len(camera_indices)} camera(s)")
            
            # Get camera names from user
            self.get_camera_names(camera_indices)
            
            # Create folders
            self.create_camera_folders()
            
            # Initialize cameras
            self.initialize_cameras()
            
            print("\n" + "="*50)
            print("MULTI-CAMERA RECORDER - READY")
            print("="*50)
            print("Controls:")
            print("  's' - Start recording")
            print("  'e' - Stop recording")
            print("  'q' - Quit")
            print("="*50)
            print("Displaying camera feeds...")
            print("="*50)
            
            # Main loop
            running = True
            while running:
                # Display cameras
                self.display_cameras()
                
                # Handle keyboard input
                running = self.handle_keyboard_input()
                
                # Check for OpenCV window close
                if cv2.getWindowProperty('Multi-Camera Recorder', cv2.WND_PROP_VISIBLE) < 1:
                    break
                
                # Small delay to prevent high CPU usage
                time.sleep(0.03)
        
        except KeyboardInterrupt:
            print("\nInterrupted by user")
        
        finally:
            self.cleanup()

if __name__ == "__main__":
    recorder = MultiCameraRecorder()
    recorder.run() 