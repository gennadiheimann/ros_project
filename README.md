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

### run projects

```bash
code ros2-for-beginners
code tf_urdf_rviz_gazebo
```

## Run GUI in Docker in kde neon

```bash
xhost +local:docker
```
