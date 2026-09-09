```bash
ros2 pkg create interfaces
colcon build --packages-select interfaces
ros2 interface show interfaces/action/CountUntil
```

```bash
ros2 pkg create actions_py --build-type ament_python --dependencies rclpy interfaces
colcon build --packages-select actions_py --symlink-install
```

```bash
ros2 run actions_py count_until_server
ros2 run actions_py count_until_client
````