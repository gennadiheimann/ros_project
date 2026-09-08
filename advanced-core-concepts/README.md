```bash
ros2 pkg create interfaces
colcon build --packages-select interfaces
ros2 interface show interfaces/action/CountUntil
```

```bash
ros2 pkg create actions_py --build-type ament_python --dependencies rclpy interfaces

```