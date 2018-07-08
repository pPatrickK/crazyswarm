#!/bin/bash
source ros_ws/devel/setup.bash

python ros_ws/src/crazyswarm/scripts/shut_down_drones_sh.py

wait
echo "Alle Drohnen sind aus"

python ros_ws/src/crazyswarm/scripts/test_positions_sh.py

wait
echo "Fertig. Alle Drohnen überprüft?"

roslaunch crazyswarm hover_swarm.launch

wait

python ros_ws/src/crazyswarm/scripts/shut_down_drones_sh.py
