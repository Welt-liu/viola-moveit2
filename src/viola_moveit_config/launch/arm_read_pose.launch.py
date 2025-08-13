from launch import LaunchDescription
from launch_ros.actions import Node
from moveit_configs_utils import MoveItConfigsBuilder
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
import os
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    # Set MoveIt configuration
    moveit_config = MoveItConfigsBuilder("viola").to_moveit_configs()

    arm_read_pose_config_path = os.path.join(
        get_package_share_directory('viola_moveit_config'),
        'config',
        )

    declare_param_file_cmd=DeclareLaunchArgument(
        'arm_params',
        default_value= arm_read_pose_config_path,
        # 'Full path to the ROS2 parameters file'
    )


    return LaunchDescription(
        [
            declare_param_file_cmd,
            Node(
                package="arm_read_pose",
                executable="arm_read_pose",
                output="screen",
                parameters=[
                    moveit_config.robot_description,  # Load URDF
                    moveit_config.robot_description_semantic,  # Load SRDF
                    moveit_config.robot_description_kinematics,  # Load kinematics.yaml
                    LaunchConfiguration('arm_params'),
                    # arm_read_pose_config,
                ],
        )
        ]
    )