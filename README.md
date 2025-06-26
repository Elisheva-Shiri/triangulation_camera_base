# Multi-Camera Recording System

A Python-based multi-camera recording system that automatically detects available cameras, allows user-defined naming, and provides synchronized recording capabilities with organized file storage.

## Features

- **Automatic Camera Detection**: Automatically finds all connected cameras
- **User-Defined Camera Naming**: Interactive camera naming during setup
- **Multi-Camera Display**: Real-time display of all camera feeds in a grid layout
- **Synchronized Recording**: Start/stop recording for all cameras simultaneously
- **Organized File Storage**: Automatic folder creation and file naming
- **Keyboard Controls**: Simple keyboard-based recording controls

## Requirements

- Python 3.7 or higher
- Webcams or USB cameras
- Windows/Linux/macOS

## Installation

1. **Clone or download the project files**

2. **Install required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

   Or install manually:
   ```bash
   pip install opencv-python pygame numpy
   ```

## Usage

### Running the Script

1. **Start the application**:
   ```bash
   python multi_camera_recorder.py
   ```

2. **Camera Detection Phase**:
   - The script will automatically detect all available cameras
   - Each detected camera will be displayed briefly with a countdown
   - You'll be prompted to name each camera (e.g., "front", "side", "top")

3. **Main Interface**:
   - All camera feeds will be displayed in a grid layout
   - Camera names and recording status are shown on each feed
   - Status information is displayed at the bottom

### Controls

- **'s' key**: Start recording (you'll be prompted for a trial name)
- **'e' key**: Stop recording and save videos
- **'q' key**: Quit the application
- **Close window**: Click the X button to exit

### Recording Process

1. **Start Recording**:
   - Press 's' to start recording
   - Enter a trial name when prompted (e.g., "trial_001", "experiment_1")
   - All cameras will begin recording simultaneously

2. **Stop Recording**:
   - Press 'e' to stop recording
   - Videos will be automatically saved to their respective folders

## Performance Issues and Solutions

### Common Performance Problems

If you experience slow performance with additional cameras, try these solutions:

1. **Use the Optimized Version**:
   ```bash
   python multi_camera_recorder_optimized.py
   ```
   
   The optimized version includes:
   - Lower display refresh rate (15 FPS instead of 30)
   - Frame skipping for display (every 2nd frame)
   - Reduced buffer sizes
   - Better error handling

2. **Reduce Resolution**:
   Edit the `frame_size` parameter in the script:
   ```python
   self.frame_size = (320, 240)  # Lower resolution
   ```

3. **Close Other Applications**:
   - Close any other applications using the cameras
   - Ensure sufficient CPU and memory resources

4. **Check Camera Drivers**:
   - Update camera drivers
   - Try different USB ports
   - Check if cameras support the selected resolution

### Camera Naming Phase

If the program seems to stop after creating the data folder:
- The camera naming phase shows each camera for 3 seconds with a countdown
- Look for the countdown numbers on each camera window
- Enter camera names in the terminal when prompted
- The program will continue to the main display after all cameras are named

## Folder Architecture

The system creates the following folder structure:

```
DataVideo/
├── multi_camera_recorder.py
├── multi_camera_recorder_optimized.py
├── requirements.txt
├── README.md
├── test_installation.py
├── run_recorder.bat
└── data/
    ├── front/
    │   ├── trial_001_front.mp4
    │   ├── experiment_1_front.mp4
    │   └── ...
    ├── side/
    │   ├── trial_001_side.mp4
    │   ├── experiment_1_side.mp4
    │   └── ...
    ├── top/
    │   ├── trial_001_top.mp4
    │   ├── experiment_1_top.mp4
    │   └── ...
    └── [other_camera_names]/
        └── ...
```

### Folder Structure Explanation

- **`data/`**: Main directory for all recorded videos
- **`data/[camera_name]/`**: Individual folders for each camera
- **File naming**: `{trial_name}_{camera_name}.mp4`

## Technical Details

### Camera Detection
- Uses OpenCV's `VideoCapture` to detect cameras starting from index 0
- Automatically stops when no more cameras are found
- Supports any number of cameras (limited by system resources)

### Video Recording
- **Format**: MP4 with H.264 codec
- **Frame Rate**: 30 FPS (configurable)
- **Resolution**: 640x480 (configurable)
- **Synchronization**: All cameras start/stop recording simultaneously

### Display Layout
- **Grid Layout**: Automatically arranges cameras in a grid (max 3 columns)
- **Real-time Display**: Shows live feeds from all cameras
- **Status Indicators**: Shows recording status and camera names
- **Responsive**: Handles different numbers of cameras gracefully

## Configuration

You can modify the following parameters in the `MultiCameraRecorder` class:

```python
self.fps = 30.0              # Frame rate
self.frame_size = (640, 480) # Video resolution
```

For the optimized version, additional settings:
```python
self.display_fps = 15.0      # Display refresh rate
self.frame_skip = 2          # Frame skipping for display
```

## Troubleshooting

### Common Issues

1. **No cameras detected**:
   - Ensure cameras are properly connected
   - Check if cameras are being used by other applications
   - Try restarting the application

2. **Permission errors**:
   - Ensure you have write permissions in the project directory
   - Run as administrator if necessary (Windows)

3. **Video codec issues**:
   - The script uses 'mp4v' codec which should work on most systems
   - If you encounter issues, you can change the codec in the `start_recording` method

4. **Performance issues**:
   - Use the optimized version: `multi_camera_recorder_optimized.py`
   - Reduce frame rate or resolution for better performance
   - Close other applications using the cameras
   - Ensure sufficient disk space for recording

5. **Program stops after data folder creation**:
   - This is the camera naming phase
   - Look for camera windows with countdown numbers
   - Enter names in the terminal when prompted
   - The program will continue after all cameras are named

### Camera Index Issues

If cameras are not detected in the expected order:
- The script detects cameras starting from index 0
- Camera order depends on system configuration
- You can manually specify camera indices by modifying the detection logic

## Dependencies

- **opencv-python**: Computer vision library for camera access and video processing
- **pygame**: Library for keyboard input handling
- **numpy**: Numerical computing library for array operations

## License

This project is open source and available under the MIT License.

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve the system.

## Support

For issues or questions, please check the troubleshooting section above or create an issue in the project repository. 