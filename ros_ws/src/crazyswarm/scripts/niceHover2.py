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
        pos = np.array(cf.initialPosition) + np.array([0, 0, Z])
        cf.goTo(pos, 0, 2.0)
    timeHelper.sleep(2.0+Z)

    for cf in allcfs.crazyflies:
        pos = np.array(cf.initialPosition) + np.array([2, 2, Z])
        cf.goTo(pos, 0, 3.0)
    timeHelper.sleep(3.0+Z)

    for cf in allcfs.crazyflies:
        pos = np.array(cf.initialPosition) + np.array([0, 2, Z])
        cf.goTo(pos, 0, 3.0)
    timeHelper.sleep(3.0+Z)

    for cf in allcfs.crazyflies:
        pos = np.array(cf.initialPosition) + np.array([0, 0, Z])
        cf.goTo(pos, 0, 3.0)
    timeHelper.sleep(3.0+Z)

    allcfs.land(targetHeight=0.02, duration=2.0+Z)
    timeHelper.sleep(2.0+Z)
