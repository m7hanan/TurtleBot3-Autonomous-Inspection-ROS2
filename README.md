# TurtleBot3 Autonomous Indoor Navigation & Inspection

A real-world autonomous mobile robotics project built using
**ROS 2 Jazzy, TurtleBot3 Waffle Pi, Raspberry Pi 4, OpenCR,
LDS-02 LiDAR, SLAM Toolbox, and RViz2**.

The project focuses on real-time indoor mapping, autonomous
navigation, and future camera-based laboratory inspection.

> **Project Status:** Active Development
> **Current Milestone:** Real-time 2D SLAM implemented and demonstrated
> **Next Milestone:** Nav2 autonomous navigation

## Project Objectives

- Build a ROS 2-based autonomous mobile robot.
- Generate real-time 2D maps of indoor environments.
- Perform autonomous navigation using Nav2.
- Implement obstacle-aware navigation.
- Integrate camera-based remote monitoring.
- Develop autonomous laboratory inspection missions.
- Evaluate robotic communication performance for research.

## Hardware

| Component | Specification |
|---|---|
| Robot | TurtleBot3 Waffle Pi |
| Computer | Raspberry Pi 4 Model B (2GB) |
| Controller | ROBOTIS OpenCR |
| Motors | DYNAMIXEL |
| LiDAR | LDS-02 |
| Camera | Raspberry Pi IMX219 CSI |
| Development Computer | Ubuntu Laptop |

## Software Stack

- Ubuntu 24.04 LTS
- ROS 2 Jazzy
- Fast DDS
- Python
- SLAM Toolbox
- RViz2
- Nav2 (planned)
- RTAB-Map (future development)

## System Architecture

```text
              TurtleBot3 Waffle Pi
                       |
                Raspberry Pi 4
                       |
          +------------+------------+
          |                         |
        OpenCR                    LDS-02
          |                         |
    Motors + IMU                  LiDAR
    + Encoders                     |
          |                         |
        /odom                     /scan
          |                         |
          |                 Scan Normalizer
          |                         |
          |                  /scan_normalized
          |                         |
          +------------+------------+
                       |
                   ROS 2 DDS
                       |
                Ubuntu Laptop
                       |
                 SLAM Toolbox
                       |
                  /map + TF
                       |
                     RViz2
```

## Completed Development

The following features have been implemented and tested:

- Raspberry Pi and laptop ROS 2 communication.
- Custom headless robot bringup.
- OpenCR integration.
- ROS-controlled motor movement.
- Motor torque enable/disable.
- Wheel encoder feedback.
- IMU and wheel odometry.
- LDS-02 LiDAR integration.
- Custom LiDAR scan normalization.
- Real-time 2D SLAM using SLAM Toolbox.
- RViz2 mapping and visualization.
- Live mapping demonstration during robot movement.
- IMX219 camera raw-image capture.

### SLAM Implementation

The LDS-02 driver produces LaserScan messages with
varying numbers of readings.

A custom Python scan-normalization node converts the
incoming measurements into a fixed 224-bin angular grid
for SLAM Toolbox.

```text
/scan
  |
  v
normalize_scan.py
  |
  v
/scan_normalized
  |
  v
SLAM Toolbox
  |
  v
/map
```

The original scan topic is preserved.

Normalization is an engineering workaround;
its effect on mapping accuracy requires further validation.

### Verified Measurements

| Test | Result |
|---|---|
| LiDAR frequency | Approximately 10 Hz |
| Normalized scan size | 224 beams |
| Ground movement command | 0.02 m/s for 1.5 seconds |
| Encoder-estimated travel | Approximately 2.98 cm |
| SLAM map resolution | 0.05 m/cell |
| SLAM lifecycle | Active during tests |
| Map-to-odom TF | Verified |

## Repository Structure

```text
slam/
  config/
    waffle_pi_async.yaml
  scripts/
    normalize_scan.py

rviz/
  tb3_mapping.rviz

docs/
media/
```

Additional source files from the Raspberry Pi
will be added in future commits.

## Running the SLAM Components

Prerequisites:

- ROS 2 Jazzy installed.
- TurtleBot3 robot bringup running.
- `/scan`, `/odom`, and required TF transforms available.
- Laptop and robot connected through the ROS 2 network.

### 1. Start Scan Normalizer

```bash
source /opt/ros/jazzy/setup.bash
python3 slam/scripts/normalize_scan.py
```

### 2. Start SLAM Toolbox

In another terminal:

```bash
source /opt/ros/jazzy/setup.bash

ros2 launch slam_toolbox online_async_launch.py \
  slam_params_file:=$(pwd)/slam/config/waffle_pi_async.yaml \
  use_sim_time:=false
```

### 3. Launch RViz2

```bash
source /opt/ros/jazzy/setup.bash
rviz2 -d rviz/tb3_mapping.rviz
```

## Development Roadmap

### v0.1 - ROS 2 SLAM Baseline

- [x] ROS 2 communication
- [x] OpenCR motor control
- [x] LiDAR integration
- [x] Wheel odometry
- [x] Real-time SLAM
- [x] RViz visualization
- [ ] Publish complete Raspberry Pi bringup source
- [ ] Export and verify saved occupancy grid map files

### v1.0 - Autonomous Navigation

- [ ] Nav2 integration
- [ ] AMCL localization
- [ ] Global and local costmaps
- [ ] Autonomous goal navigation
- [ ] Obstacle avoidance testing
- [ ] Multi-waypoint navigation
- [ ] Full laboratory demonstration

### v2.0 - Autonomous Laboratory Inspection

- [ ] ROS 2 camera streaming
- [ ] Live remote monitoring
- [ ] Autonomous inspection missions
- [ ] Image capture at inspection stations
- [ ] Mission reporting

### v3.0 - Research Integration

- [ ] ROS 2 communication benchmarking
- [ ] Rust-based middleware experiments
- [ ] Latency and throughput analysis
- [ ] CPU and memory analysis
- [ ] End-to-end performance comparison

## Future Development

This platform will also serve as a real-hardware
experimental environment for research into
high-performance robotic communication.

## Project Status

This is an ongoing undergraduate robotics development project.
Autonomous navigation and inspection features are planned
and have not yet been completed.

## License

License selection pending.
