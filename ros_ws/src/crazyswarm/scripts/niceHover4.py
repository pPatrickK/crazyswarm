#!/usr/bin/env python

import numpy as np
from pycrazyswarm import *

Z = 0.5

if __name__ == "__main__":
    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper
    allcfs = swarm.allcfs

    allcfs.takeoff(targetHeight=Z, duration=1.0+Z)
    timeHelper.sleep(1.5+Z)
    for cf in allcfs.crazyflies:
        pos = np.array(cf.initialPosition) + np.array([0, 1.5, 0.5])
        cf.goTo(pos, 0, 2.0)
    timeHelper.sleep(2.0+Z)

    for cf in allcfs.crazyflies:
        pos = np.array(cf.initialPosition) + np.array([9, 1.5, 0.5])
        cf.goTo(pos, 0, 7.0)
    timeHelper.sleep(7.1)

    for cf in allcfs.crazyflies:
        pos = np.array(cf.initialPosition) + np.array([-5, 1.5, 1.2])
        cf.goTo(pos, 0, 14)
    timeHelper.sleep(14.1)

    for cf in allcfs.crazyflies:
        pos = np.array(cf.initialPosition) + np.array([0, 0, 0.5])
        cf.goTo(pos, 0, 10)
    timeHelper.sleep(10.1)

    allcfs.land(targetHeight=0.02, duration=2.0+Z)
    timeHelper.sleep(2.0+Z)
