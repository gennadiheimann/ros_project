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

```bash
ros2 run tf2_tools view_frames
```

Start Gazebo alone

```bash
gz sim -v 4 /home/ws/install/my_robot_bringup/share/my_robot_bringup/worlds/my_robot_world.sdf
```

## Arm project

Start Rviz

```bash
ros2 run robot_state_publisher robot_state_publisher --ros-args -p robot_description:="$(xacro src/my_robot_description/urdf/standalone_arm.urdf.xacro)"
ros2 run rviz2 rviz2
```

Debug

```bash
check_urdf
xacro src/my_robot_description/urdf/my_robot.urdf.xacro > /home/ws/robot.urdf
```

Run without gazibo Rviz, joint_state_publisher_gui, robot_state_publisher

```bash
ros2 run robot_state_publisher robot_state_publisher --ros-args -p robot_description:="$(xacro src/my_robot_description/urdf/my_robot.urdf.xacro)"
ros2 run joint_state_publisher_gui joint_state_publisher_gui
ros2 run rviz2 rviz2 ros-args -d src/my_robot_description/rviz/urdf_config_robot_arm.rviz
```

## Run GUI in Docker in kde neon

```bash
xhost +local:docker
```
