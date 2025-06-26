import cv2
import os
import time
import numpy as np
from datetime import datetime
import logging

# Disable OpenCV warnings
os.environ["OPENCV_LOG_LEVEL"] = "OFF"
logging.getLogger("cv2").setLevel(logging.ERROR)

class MultiCameraRecorder:
    def __init__(self):
        self.cameras = {}  # {index: VideoCapture}
        self.camera_names = {}  # {index: "name"}
        self.video_writers = {}
        self.recording = False
        self.fps = 30.0
        self.frame_size = (640, 480)  # fallback if can't read real size

        if not os.path.exists("data"):
            os.makedirs("data")

    def detect_cameras(self, max_test=10):
        print("Detecting connected cameras (may take a few seconds)...")
        detected = []
        
        # Try different camera indices with different APIs
        for i in range(max_test):
            # Try DirectShow first
            try:
                cap = cv2.VideoCapture(i + cv2.CAP_DSHOW)
                if cap.isOpened():
                    print(f"  → Trying camera index {i} with DirectShow...")
                    time.sleep(1)
                    ret, frame = cap.read()
                    if ret and frame is not None:
                        print(f"  ✓ Camera {i} is working (DirectShow)")
                        detected.append(i)
                    cap.release()
                    continue
            except Exception:
                pass

            # Fallback to default API
            try:
                cap = cv2.VideoCapture(i)
                if cap.isOpened():
                    print(f"  → Trying camera index {i} with default API...")
                    time.sleep(1)
                    ret, frame = cap.read()
                    if ret and frame is not None and i not in detected:
                        print(f"  ✓ Camera {i} is working (default)")
                        detected.append(i)
                    cap.release()
            except Exception:
                continue

        return detected

    def get_camera_names(self, indices):
        for idx in indices:
            try:
                # Try DirectShow first
                cap = cv2.VideoCapture(idx + cv2.CAP_DSHOW)
                if not cap.isOpened():
                    # Fallback to default
                    cap = cv2.VideoCapture(idx)
                
                if not cap.isOpened():
                    print(f"Could not open camera {idx}")
                    continue
                    
                cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                time.sleep(1)
                print(f"\nPreviewing camera {idx}...")

                success = False
                for _ in range(5):  # Try up to 5 times to get a frame
                    ret, frame = cap.read()
                    if ret:
                        h, w = frame.shape[:2]
                        print(f"  Resolution: {w}x{h}")
                        cv2.putText(frame, f"Camera {idx} - Name it in Terminal",
                                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                        cv2.imshow("Name This Camera", frame)
                        cv2.waitKey(1000)  # wait 1 sec
                        success = True
                        break
                    time.sleep(0.5)

                if not success:
                    print(f"Could not get preview from camera {idx}")
                    continue

                name = input(f"Enter name for camera {idx} (e.g., 'front', 'side'): ").strip()
                self.camera_names[idx] = name
                cap.release()
                cv2.destroyAllWindows()

                folder_path = os.path.join("data", name)
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)
            except Exception as e:
                print(f"Error with camera {idx}: {str(e)}")

    def initialize_cameras(self):
        print("\nInitializing all named cameras...")
        for idx in self.camera_names:
            try:
                # Try DirectShow first
                cap = cv2.VideoCapture(idx + cv2.CAP_DSHOW)
                if not cap.isOpened():
                    # Fallback to default
                    cap = cv2.VideoCapture(idx)
                
                if not cap.isOpened():
                    print(f"Failed to initialize camera {idx}")
                    continue
                    
                cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.frame_size[0])
                cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.frame_size[1])
                self.cameras[idx] = cap
                print(f"  ✓ {self.camera_names[idx]} ready")
            except Exception as e:
                print(f"Error initializing camera {idx}: {str(e)}")

    def start_recording(self, trial_name):
        self.video_writers = {}
        print(f"🎥 Starting recording: {trial_name}")
        for idx, name in self.camera_names.items():
            filename = f"{trial_name}_{name}.mp4"
            filepath = os.path.join("data", name, filename)
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            writer = cv2.VideoWriter(filepath, fourcc, self.fps, self.frame_size)
            self.video_writers[idx] = writer
        self.recording = True

    def stop_recording(self):
        print("⏹️  Stopping recording and saving videos...")
        for writer in self.video_writers.values():
            writer.release()
        self.video_writers = {}
        self.recording = False

    def run(self):
        indices = self.detect_cameras()
        if not indices:
            print("No cameras found.")
            return

        print(f"Found {len(indices)} cameras.")
        self.get_camera_names(indices)
        self.initialize_cameras()

        print("\nReady. Press 's' to start, 'e' to end, 'q' to quit.\n")
        while True:
            frames = {}
            for idx, cap in self.cameras.items():
                ret, frame = cap.read()
                if ret:
                    frame = cv2.resize(frame, self.frame_size)
                    frames[idx] = frame
                    label = self.camera_names[idx]
                    cv2.putText(frame, label, (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                    if self.recording:
                        cv2.putText(frame, "REC", (10, 60),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

            # Combine into one window
            if frames:
                grid = np.hstack(list(frames.values()))
                cv2.imshow("Multi-Camera Recorder", grid)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('s') and not self.recording:
                trial_name = input("Enter trial name: ").strip()
                if trial_name:
                    self.start_recording(trial_name)

            elif key == ord('e') and self.recording:
                self.stop_recording()

            elif key == ord('q'):
                print("Exiting...")
                break

            if self.recording:
                for idx, frame in frames.items():
                    self.video_writers[idx].write(frame)

        self.cleanup()

    def cleanup(self):
        self.stop_recording()
        for cap in self.cameras.values():
            cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    app = MultiCameraRecorder()
    app.run()
