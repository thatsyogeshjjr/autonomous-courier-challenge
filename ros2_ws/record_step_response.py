#!/usr/bin/env python3
import csv
import time

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import JointState


class StepResponseRecorder(Node):
    def __init__(self):
        super().__init__('step_response_recorder')

        self.cmd_v = 0.0
        self.cmd_w = 0.0
        self.joint_state = None
        self.start_time = time.monotonic()

        self.create_subscription(
            Twist, '/cmd_vel', self.cmd_callback, 10
        )
        self.create_subscription(
            JointState, '/joint_state', self.joint_callback, 10
        )

        self.file = open('step_response.csv', 'w', newline='')
        self.writer = csv.writer(self.file)
        self.writer.writerow([
            'time_s', 'cmd_linear_mps', 'cmd_angular_radps',
            'left_wheel_radps', 'right_wheel_radps'
        ])

        self.create_timer(0.02, self.record)
        self.get_logger().info('Recording to step_response.csv')

    def cmd_callback(self, msg):
        self.cmd_v = msg.linear.x
        self.cmd_w = msg.angular.z

    def joint_callback(self, msg):
        self.joint_state = msg

    def record(self):
        if self.joint_state is None:
            return

        names = self.joint_state.name
        velocities = self.joint_state.velocity

        try:
            left = velocities[names.index('wheel_left_joint')]
            right = velocities[names.index('wheel_right_joint')]
        except (ValueError, IndexError):
            return

        self.writer.writerow([
            time.monotonic() - self.start_time,
            self.cmd_v, self.cmd_w, left, right
        ])
        self.file.flush()

    def destroy_node(self):
        self.file.close()
        super().destroy_node()


def main():
    rclpy.init()
    node = StepResponseRecorder()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
