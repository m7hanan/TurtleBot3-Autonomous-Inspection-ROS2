# Real-Robot Autonomous Navigation — 12 November 2026

## Outcome and evidence boundary

**Reported outcome:** Following physical robot reassembly and creation of a new map, Nav2 autonomous point-to-point navigation was run successfully multiple times on the physical TurtleBot3 Waffle Pi. The project lead recorded a video demonstration:

**[Real-world autonomous navigation demo (YouTube Shorts)](https://youtube.com/shorts/Oj6nLm5XzTM)**

This video link and the multiple-run success report were supplied by the project lead. Individual action-status logs, measured success rates, positioning errors, and collision-monitor intervention tests have not been independently provided for the 12 Nov runs. The video is demonstration evidence, not a quantitative benchmark.

## Real robot and software stack

- TurtleBot3 Waffle Pi, Raspberry Pi 4B (2 GB), ROBOTIS OpenCR + DYNAMIXEL, LDS-02 LiDAR
- Ubuntu Server 24.04.5 on Pi; Ubuntu 24.04 on laptop; ROS 2 Jazzy; Fast DDS
- Laptop `normalize_scan.py` for variable raw scan sizes to 224-bin `/scan_normalized`
- SLAM Toolbox for mapping; Nav2 map server + AMCL for saved-map localization
- Nav2 global planning, MPPI DiffDrive controller, velocity smoother, collision monitor
- Velocity command interface to OpenCR: `geometry_msgs/msg/TwistStamped`

## Saved map and artifacts

| Artifact | Recorded value |
|---|---|
| Map | `lab_map_2026_11_12` |
| Occupancy grid size | 762 × 238 cells |
| Resolution | 0.05 m/cell |
| Grid extent | 38.1 × 11.9 m (allocated extents; **not** surveyed free space) |
| Origin | [-19.125, -8.896, 0] |
| Occupancy map files | `.pgm` and `.yaml` exported successfully |
| Serialized SLAM artifacts | `.posegraph` and `.data` saved locally (`result=0`) |
| Nav2 map | Copied to `~/tb3_nav2/maps/`, byte-for-byte verified against original |
| Map server + AMCL | `active [3]` after saved map reload |

The occupancy map is included in `navigation/maps/`. The larger SLAM posegraph/data files are retained locally for later archival rather than committed to this repository.

## Configuration and usage

- Saved-map localization: `nav2_bringup localization_launch.py` with `lab_map_2026_11_12.yaml`.
- Navigation: `nav2_bringup navigation_launch.py` with `navigation/config/nav2_params.yaml`.
- MPPI `DiffDrive`; last recorded controller frequency 10 Hz, `model_dt=0.1 s`, maximum forward linear speed 0.04 m/s, and forward-only `vx_min=0.0`. The committed YAML is the canonical configuration snapshot; inspect its current values.
- Navigation command chain: controller → velocity smoother → collision monitor → OpenCR, carrying `TwistStamped`.

## Known limitations / next validation

- Previous sessions had a physical front/back disagreement with RViz, followed by robot reassembly. Repeat a controlled physical +X motor/odometry direction check before publishing a claim of calibrated alignment.
- The scan normalization algorithm is a working engineering workaround; quantify angular accuracy and false/infinite readings.
- Previous sessions showed intermittent scan/TF timestamp and queue-filter warnings; log rates during representative navigation runs.
- The physical footprint was provisionally modeled with a 0.22 m radius; measure actual clearance and validate against obstacles.
- Battery telemetry and physical emergency stop must be checked per session.
- Robust obstacle avoidance, multi-waypoint mission success, localization drift, path tracking errors, and reproducibility statistics remain unquantified.
- Raspberry Pi `tb3_headless_bringup` source and motor-control scripts are not yet copied into the public repository.

## Future experiment log template

| Trial | Start pose | Goal pose | Duration | Result | Final error | Recoveries | Notes |
|---|---|---|---|---|---|---|---|
| 01+ | To be logged | To be logged | — | User-reported success | Not measured | Not measured | Video link above |

Do not infer a success percentage or localization precision from the available video alone.
