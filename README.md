https://docs.ros.org/en/foxy/How-To-Guides/Setup-ROS-2-with-VSCode-and-Docker-Container.html
ws_[project]
├── cache
|   ├── [ROS2_DISTRO]
|   |   ├── build
|   |   ├── install
|   |   └── log
|   └── ...
|
├── src
    ├── .devcontainer
    │   ├── devcontainer.json
    │   └── Dockerfile
    ├── package1
    └── package2
## Project

## Workspace
```bash
cd workspace
colcon build
```
## Py packege
in ws/src
```bash 
ros2 pkg create my_py_pkg --build-type ament_python --dependencies rclpy
```

## CPP package
```bash
ros2 pkg create my_cpp_pkg --build-type ament_cmake --dependencies rclcpp
```

## install selected package
```bash
colcon build --packages-select my_py_pkg
```

## source env
```bash
.  install/setup.sh
. /opt/ros/jazzy/setup.bash 
```

## run package

```bash
ros2 run my_py_pkg py_node
```

## Project

```bash
sudo apt install ros-jazzy-turtlesim
sudo apt install ros-jazzy-rqt-graph
```

```bash
ros2 pkg create turtelsim_catch_them_all --build-type ament_python --dependencies rclpy turtelsim
```

```bash
ros2 run turtlesim turtlesim_node

ros2 topic list

ros2 topic echo /turtle1/pose

ros2 topic info /turtle1/pose

ros2 interface show turtlesim/msg/Pose

colcon build --packages-select turtelsim_catch_them_all --symlink-install

ros2 run turtelsim_catch_them_all turtle_controller

ros2 service list

ros2 service type /spawn

ros2 service call /spawn turtlesim/srv/Spawn "{x: 4.0, y: 6.0, theta: 3.14}"

ros2 run turtelsim_catch_them_all turtle_spawner
```
### Tortlesim App
### Sourcing
```
.  install/setup.sh
. /opt/ros/jazzy/setup.bash 
```
```
ros2 run turtlesim turtlesim_node
ros2 run turtelsim_catch_them_all turtle_controller
ros2 run turtelsim_catch_them_all turtle_spawner
```
### Luaunch

```
ros2 launch my_robot_bringup turtelsim_catch_them_all.launch.xml 
```

# ros2 tf urdf rviz gazebo

## URDF Tutorial

```bash
sudo apt install ros-jazzy-urdf-tutorial
source /opt/ros/jazzy/setup.bash
ros2 launch urdf_tutorial display.launch.py model:=urdf/08-macroed.urdf.xacro 
ros2 launch urdf_tutorial display.launch.py model:=/home/ws/src/my_robot.urdf 
```

## Run robot state publisher in rviz

```bash
ros2 run robot_state_publisher robot_state_publisher --ros-args -p robot_description:="$(xacro src/my_robot.urdf)"
rqt_graph
ros2 run joint_state_publisher_gui joint_state_publisher_gui
ros2 run rviz2 rviz2
```

## Create robot description package

in workspace

```bash
colcon build
```

launch robot_description

```bash
ros2 launch my_robot_description display.launch.xml
```

##  Gazebo

```bash
ros2 launch ros_gz_sim gz_sim.launch.py gz_args:=empty.sdf
```

Inertia

https://en.wikipedia.org/wiki/List_of_moments_of_inertia#List_of_3D_inertia_tensors
https://wiki.ros.org/urdf/Tutorials/Adding%20Physical%20and%20Collision%20Properties%20to%20a%20URDF%20Model

Spawn the robot in gazibo

```bash
cd src/my_robot_description
ros2 run robot_state_publisher robot_state_publisher --ros-args -p robot_description:="$(xacro urdf/my_robot.urdf)"
ros2 launch ros_gz_sim gz_sim.launch.py gz_args:="empty.sdf -r"
ros2 run ros_gz_sim create -topic robot_description
```

## Spawn the robot in gazibo (bringup)

```bash
ros2 launch my_robot_bringup my_robot_gazebo.launch.xml
```

## Add gazibo pugin and bridge

[Gazibo Plugins](https://github.com/gazebosim/gz-sim/tree/gz-sim9/src/systems)  
[Gazibo Bridge](https://github.com/gazebosim/ros_gz/tree/ros2/ros_gz_bridge)
[Ros Gazibo Bridge](https://github.com/gazebosim/ros_gz/tree/ros2/ros_gz_bridge)

```bash
ros2 topic list
gz topic -l
gz topic -i -t /clock
ros2 topic echo /joint_states
ros2 topic pub -r 1 /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.0}, angular: {z: 0.0}}"
ros2 interface show geometry_msgs/msg/Twist
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

Show TF Graph

````bash
ros2 run tf2_tools view_frames
```

Start Gazebo alone

```bash
gz sim -v 4 /home/ws/install/my_robot_bringup/share/my_robot_bringup/worlds/my_robot_world.sdf
```

## Run GUI in Docker in kde neon

```bash
xhost +local:docker
```

## ...

```bash

```
