# Action

## Create interface package

```bash
ros2 pkg create interfaces
colcon build --packages-select interfaces
ros2 interface show interfaces/action/CountUntil
```

## Create actions python package

```bash
ros2 pkg create actions_py --build-type ament_python --dependencies rclpy interfaces
colcon build --packages-select actions_py --symlink-install
```

# Run Client and Server

```bash
ros2 run actions_py count_until_server
ros2 run actions_py count_until_client
```

## Introspect Action

```bash
ros2 action
ros2 action list
ros2 action info /count_until
ros2 node info /count_until_server
ros2 topic list --include-hidden-topics 
ros2 service list --include-hidden-services 
ros2 action list -t
ros2 interface show interfaces/action/CountUntil
ros2 action send_goal /count_until interfaces/action/CountUntil "{target_number: 8, period: 2.0}"
ros2 action send_goal /count_until interfaces/action/CountUntil "{target_number: 8, period: 2.0}" --feedback 
```