#!/usr/bin/env python

import numpy as np
from pycrazyswarm import *
import datetime

def postionFinder(cf,pos):
    print(cf.position())
    print(pos)



Z = 0.20

if __name__ == "__main__":
    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper
    allcfs = swarm.allcfs

    time = datetime.datetime.now()

    allcfs.takeoff(targetHeight=Z, duration=2.0+Z)
    timeHelper.sleep(2.5+Z)

    print(datetime.datetime.now() - time)
    time = datetime.datetime.now()

    for cf in allcfs.crazyflies:
        pos = np.array(cf.initialPosition) + np.array([0, 0, Z])
        postionFinder(cf,pos)
        cf.goTo(pos, 0, 1.0)
    timeHelper.sleep(1.5)

    print(datetime.datetime.now() - time)
    time = datetime.datetime.now()

    for cf in allcfs.crazyflies:
        pos = np.array(cf.initialPosition) + np.array([0, 0, Z])
        postionFinder(cf,pos)
        cf.goTo(pos, 1, 1.0)
    timeHelper.sleep(1.5)

    print(datetime.datetime.now() - time)
    time = datetime.datetime.now()

    for cf in allcfs.crazyflies:
        pos = np.array(cf.initialPosition) + np.array([0, 0, Z])
        postionFinder(cf,pos)
        cf.goTo(pos, 2, 1.0)
    timeHelper.sleep(1.5)

    print(datetime.datetime.now() - time)
    time = datetime.datetime.now()

    for cf in allcfs.crazyflies:
        pos = np.array(cf.initialPosition) + np.array([0, 0, Z])
        postionFinder(cf,pos)
        cf.goTo(pos, 3, 1.0)
    timeHelper.sleep(1.5)

    print(datetime.datetime.now() - time)
    time = datetime.datetime.now()

    for cf in allcfs.crazyflies:
        pos = np.array(cf.initialPosition) + np.array([0, 0, Z])
        postionFinder(cf,pos)
        cf.goTo(pos, 4, 1.0)
    timeHelper.sleep(1.5)

    print(datetime.datetime.now() - time)
    time = datetime.datetime.now()

    allcfs.land(targetHeight=0.02, duration=1.0+Z)
    timeHelper.sleep(1.0+Z)
