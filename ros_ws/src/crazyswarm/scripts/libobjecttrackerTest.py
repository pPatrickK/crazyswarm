#!/usr/bin/env python

import numpy as np
from pycrazyswarm import *
import rospy
from tf import TransformListener

if __name__ == "__main__":
    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper
    allcfs = swarm.allcfs



    numberCfs = 0
    cfs = []
    # [1,2,3,4,6,8,10,14,15,16,17,18,20,21,25,26]
    for id in [1,2,3,4,6,8,10,14,15,16,17,18,20,21,25,26]:
        cfs.append(allcfs.crazyfliesById[id])
        numberCfs += 1

    #constants
    CENTERX = 0
    CENTERY = 0
    CENTERZ = 0.3
    RADIUS = 1 #meter
    ALPHA = 2*np.pi/numberCfs

    # rotationmatrix
    R=np.matrix([[np.cos(ALPHA),-np.sin(ALPHA),0],[np.sin(ALPHA),np.cos(ALPHA),0],[0,0,1]])


    # Takeoff
    for cf in cfs:
        cf.takeoff(targetHeight=1.0, duration=2.0)
    timeHelper.sleep(2.0)

    # fly into formation
    pos = np.array([CENTERX, CENTERY+RADIUS, CENTERZ])
    for cf in cfs:
        pos = np.dot(R,pos)
        pos = np.asarray(pos.T)
        pos = pos[0]
        cf.goTo(pos, 0, 6.0)
        #timeHelper.sleep(0.5)
    timeHelper.sleep(6)




    timeHelper.sleep(16.0)



    # fly home
    for cf in cfs:
        pos = np.array(cf.initialPosition) + np.array([0, 0.0, 0.4])
        cf.goTo(pos, 0, 6.0)
    timeHelper.sleep(10.0)

    allcfs.land(targetHeight=0.6, duration=4.0)
