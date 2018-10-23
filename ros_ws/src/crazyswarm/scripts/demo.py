#!/usr/bin/env python

import numpy as np

from pycrazyswarm import *
import uav_trajectory

if __name__ == "__main__":
    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper
    allcfs = swarm.allcfs

    traj1 = uav_trajectory.Trajectory()
    traj2 = uav_trajectory.Trajectory()
    traj3 = uav_trajectory.Trajectory()
    traj4 = uav_trajectory.Trajectory()

    traj1.loadcsv("a6_1_race.csv")
    traj2.loadcsv("a6_2_race.csv")
    traj3.loadcsv("a6_3_race.csv")
    traj4.loadcsv("a6_4_race.csv")


    cf1 = allcfs.crazyfliesById[1]
    cf2 = allcfs.crazyfliesById[2]
    cf3 = allcfs.crazyfliesById[3]
    cf4 = allcfs.crazyfliesById[4]

    cf1.setGroupMask(0b00000001)
    cf2.setGroupMask(0b00000010)
    cf3.setGroupMask(0b00000100)
    cf4.setGroupMask(0b00001000)

    z = 1.5
    TRIALS = 1
    TIMESCALE = 0.5
    for i in range(TRIALS):
        cf1.uploadTrajectory(0, 0, traj1) # req.trajectoryId, req.pieceOffset, pieces
        cf2.uploadTrajectory(0, 0, traj2)
        cf3.uploadTrajectory(0, 0, traj4)
        cf4.uploadTrajectory(0, 0, traj3)

        allcfs.takeoff(targetHeight=0.7, duration=2.0)
        timeHelper.sleep(2.5)



        pos1 = np.array(cf1.initialPosition) + np.array([1, -3.5, 0.3])
        cf1.goTo(pos1, 0, 5.0)
        pos3 = np.array(cf3.initialPosition) + np.array([1, -4.5, 0.4])
        cf3.goTo(pos3, 0, 5.0)
        timeHelper.sleep(2)
        pos2 = np.array(cf2.initialPosition) + np.array([1, -3.5, 0.2])
        cf2.goTo(pos2, 0, 5.0)
        pos4 = np.array(cf4.initialPosition) + np.array([1, -3.5, 0.1])
        cf4.goTo(pos4, 0, 5.0)
        timeHelper.sleep(5.5)



        allcfs.startTrajectory(0, TIMESCALE * 0.90, groupMask=0b00000001)
        allcfs.startTrajectory(0, TIMESCALE, groupMask=0b00000010)
        allcfs.startTrajectory(0, TIMESCALE * 0.78, groupMask=0b00000100)
        allcfs.startTrajectory(0, TIMESCALE * 1.3, groupMask=0b00001000)
        timeHelper.sleep(traj2.duration * TIMESCALE + 5)


        # pos1 = np.array(cf1.initialPosition) + np.array([1, -3.5, 0.3])
        # cf1.goTo(pos1, 0, 5.0)
        # pos3 = np.array(cf3.initialPosition) + np.array([1, -4.5, 0.4])
        # cf3.goTo(pos3, 0, 5.0)
        # pos2 = np.array(cf2.initialPosition) + np.array([1, -3.5, 0.2])
        # cf2.goTo(pos2, 0, 5.0)
        # pos4 = np.array(cf4.initialPosition) + np.array([1, -3.5, 0.1])
        # cf4.goTo(pos4, 0, 5.0)
        # timeHelper.sleep(5.5)

        allcfs.startTrajectory(0, TIMESCALE * 0.90, groupMask=0b00000001, reverse=True)
        allcfs.startTrajectory(0, TIMESCALE, groupMask=0b00000010, reverse=True)
        allcfs.startTrajectory(0, TIMESCALE * 0.78, groupMask=0b00000100, reverse=True)
        allcfs.startTrajectory(0, TIMESCALE * 1.3, groupMask=0b00001000, reverse=True)
        timeHelper.sleep(traj2.duration * TIMESCALE + 5)



        # pos1 = np.array(cf1.initialPosition) + np.array([0, -2.5, 0])
        # cf1.goTo(pos1, 0, 5.0)
        # pos2 = np.array(cf2.initialPosition) + np.array([0, -3, 0])
        # cf2.goTo(pos2, 0, 5.0)
        # pos3 = np.array(cf3.initialPosition) + np.array([0, -4, 0])
        # cf3.goTo(pos3, 0, 5.0)
        # pos4 = np.array(cf4.initialPosition) + np.array([0, -3, 0])
        # cf4.goTo(pos4, 0, 5.0)
        # timeHelper.sleep(5.5)


        pos1 = np.array(cf1.initialPosition) + np.array([1, -3.5, 0.3])
        cf1.goTo(pos1, 0, 5.0)
        pos3 = np.array(cf3.initialPosition) + np.array([1, -4.5, 0.4])
        cf3.goTo(pos3, 0, 5.0)
        pos2 = np.array(cf2.initialPosition) + np.array([1, -3.5, 0.2])
        cf2.goTo(pos2, 0, 5.0)
        pos4 = np.array(cf4.initialPosition) + np.array([1, -3.5, 0.1])
        cf4.goTo(pos4, 0, 5.0)
        timeHelper.sleep(5.5)

        for cf in allcfs.crazyflies:
            pos = np.array(cf.initialPosition) + np.array([0, 0, 0.3])
            cf.goTo(pos, 0, 5.0)
        timeHelper.sleep(5.5)

        allcfs.land(targetHeight=0.40, duration=2.0)
        timeHelper.sleep(3.0)
