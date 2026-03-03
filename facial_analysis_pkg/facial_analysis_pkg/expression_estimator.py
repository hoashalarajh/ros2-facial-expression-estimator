#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import String
from cv_bridge import CvBridge
import cv2
import json
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
import numpy as np
import os

class ExpressionEstimator(Node):
    def __init__(self):
        super().__init__('expression_estimator')
        self.subscription = self.create_subscription(Image, '/video_frames', self.image_callback, 10)
        self.expression_pub = self.create_publisher(String, '/facial_expressions', 10)
        self.annotated_pub = self.create_publisher(Image, '/annotated_frames', 10)
        self.bridge = CvBridge()

        # Resolve model path (assuming we run from ~/ros2_ws)
        model_path = os.path.join(os.getcwd(), 'face_landmarker.task')
        if not os.path.exists(model_path):
            self.get_logger().error(f"Model not found at {model_path}. Please run node from workspace root.")
            return

        base_options = python.BaseOptions(model_asset_path=model_path)
        options = vision.FaceLandmarkerOptions(
            base_options=base_options,
            output_face_blendshapes=True,
            output_facial_transformation_matrixes=True,
            num_faces=1,
            running_mode=vision.RunningMode.IMAGE
        )
        self.detector = vision.FaceLandmarker.create_from_options(options)
        self.get_logger().info("Expression Estimator Node started.")

    def image_callback(self, msg):
        cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        rgb_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_image)

        detection_result = self.detector.detect(mp_image)

        if detection_result.face_blendshapes:
            blendshapes = detection_result.face_blendshapes[0]
            expressions_dict = {cat.category_name: cat.score for cat in blendshapes}
            
            # Publish JSON
            msg_str = String()
            msg_str.data = json.dumps(expressions_dict)
            self.expression_pub.publish(msg_str)

            # Draw & Publish Annotated Image
            annotated_image = self.draw_landmarks(cv_image.copy(), detection_result)
            ros_annotated_img = self.bridge.cv2_to_imgmsg(annotated_image, encoding="bgr8")
            self.annotated_pub.publish(ros_annotated_img)
        else:
            self.annotated_pub.publish(msg) # Publish original if no face found

    def draw_landmarks(self, rgb_image, detection_result):
        face_landmarks_list = detection_result.face_landmarks
        annotated_image = np.copy(rgb_image)
        for face_landmarks in face_landmarks_list:
            face_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
            face_landmarks_proto.landmark.extend([
                landmark_pb2.NormalizedLandmark(x=lm.x, y=lm.y, z=lm.z) for lm in face_landmarks
            ])
            solutions.drawing_utils.draw_landmarks(
                image=annotated_image,
                landmark_list=face_landmarks_proto,
                connections=solutions.face_mesh.FACEMESH_TESSELATION,
                connection_drawing_spec=solutions.drawing_styles.get_default_face_mesh_tesselation_style())
        return annotated_image

def main(args=None):
    rclpy.init(args=args)
    node = ExpressionEstimator()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()