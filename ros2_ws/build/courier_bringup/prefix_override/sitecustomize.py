import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/yogesh/dev/autonomous-courier-challenge/ros2_ws/install/courier_bringup'
