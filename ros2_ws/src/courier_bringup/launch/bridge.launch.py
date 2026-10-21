from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():
    package_share = get_package_share_directory('courier_bringup')

    default_config = os.path.join(
        package_share,
        'bridge.yaml'
    )

    config_file = LaunchConfiguration('config_file')

    return LaunchDescription([
        DeclareLaunchArgument(
            'config_file',
            default_value=default_config,
            description='Path to the Gazebo-ROS bridge YAML configuration'
        ),

        Node(
            package='ros_gz_bridge',
            executable='parameter_bridge',
            name='tugbot_bridge',
            output='screen',
            parameters=[{
                'config_file': config_file
            }]
        )
    ])