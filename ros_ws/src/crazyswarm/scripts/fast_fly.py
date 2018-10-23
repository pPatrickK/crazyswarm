#!/usr/bin/env python

import numpy as np
from pycrazyswarm import *
import rospy
from tf import TransformListener

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
        pos = np.array(cf.initialPosition) + np.array([4, -1.5, 0.4])
        cf.goTo(pos, 0, 2.35)
    timeHelper.sleep(5.0)

    for cf in allcfs.crazyflies:
        pos = np.array(cf.initialPosition) + np.array([1, 1, 0.4])
        cf.goTo(pos, 0, 2.35)

    timeHelper.sleep(20.0)

    # timeHelper.sleep(2.0)
    #
    # cf = allcfs.crazyfliesById[28] #28
    # deviation = np.array([0,0,0])
    # for x in range(0, 100):
    #     deviation = np.array(deviation) + (cf.position()-np.array([1.0,-1.0,0.4]) )
    #     print ((cf.position()-np.array([1.0,-1.0,0.4]) ))
    #     timeHelper.sleep(0.2)
    #
    # deviation = np.array(deviation)/100;
    # print(deviation)
    #
    for cf in allcfs.crazyflies:
        pos = np.array(cf.initialPosition) + np.array([0, 0, 0.4])
        cf.goTo(pos, 0, 2.0)
    timeHelper.sleep(4.0)

    allcfs.land(targetHeight=0.0, duration=4.0)
