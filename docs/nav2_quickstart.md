# TurtleBot3 Waffle Pi — Saved-Map Nav2 Quickstart

**Platform:** Raspberry Pi 4B (Ubuntu Server 24.04, ROS 2 Jazzy), OpenCR + DYNAMIXEL, LDS-02 LiDAR, HP Victus Ubuntu laptop, Fast DDS.  
**Map:** `navigation/maps/lab_map_2026_11_12.yaml` (map created 12 Nov 2026).  
**Status:** Nav2 autonomous navigation demonstrated on a real robot in multiple runs (user-reported); quantified performance evaluation remains pending.

> Safety: This is a supervised research robot, not a safety-certified system. Before commanding motion, verify battery under load, accessible physical stop, clear floor, command authority, robot dimensions, transform alignment, and collision-monitor behavior. A previous session showed a front/back direction mismatch; confirm the physical forward axis after reassembly. Do not send a goal until that check passes.

## Terminal 1 — Raspberry Pi robot bringup (laptop SSH)

```bash
ssh hanan@mahdi.local
source /opt/ros/jazzy/setup.bash
source ~/ros2_ws/install/setup.bash
export TURTLEBOT3_MODEL=waffle_pi
export ROS_DOMAIN_ID=0
ls -l /dev/ttyACM0 /dev/ttyUSB0
ros2 launch tb3_headless_bringup robot.launch.py \
  enable_opencr:=true enable_lidar:=true
```

Keep terminal running. Pi's custom `tb3_headless_bringup` source is not yet included in this repository; it will be added after a future laboratory visit.

## Terminal 2 — Laptop LiDAR normalizer

```bash
source /opt/ros/jazzy/setup.bash
export ROS_DOMAIN_ID=0
python3 ~/tb3_slam/scripts/normalize_scan.py
```

The node converts `/scan` to a fixed 224-bin `/scan_normalized`. Its original source is also published in `slam/scripts/normalize_scan.py`. Ensure a single normalizer instance runs.

## Terminal 3 — Saved map + AMCL localization (NOT SLAM Toolbox)

```bash
source /opt/ros/jazzy/setup.bash
export ROS_DOMAIN_ID=0
ros2 launch nav2_bringup localization_launch.py \
  map:=$HOME/tb3_nav2/maps/lab_map_2026_11_12.yaml \
  params_file:=$HOME/tb3_nav2/config/nav2_params.yaml \
  use_sim_time:=false autostart:=true use_composition:=False
```

These commands use the laptop's known working directories. To run from a fresh clone, copy `navigation/maps/` and `navigation/config/nav2_params.yaml` to the equivalent `~/tb3_nav2/` paths first, or update the launch arguments to point into your clone.

## Terminal 4 — Nav2 navigation stack (laptop)

Only after `map_server` and `amcl` are `active [3]`, with `slam_toolbox` stopped:

```bash
source /opt/ros/jazzy/setup.bash
export ROS_DOMAIN_ID=0
ros2 launch nav2_bringup navigation_launch.py \
  params_file:=$HOME/tb3_nav2/config/nav2_params.yaml \
  use_sim_time:=false autostart:=true use_composition:=False
```

Do **not** launch a separate planner alongside this launch; it previously caused duplicate planner/costmap nodes.

## Terminal 5 — RViz (laptop)

```bash
source /opt/ros/jazzy/setup.bash
export ROS_DOMAIN_ID=0
rviz2 -d /opt/ros/jazzy/share/nav2_bringup/rviz/nav2_default_view.rviz
```

Select Fixed Frame `map`; Map `/map`; laser `/scan_normalized` (Best Effort QoS). Use **2D Pose Estimate** to set the robot's physical position and heading. Confirm live scan points align with the saved map and `map -> base_footprint` TF exists. The RViz **Navigation2 Goal** button submits a destination to Nav2; only use it after all safety checks.

## Terminal 6 — Read-only verification (laptop)

```bash
source /opt/ros/jazzy/setup.bash
export ROS_DOMAIN_ID=0
ros2 node list | sort | uniq -cd
for n in map_server amcl controller_server planner_server bt_navigator velocity_smoother collision_monitor; do
  echo "=== $n ==="
  timeout 5s ros2 lifecycle get "/$n" || true
done
ros2 param get /map_server yaml_filename
ros2 action list -t | grep navigate_to_pose
ros2 topic info -v /cmd_vel_nav
ros2 topic info -v /cmd_vel_smoothed
ros2 topic info -v /cmd_vel
ros2 topic info -v /scan_normalized
ros2 topic echo /battery_state --once --field voltage
```

Expected: only one `/map_server` and `/amcl`, no `/slam_toolbox` in saved-map mode; each required lifecycle node `active [3]`; `/navigate_to_pose` available; `/cmd_vel_nav` (controller) → `/cmd_vel_smoothed` (velocity smoother) → `/cmd_vel` (collision monitor) → OpenCR, using `geometry_msgs/msg/TwistStamped`. Check the complete publisher/subscriber chain rather than just topic names. Check live local costmap, footprint, and physical emergency stop.

## After a supervised goal / shutdown

- Record goal, start position, observed direction, outcome, recovery count, map and config revisions, battery, and video link.
- Cancel active goal, verify physical stop. `Ctrl+C` navigation, RViz, localization, normalizer; then robot bringup.
- On Pi, `sudo shutdown -h now` and wait for shutdown before removing power.
- Do **not** run `slam_toolbox` at the same time as AMCL in saved-map navigation mode.

## Optional — Create a fresh map instead

For mapping, run `slam_toolbox online_async_launch.py` with `slam/config/waffle_pi_async.yaml` instead of AMCL/Nav2. After supervised driving, export `.pgm`/`.yaml` with `nav2_map_server map_saver_cli` and, if needed, `.posegraph`/`.data` with `/slam_toolbox/serialize_map`. Verify files before stopping SLAM. See the project's SLAM section for details.
