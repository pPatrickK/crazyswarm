#!/usr/bin/env python

import numpy as np
from pycrazyswarm import *
import rospy
from tf import TransformListener

if __name__ == "__main__":
    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper
    allcfs = swarm.allcfs

    cf28 = allcfs.crazyfliesById[25] # hunter drone
    cf26 = allcfs.crazyfliesById[28] # prey drone
    #allcfs.takeoff(targetHeight=0.4, duration=2.0)
    #allcfs.takeoff(targetHeight=1, duration=2.0)
    cf28.takeoff(targetHeight=1, duration=2.0)
    timeHelper.sleep(2.0)

    print("press button to continue...")
    swarm.input.waitUntilButtonPressed()

    for i in range(0, 300):

        v28to26 = np.array(cf26.position()) - np.array(cf28.position())
        distance = np.linalg.norm(v28to26)
        if distance >= 1.0:
            factor = (distance - 1) / distance
            finishVector = np.multiply(v28to26, factor)
            pos = np.array(cf28.position() + finishVector)
            cf28.goTo(pos, 0, 0.001)
            timeHelper.sleep(0.1)
        else:
            timeHelper.sleep(0.1)

    for cf in allcfs.crazyflies:
        pos = np.array(cf.initialPosition) + np.array([0, 0.0, 0.4])
        cf.goTo(pos, 0, 6.0)
    timeHelper.sleep(10.0)

    allcfs.land(targetHeight=0.6, duration=4.0)
