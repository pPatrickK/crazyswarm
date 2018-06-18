#!/usr/bin/env python

import numpy as np
from pycrazyswarm import *

z1 = 1.2
z2 = 1.4
z3 = 1.7

if __name__ == "__main__":
    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper
    allcfs = swarm.allcfs
    cf3 = allcfs.crazyfliesById[3]
    cf2 = allcfs.crazyfliesById[2]
    # cf3 = allcfs.crazyfliesById[3]
    # cf4 = allcfs.crazyfliesById[4]
    cf5 = allcfs.crazyfliesById[5]
    cf6 = allcfs.crazyfliesById[6]
    # cf7 = allcfs.crazyfliesById[7]
    # cf8 = allcfs.crazyfliesById[8]

    cf3.takeoff(targetHeight=z3, duration=2.9)
    cf5.takeoff(targetHeight=z3, duration=2.9)

    cf2.takeoff(targetHeight=z2, duration=2.9)
    cf6.takeoff(targetHeight=z2, duration=2.9)

    # cf3.takeoff(targetHeight=1.0, duration=2.5)
    # cf7.takeoff(targetHeight=1.0, duration=2.5)

    # cf4.takeoff(targetHeight=z1, duration=2.5)
    # cf8.takeoff(targetHeight=z1, duration=2.5)
    timeHelper.sleep(3)


    for cf in allcfs.crazyflies:
        pos = np.array(cf.initialPosition) + np.array([12, 0, 1.5])
        cf.goTo(pos, 0, 17.0)
    timeHelper.sleep(17.2)

    allcfs.land(targetHeight=0.02, duration=4.0)
    timeHelper.sleep(4.1)

    # allcfs.takeoff(targetHeight=Z, duration=1.0+Z)
    # timeHelper.sleep(1.5+Z)
    # for cf in allcfs.crazyflies:
    #     pos = np.array(cf.initialPosition) + np.array([0, 0, Z])
    #     cf.goTo(pos, 0, 1.0)
    #
    # print("press button to continue...")
    # swarm.input.waitUntilButtonPressed()
    #
    # allcfs.land(targetHeight=0.02, duration=1.0+Z)
    # timeHelper.sleep(1.0+Z)
