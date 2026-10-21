# Autonomous Courier Challenge

A milestone-gated ROS 2 and Gazebo experiment for a differential-drive robot
that maps an indoor environment, navigates to at least five waypoints, responds
to obstacles, and records quantitative performance.

## Planned stack

- ROS 2 and a compatible Gazebo release
- Nav2 for planning, local control, and navigation behaviors
- SLAM Toolbox for mapping (where supported by the selected ROS distribution)
- ros2_control / diff-drive controller where compatible with the chosen simulator
- Python analysis scripts for repeatable trials

Verify the installed OS, ROS distribution, Gazebo version, and package compatibility
before installing dependencies. Do not replace a working ROS installation merely
to match a suggested version.

## Repository layout

- `docs/`: architecture, milestone gates, and experiment protocol
- `config/`: controller, SLAM, and Nav2 parameters
- `worlds/`: Gazebo worlds
- `maps/`: saved maps
- `data/raw/`: unmodified trial data
- `data/processed/`: derived data
- `results/`: plots and reports
- `scripts/`: data collection and analysis helpers
- `ros2_ws/src/`: ROS 2 packages

## Milestones

1. M0 — workspace and ROS 2 observability
2. M1 — robot model, kinematics, and simulation
3. M2 — wheel velocity P/PI/PID characterization
4. M3 — mapping, localization, and planning
5. M4 — autonomous waypoint mission and recovery
6. M5 — controlled experiments and final demonstration

Do not mark a milestone complete until its acceptance criteria and evidence are
saved. Record failures as well as successes.

## Initial setup

After sourcing the ROS 2 installation appropriate to this machine:

