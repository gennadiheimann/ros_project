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
## Create action c++ package

```bash
ros2 pkg create actions_cpp --build-type ament_cmake --dependencies rclcpp interfaces
ros2 run actions_cpp count_until_server 
```

## Build

```bash
colcon build --packages-select actions_cpp
colcon build --cmake-args -DCMAKE_EXPORT_COMPILE_COMMANDS=ON
```

### Docker help commands

```bash
docker system prune
docker builder prune --all
docker system prune -a --volumes
docker system df
sudo systemctl start docker
docker context use default
docker info
# Autostart
sudo systemctl enable docker
# disable Autostart
sudo systemctl disable docker
sudo systemctl stop docker
sudo systemctl stop docker.socket
docker exec -it <container-id-oder-name> bash
# build commands.json
# ad to .vscode  "compileCommands": "${workspaceFolder}/build/compile_commands.json"
# see example below
colcon build --cmake-args -DCMAKE_EXPORT_COMPILE_COMMANDS=ON
```

```json
{
    "configurations": [
        {
            "name": "Linux",
            "includePath": [
                "${workspaceFolder}/**",
                "/opt/ros/jazzy/include/**",
                "/home/ws/install/**"
            ],
            "compilerPath": "/usr/bin/gcc",
            "cStandard": "c17",
            "cppStandard": "c++17",
            "intelliSenseMode": "linux-gcc-x64",
            "compileCommands": "/home/ws/build/compile_commands.json"
        }
    ],
    "version": 4
}
```
