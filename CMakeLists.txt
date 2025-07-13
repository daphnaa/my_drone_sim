cmake_minimum_required(VERSION 3.5)
project(my_drone_sim)

# Find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(gazebo_ros REQUIRED)

# Install Gazebo world files, textures, and models
install(DIRECTORY worlds/
  DESTINATION share/${PROJECT_NAME}/worlds)

install(DIRECTORY launch/
  DESTINATION share/${PROJECT_NAME}/launch)

ament_package()

