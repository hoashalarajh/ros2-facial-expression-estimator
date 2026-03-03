#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

class CameraPublisher(Node):
    def __init__(self):
        super().__init__('camera_publisher')
        self.publisher_ = self.create_publisher(Image, '/video_frames', 10)
        self.timer = self.create_timer(0.05, self.timer_callback) # ~20 FPS
        self.cap = cv2.VideoCapture(0) # 0 is usually the default laptop webcam
        self.bridge = CvBridge()
        self.get_logger().info('Camera Publisher Node has been started.')

    def timer_callback(self):
        ret, frame = self.cap.read()
        if ret:
            # Convert OpenCV image (BGR) to ROS Image message
            msg = self.bridge.cv2_to_imgmsg(frame, encoding="bgr8")
            self.publisher_.publish(msg)

    def destroy_node(self):
        self.cap.release()
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    node = CameraPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()