#!/usr/bin/env python

import numpy as np
from pycrazyswarm import *

if __name__ == "__main__":
    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper
    allcfs = swarm.allcfs

    allcfs.takeoff(targetHeight=0.4, duration=2.0)

    timeHelper.sleep(2.0)

    for cf in allcfs.crazyflies:
        pos = np.array(cf.initialPosition) + np.array([0, 0, 0.4])
        cf.goTo(pos, 0, 2.0)

    timeHelper.sleep(2.0)


    for cf in allcfs.crazyflies:
        pos = np.array(cf.initialPosition) + np.array([1, -1, 0.4])
        cf.goTo(pos, 1.55, 2.0)

    timeHelper.sleep(2.0)

    for cf in allcfs.crazyflies:
        pos = np.array(cf.initialPosition) + np.array([1, -1, 0.52])
        cf.goTo(pos, 1.55, 2.0)

    timeHelper.sleep(2.0)

    for cf in allcfs.crazyflies:
        pos = np.array(cf.initialPosition) + np.array([1, -1, 0.52])
        cf.goTo(pos, 0, 2.0)

    timeHelper.sleep(2.0)

    # for cf in allcfs.crazyflies:
    #     pos = np.array(cf.initialPosition) + np.array([1, -1, 0.4])
    #     cf.goTo(pos, 1.55, 2.0)
    #
    # timeHelper.sleep(2.0)
    #
    # for cf in allcfs.crazyflies:
    #     pos = np.array(cf.initialPosition) + np.array([0, 0, 0.4])
    #     cf.goTo(pos, 0, 2.0)
    #
    # timeHelper.sleep(2.0)

    allcfs.land(targetHeight=0.44, duration=4.0)

    timeHelper.sleep(10.0)

    allcfs.takeoff(targetHeight=0.52, duration=4.0)

    for cf in allcfs.crazyflies:
        pos = np.array(cf.initialPosition) + np.array([1, -1, 0.52])
        cf.goTo(pos, 0, 2.0)

    timeHelper.sleep(2.0)

    for cf in allcfs.crazyflies:
        pos = np.array(cf.initialPosition) + np.array([1, -1, 0.52])
        cf.goTo(pos, 1.55, 2.0)

    timeHelper.sleep(2.0)

    for cf in allcfs.crazyflies:
        pos = np.array(cf.initialPosition) + np.array([1, -1, 0.4])
        cf.goTo(pos, 1.55, 2.0)

    timeHelper.sleep(2.0)

    for cf in allcfs.crazyflies:
        pos = np.array(cf.initialPosition) + np.array([0, 0, 0.4])
        cf.goTo(pos, 0, 2.0)

    timeHelper.sleep(2.0)

    allcfs.land(targetHeight=0.0, duration=2.0)
