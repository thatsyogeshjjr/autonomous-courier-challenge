#!/usr/bin/env python3

import time

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class SquareTrajectory(Node):

    def __init__(self):
        super().__init__("square_trajectory")

        self.publisher = self.create_publisher(
            Twist,
            "/cmd_vel",
            10
        )

        # Trajectory parameters
        self.side_length = 0.5       # metres
        self.linear_speed = 0.8      # m/s
        self.angular_speed = 0.3     # rad/s
        self.rate_hz = 20.0          # command publishing frequency

        self.get_logger().info(
            f"Square trajectory initialized: "
            f"side={self.side_length} m, "
            f"linear_speed={self.linear_speed} m/s, "
            f"angular_speed={self.angular_speed} rad/s"
        )

    def publish_velocity(self, linear=0.0, angular=0.0):
        msg = Twist()
        msg.linear.x = float(linear)
        msg.angular.z = float(angular)
        self.publisher.publish(msg)

    def stop(self, duration=0.5):
        """Publish zero velocity to stop the robot."""
        end_time = time.monotonic() + duration

        while time.monotonic() < end_time:
            self.publish_velocity()
            time.sleep(1.0 / self.rate_hz)

    def execute_segment(self, linear, angular, duration, description):
        """Execute one timed motion segment."""
        self.get_logger().info(description)

        end_time = time.monotonic() + duration

        try:
            while time.monotonic() < end_time:
                self.publish_velocity(linear, angular)
                time.sleep(1.0 / self.rate_hz)
        finally:
            self.stop()

    def run_square(self):
        # Estimate the time required for each side and turn.
        straight_duration = self.side_length / self.linear_speed
        turn_duration = (3.141592653589793 / 2.0) / self.angular_speed

        self.get_logger().info(
            f"Estimated straight duration: {straight_duration:.2f} s"
        )
        self.get_logger().info(
            f"Estimated turn duration: {turn_duration:.2f} s"
        )

        self.stop(1.0)

        for side in range(4):
            self.execute_segment(
                linear=self.linear_speed,
                angular=0.0,
                duration=straight_duration,
                description=f"Side {side + 1}/4: driving forward"
            )

            self.execute_segment(
                linear=0.0,
                angular=self.angular_speed,
                duration=turn_duration,
                description=f"Corner {side + 1}/4: turning 90 degrees"
            )

        self.stop(1.0)
        self.get_logger().info("Square trajectory completed.")


def main(args=None):
    rclpy.init(args=args)
    node = SquareTrajectory()

    try:
        node.run_square()
    except KeyboardInterrupt:
        node.get_logger().warning("Trajectory interrupted.")
    finally:
        node.stop(0.5)
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()