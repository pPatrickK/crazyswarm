#!/usr/bin/env python

import numpy as np
from pycrazyswarm import *

if __name__ == "__main__":
    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper
    allcfs = swarm.allcfs

    allcfs.takeoff(targetHeight=1.0, duration=3.0)

    timeHelper.sleep(3.0)

    for cf in allcfs.crazyflies:
        pos = np.array(cf.initialPosition) + np.array([0, 0, 1.0])
        cf.goTo(pos, 0, 2.0)

    timeHelper.sleep(2.0)
    # for cf in allcfs.crazyflies:
    #     pos = np.array(cf.initialPosition) + np.array([1, -1, 1.0])
    #     cf.goTo(pos, 1.55, 2.0)
    #
    # timeHelper.sleep(2.0)

    for cf in allcfs.crazyflies:
        pos = np.array(cf.initialPosition) + np.array([1, -1, 1.0])
        cf.goTo(pos, 0, 2.0)

    timeHelper.sleep(2.0)

    allcfs.land(targetHeight=0.44, duration=12.0)
    timeHelper.sleep(12.0)
