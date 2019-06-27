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
    centerX=0
    centerY=0
    centerZ=1
    DISTANCE = 0.5 #Distance between drones in [m]


    formation = [[centerX+3*DISTANCE,   centerY,            centerZ],
                [centerX+2*DISTANCE,    centerY-DISTANCE,   centerZ],
                [centerX+DISTANCE,      centerY-2*DISTANCE, centerZ],
                [centerX+DISTANCE,      centerY-DISTANCE,   centerZ],
                [centerX,               centerY-DISTANCE,   centerZ],
                [centerX-DISTANCE,      centerY-DISTANCE,   centerZ],
                [centerX-2*DISTANCE,    centerY-DISTANCE,   centerZ],
                [centerX-3*DISTANCE,    centerY-DISTANCE,   centerZ],
                [centerX-3*DISTANCE,    centerY,            centerZ],
                [centerX-3*DISTANCE,    centerY+DISTANCE,   centerZ],
                [centerX-2*DISTANCE,    centerY+DISTANCE,   centerZ],
                [centerX-DISTANCE,      centerY+DISTANCE,   centerZ],
                [centerX,               centerY+DISTANCE,   centerZ],
                [centerX+DISTANCE,      centerY+DISTANCE,   centerZ],
                [centerX+DISTANCE,      centerY+2*DISTANCE, centerZ],
                [centerX+2*DISTANCE,    centerY+DISTANCE,   centerZ]]

    numberCfs = 0
    cfs = []
    # [1,2,3,4,6,8,10,14,15,16,17,18,20,21,25,26]
    for id in [1,2,3,4,6,8,10,14,15,16,17,18,20,21,25,26]:
        cfs.append(allcfs.crazyfliesById[id])
        numberCfs += 1

    # takeoff
    for cf in cfs:
        cf.takeoff(targetHeight=1.0, duration=2.0)
    timeHelper.sleep(2.0)


    # fly to start-position
    for k in range(numberCfs):
        for iter in range(k+1):
            pos = formation[k-iter]
            cfs[iter].goTo(pos, 0, 3.0)
            iter += 1
        timeHelper.sleep(2)
    timeHelper.sleep(4.0)

    # fly show
    iter = 0
    for i in range(1,20):
        for cf in cfs:
            pos = np.array(cf.position())+np.array([DISTANCE,0,0])
            iter += 1
            cf.goTo(pos, 0, 2.0)
        timeHelper.sleep(0.5)
    timeHelper.sleep(4)


    # fly home
    for cf in cfs:
        pos = np.array(cf.initialPosition) + np.array([0, 0.0, 0.4])
        cf.goTo(pos, 0, 6.0)
    timeHelper.sleep(10.0)

    allcfs.land(targetHeight=0.6, duration=4.0)
