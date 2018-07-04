#!/usr/bin/env python

import numpy as np

from pycrazyswarm import *
import uav_trajectory

if __name__ == "__main__":
    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper
    allcfs = swarm.allcfs
    z = 0.4
    TIMESCALE = 1.0

    traj1 = uav_trajectory.Trajectory()
    traj1.loadcsv("figure8.csv")


    for cf in allcfs.crazyflies:
        cf.uploadTrajectory(0, 0, traj1)

    allcfs.takeoff(targetHeight=z, duration=2.0)
    timeHelper.sleep(2.5)
    for cf in allcfs.crazyflies:
        pos = np.array(cf.initialPosition) + np.array([0, 0, z])
        cf.goTo(pos, 0, 2.0)
    timeHelper.sleep(2.0)

    cf1 = allcfs.crazyflies[0]
    cf1.setGroupMask(0b00000001)
    cf2 = allcfs.crazyflies[1]
    cf2.setGroupMask(0b00000010)
    allcfs.startTrajectory(0, timescale=TIMESCALE, groupMask=0b00000001)
    timeHelper.sleep(traj1.duration * TIMESCALE + 2.0)

    for cf in allcfs.crazyflies:
        pos = np.array(cf.initialPosition) + np.array([0, 0, z])
        cf.goTo(pos, 0, 2.0)
    timeHelper.sleep(2.0)
    # allcfs.startTrajectory(0, timescale=TIMESCALE, reverse=True)
    # timeHelper.sleep(traj1.duration * TIMESCALE + 2.0)

    cf1.land(targetHeight=0.00, duration=2.0)
    timeHelper.sleep(2.0)
    cf2.land(targetHeight=0.00, duration=2.0)
    timeHelper.sleep(3.0)
    # allcfs.land(targetHeight=0.00, duration=2.0)
    # timeHelper.sleep(3.0)
