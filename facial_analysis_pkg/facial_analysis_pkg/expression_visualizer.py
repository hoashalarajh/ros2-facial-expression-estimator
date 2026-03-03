#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import json
import time
from collections import deque
import threading
import matplotlib.pyplot as plt

class ExpressionVisualizer(Node):
    def __init__(self):
        super().__init__('expression_visualizer')
        # Subscribe to the JSON expressions topic
        self.subscription = self.create_subscription(
            String,
            '/facial_expressions',
            self.listener_callback,
            10)
        
        # A deque (double-ended queue) is perfect for a sliding window
        self.history = deque()
        self.window_size = 10.0  # 10 seconds moving window
        
        self.get_logger().info("Visualizer node started. Waiting for data...")

    def listener_callback(self, msg):
        try:
            # Parse the JSON string back into a Python dictionary
            data = json.loads(msg.data)
            current_time = time.time()
            
            # Add new data with its timestamp
            self.history.append((current_time, data))
            
            # Remove old data that falls outside our 10-second window
            while self.history and self.history[0][0] < current_time - self.window_size:
                self.history.popleft()
                
        except Exception as e:
            self.get_logger().error(f"Error parsing JSON: {e}")

    def get_average_expressions(self):
        """Calculates the mean score for each expression in the current window."""
        if not self.history:
            return {}
            
        # Initialize a dictionary to hold the sum of all expressions
        sums = {key: 0.0 for key in self.history[0][1].keys()}
        count = len(self.history)
        
        # Add them all up
        for _, data_dict in self.history:
            for key, value in data_dict.items():
                if key in sums:
                    sums[key] += value
                    
        # Divide by count to get the average
        averages = {key: sums[key] / count for key in sums}
        return averages


def main(args=None):
    rclpy.init(args=args)
    node = ExpressionVisualizer()
    
    # Run the ROS listener in a separate background thread
    # This prevents ROS from freezing the Matplotlib window!
    spin_thread = threading.Thread(target=rclpy.spin, args=(node,))
    spin_thread.start()
    
    # --- Setup Matplotlib (Main Thread) ---
    plt.ion()  # Turn on interactive mode for live updating
    fig, ax = plt.subplots(figsize=(16, 8)) # Make it wide to fit 52 bars
    fig.canvas.manager.set_window_title('Live 10-Second Expression Distribution')
    
    try:
        # Loop to continuously draw the graph
        while rclpy.ok():
            averages = node.get_average_expressions()
            
            if averages:
                ax.clear()
                
                # Sort alphabetically so the bars don't jump around
                sorted_items = sorted(averages.items())
                labels = [item[0] for item in sorted_items]
                values = [item[1] for item in sorted_items]
                
                # Draw the bar chart
                ax.bar(labels, values, color='coral')
                ax.set_ylim(0, 1.0)
                ax.set_ylabel('Average Intensity (0.0 to 1.0)')
                ax.set_title('10-Second Moving Average of 52 Facial Blendshapes')
                
                # Rotate the x-axis labels 90 degrees so we can read all 52 names
                plt.xticks(rotation=90, fontsize=8)
                plt.tight_layout() 
                
            plt.pause(0.1) # Pause briefly to let the chart draw (updates at ~10 FPS)
            
    except KeyboardInterrupt:
        pass
    finally:
        # Clean up safely when you press Ctrl+C
        plt.close('all')
        node.destroy_node()
        rclpy.shutdown()
        spin_thread.join()

if __name__ == '__main__':
    main()