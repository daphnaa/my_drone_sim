import os
from launch import LaunchDescription
from launch.actions import ExecuteProcess, SetEnvironmentVariable # IMPORTANT: Added SetEnvironmentVariable
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration
from launch_ros.substitutions import FindPackageShare
from ament_index_python.packages import get_package_share_directory # Added for get_package_share_directory

def generate_launch_description():
    # Define the path to your world file
    world_file_path = os.path.join(
        FindPackageShare('my_drone_sim').find('my_drone_sim'),
        'worlds', 'bookstore', 'bookstore.world'
    )

    # --- CONFIGURE GAZEBO_MODEL_PATH HERE ---
    # Gazebo needs to know where to find all 3D models referenced in your world file.
    # You MUST replace the placeholder paths with the actual absolute paths on your system.

    model_paths = [
        # 1. Path to models within your 'my_drone_sim' package (e.g., TurtleBot3 variants)
        os.path.join(get_package_share_directory('my_drone_sim'), 'robots'),

        # 2. Path(s) to your AWS RoboMaker Retail models
        #    You need to find where you downloaded/extracted these assets.
        #    It's the directory that contains folders like 'aws_robomaker_retail_BookE_01', 'aws_robomaker_retail_Spotlight_01', etc.
        #    Example: '/home/daphnaa/my_downloaded_assets/aws_robomaker_retail_models'
        '/home/daphnaa/ros2_ws/src/my_drone_sim/worlds/bookstore/models', 

        # 3. Path to the Iris drone model
        #    This often comes from 'rotors_gazebo' package. If you installed it via apt,
        #    the line below should work. Otherwise, find its custom location.
        #    Example if installed: os.path.join(get_package_share_directory('rotors_gazebo'), 'models')
        #'/path/to/your/iris/models', # <--- REPLACE THIS WITH YOUR ACTUAL PATH (or use the get_package_share_directory if installed)!

        # 4. Standard Gazebo Classic 11 model paths (usually included by default Gazebo install)
        '/usr/share/gazebo-11/models',
        os.path.expanduser('~/.gazebo/models'), # Your user-specific Gazebo models directory

        # Optional: If 'gazebo_ros' package itself contains models (less common for Classic)
        os.path.join(get_package_share_directory('gazebo_ros'), 'models') if os.path.exists(os.path.join(get_package_share_directory('gazebo_ros'), 'models')) else '',
    ]

    # Filter out any empty paths (e.g., if a package wasn't found) and join them with a colon
    full_model_path = ":".join(filter(None, model_paths))
    # --- END GAZEBO_MODEL_PATH CONFIGURATION ---

    return LaunchDescription([
        # Set the GAZEBO_MODEL_PATH environment variable for all processes in this launch
        SetEnvironmentVariable(name='GAZEBO_MODEL_PATH', value=full_model_path),

        # Start Gazebo server
        ExecuteProcess(
            cmd=[
                'gzserver',
                '-s', 'libgazebo_ros_init.so', # This plugin is crucial for ROS-Gazebo communication
                '--verbose',
                world_file_path
            ],
            output='screen',
            name='gazebo_server_process' # Added name for clarity in logs
        ),

        # Start Gazebo client (GUI)
        ExecuteProcess(
            cmd=['gzclient'],
            output='screen',
            name='gazebo_client_process' # Added name for clarity in logs
        ),

        # Add any other necessary ROS 2 nodes here using the Node action, for example:
        # Node(
        #     package='your_drone_controller_pkg',
        #     executable='your_drone_controller_node',
        #     output='screen',
        #     parameters=[{'use_sim_time': True}]
        # ),
    ])
