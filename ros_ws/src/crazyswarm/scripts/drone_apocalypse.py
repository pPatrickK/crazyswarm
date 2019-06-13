#!/usr/bin/env python

import numpy as np
from pycrazyswarm import *
import rospy
from tf import TransformListener

if __name__ == "__main__":
    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper
    allcfs = swarm.allcfs

    #constants
    ALTITUDE = 3
    XMIN = -4.5
    YMIN = -3.5
    XMAX = 7.5
    YMAX = 5
    DISTANCE = 2# distance between 2 drones

    iter = 0
    cfs = []
    # [1,2,3,4,6,8,10,14,15,16,17,18,20,21,25,26]
    for id in [1,2,3,4,6,8,10,14,15,16,17,18,20,21,25,26]:
        cfs.append(allcfs.crazyfliesById[id])
        iter = iter + 1

    # takeoff
    for cf in cfs:
        cf.takeoff(targetHeight=1.0, duration=2.0)
    timeHelper.sleep(2.0)


    # fly to start-position
    iteration = 0
    for cf in cfs:
        if iteration < 4:
            pos = np.array([XMAX, (YMAX+YMIN)/2+(-1.5+iteration%4)*DISTANCE, ALTITUDE])
        elif iteration < 8:
            pos = np.array([(XMAX+XMIN)/2+(1.5-iteration%4)*DISTANCE, YMIN, ALTITUDE])
        elif iteration < 12:
            pos = np.array([(XMAX+XMIN)/2+(1.5-iteration%4)*DISTANCE, YMAX, ALTITUDE])
        elif iteration < 16:
            pos = np.array([XMIN, (YMAX+YMIN)/2+(-1.5+iteration%4)*DISTANCE, ALTITUDE])
        iteration +=1
        cf.goTo(pos, 0, 6.0)
    timeHelper.sleep(8.0)


    #


    # fly home
    for cf in cfs:
        pos = np.array(cf.initialPosition) + np.array([0, 0.0, 0.4])
        cf.goTo(pos, 0, 6.0)
    timeHelper.sleep(10.0)

    allcfs.land(targetHeight=0.6, duration=4.0)
