#!/usr/bin/env python

import numpy as np
from pycrazyswarm import *
import rospy
from tf import TransformListener

if __name__ == "__main__":
    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper
    allcfs = swarm.allcfs

    cf28 = allcfs.crazyfliesById[28]
    iter = 0
    cfs = []
    # [1,2,3,4,6,8,10,14,15,16,17,18,20,21,25,26]
    for id in [1,2,3,4,6,10,14,15,16,17,18,20,21,25,26]:
        cfs.append(allcfs.crazyfliesById[id])
        iter = iter + 1

    for cf in cfs:
        cf.takeoff(targetHeight=1.0, duration=2.0)
    timeHelper.sleep(2.0)

    for cf in cfs:
        pos = np.array(cf.initialPosition) + np.array([0, -4.6, 0.4])
        cf.goTo(pos, 0, 6.0)
    timeHelper.sleep(7.0)

    print("press button to continue...")
    swarm.input.waitUntilButtonPressed()

    for i in range(0, 400):
        pos28 = np.array(cf28.position())
        x28 = pos28[0]
        y28 = pos28[1]

        for cf in cfs:
            pos = np.array(cf.initialPosition) + np.array([x28, 0,0.6])
            pos[1] = y28 + 1
            cf.goTo(pos, 0, 0.01)
            # print(pos)
        timeHelper.sleep(0.5)

    for cf in cfs:
        pos = np.array(cf.initialPosition) + np.array([0, 0.0, 0.4])
        cf.goTo(pos, 0, 6.0)
    timeHelper.sleep(10.0)

    allcfs.land(targetHeight=0.6, duration=4.0)
