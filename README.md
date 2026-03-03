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


