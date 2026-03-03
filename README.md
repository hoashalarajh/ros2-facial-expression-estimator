# ROS 2 MediaPipe Facial Expression Estimator

This project is a real-time facial expression analysis pipeline built on **ROS 2 Humble**. It utilizes a webcam feed and Google's **MediaPipe Face Landmarker (Tasks API)** to detect and extract 52 distinct facial blendshapes (e.g., smiles, blinks, jaw movements). 

The package includes nodes for publishing raw camera data, estimating and publishing facial expressions as JSON strings, and a live Matplotlib visualizer that tracks a 10-second moving average of your expressions.



## 🛠️ System Architecture

* **`camera_publisher`**: Captures raw webcam frames using OpenCV and publishes them to `/video_frames`.
* **`expression_estimator`**: Subscribes to the raw frames, processes them through the MediaPipe neural network, and publishes 52 facial blendshape scores (0.0 to 1.0) to `/facial_expressions`. It also publishes an annotated video feed with a mapped face mesh to `/annotated_frames`.
* **`expression_visualizer`**: Subscribes to the JSON expression data and displays a live, 10-second moving average bar chart of all expressions using Matplotlib.

---

## 📋 Prerequisites

* **OS:** Ubuntu 22.04
* **ROS Version:** ROS 2 Humble Hawksbill
* **Hardware:** Standard USB Webcam or Laptop Camera (`/dev/video0`)

---

## ⚙️ Installation & Setup

Follow these steps to set up the workspace, install specific stable dependencies, and build the project.

### 1. Create a Workspace and Clone
If you don't have a workspace set up, create one and clone this repository into the `src` directory:
```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src
git clone <YOUR-GITHUB-REPO-URL-HERE> facial_analysis_pkg
```
### 2. Install ROS 2 Dependencies
Ensure you have the required ROS 2 sensor and vision bridging packages:
```bash
sudo apt update
sudo apt install ros-humble-cv-bridge ros-humble-sensor-msgs
```

### 3. Install Python Dependencies
Important Note: To avoid known compatibility crashes with ROS 2 cv_bridge and recent MediaPipe updates, we specifically pin `NumPy` to a `1.x` version and `MediaPipe` to `0.10.21`.

```bash
pip install opencv-python matplotlib
pip install --force-reinstall "numpy<2.0"
pip install --force-reinstall mediapipe==0.10.21
```

### 4. Download the MediaPipe Model
The expression_estimator node requires the official `MediaPipe Face Landmarker` model. Download it directly into the root of your ROS 2 workspace:

```bash
cd ~/ros2_ws
wget -q -O face_landmarker.task [https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task](https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task)
```


### 5. Build the Workspace
Compile the package and source the installation:

```bash
cd ~/ros2_ws
colcon build --packages-select facial_analysis_pkg
source install/setup.bash
```

---


🚀 Usage Guide
To run the complete pipeline, you will need to open four separate terminal windows. Make sure to run all commands from the root of your workspace `(~/ros2_ws)` so the node can find the `face_landmarker.task` model file.

**Terminal 1: Start the Camera Node**
```bash
cd ~/ros2_ws
source install/setup.bash
ros2 run facial_analysis_pkg camera_publisher
```

**Terminal 2: Start the AI Estimator Node**
```bash
cd ~/ros2_ws
source install/setup.bash
ros2 run facial_analysis_pkg expression_estimator
```

**Terminal 3: Start the Live Bar Chart Visualizer**
```bash
cd ~/ros2_ws
source install/setup.bash
ros2 run facial_analysis_pkg expression_visualizer
```

**Terminal 4: View the Face Mesh (Optional)**
To see the live video feed with the AI face tracking mesh overlaid, use ROS 2's built-in image viewer:

```baah
cd ~/ros2_ws
source install/setup.bash
ros2 run rqt_image_view rqt_image_view
```

(Select `/annotated_frames` from the drop-down menu in the GUI).

---

## Topic Reference


| Topic Name | Message Type | Description |
| ----------- | ------------ | ------------ |
| `/video_frames`      | `sensor_msgs/Image`        | Raw RGB video frames from the webcam.       |
|`/annotated_frames`    | `sensor_msgs/Image`        | Video frames overlaid with the MediaPipe face mesh (for debugging).       |
|`/facial_expressions` | `std_msgs/String` | A JSON-formatted string containing the dictionary of 52 blendshape names and their current scores (0.0 to 1.0).|



