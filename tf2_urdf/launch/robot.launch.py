import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
import xacro

def generate_launch_description():
    package_name = 'tf2_urdf'

    # robot_state_publisher
    pkg_path = os.path.join(get_package_share_directory(package_name))
    xacro_file = os.path.join(pkg_path, 'urdf', 'robot.xacro')
    robot_description = xacro.process_file(xacro_file)
    params = {'robot_description': robot_description.toxml(), 'use_sim_time': False}

    rsp = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[params],
    )
    # odometry publisher
    odometry_publisher = Node(
        package='car_odom',
        executable='car_odom',
        output='screen',
        parameters=[],
    )
    # rviz2
    rviz = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', 'src/tf2_study/tf2_urdf/rviz/car.rviz'],
    )
    fake_driver = Node(
        package='tf2_urdf',
        executable='fake_driver',
        name='fake',
        output='screen',
    )
    return LaunchDescription(
        [
            rsp,
            rviz,
            fake_driver,
            odometry_publisher,
        ]
    )