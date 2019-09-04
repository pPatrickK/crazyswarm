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
    DISTANCE = 1 # in meter
    ALPHA = np.pi/4 # angle per secound
    ROTATIONSTEPS = 8 # Number of Rotations
    HEIGHT_MAX = 1
    HEIGHT_MIN = 0.4



    iter = 0
    cfs = []
    # [1,2,3,4,6,8,10,14,15,16,17,18,20,21,25,26]
    for id in [6,8,10,14,15,16,17,18,20]:
        cfs.append(allcfs.crazyfliesById[id])
        iter = iter + 1

    #takeoff
    for cf in cfs:
        cf.takeoff(targetHeight=1.0, duration=2.0)
    timeHelper.sleep(2.0)

    #fly to the center of the hall
    drone_number=0
    for iter_y in range(0,int(np.sqrt(iter))):
        for iter_x in range(0,int(np.sqrt(iter))):
            pos = np.array([DISTANCE*(1.5-iter_x), DISTANCE*(iter_y-1.5), HEIGHT_MAX])
            cfs[drone_number].goTo(pos, 0, 6.0)
            drone_number += 1
        timeHelper.sleep(0.5)
    timeHelper.sleep(5.0)

    # lower altitude
    for cf in cfs:
        pos = cf.position()-np.array([0,0,HEIGHT_MAX-HEIGHT_MIN])
        cf.goTo(pos,0,3.0)
    timeHelper.sleep(2.0)

    #rotate
    RZ = np.matrix([[np.cos(ALPHA),-np.sin(ALPHA),0],[np.sin(ALPHA),np.cos(ALPHA),0],[0,0,1]])
    for i in range(0,ROTATIONSTEPS):
        for cf in cfs:
            TEMPpos = RZ*np.array(cf.position()).reshape((3,1))
            pos = np.asarray(np.transpose(TEMPpos))
            pos = pos[0]
            cf.goTo(pos, 0,2.0)
        timeHelper.sleep(2.0)
    timeHelper.sleep(2.0)

    # #fly to the homeposition
    # drone_number=0
    # for index in range(iter-1,-1,-1):
    #     pos = np.array(cfs[index].initialPosition) + np.array([0, 0.0, 0.4])
    #     cfs[index].goTo(pos, 0, 6.0)
    #     timeHelper.sleep(0.5)
    # timeHelper.sleep(5.0)

    # higher altitude
    for cf in cfs:
        pos = cf.position()+np.array([0,0,HEIGHT_MAX-HEIGHT_MIN])
        cf.goTo(pos,0,3.0)
    timeHelper.sleep(5.0)

    #fly to homeposition
    drone_number=iter
    for iter_y in range(0,int(np.sqrt(iter))):
        for iter_x in range(0,int(np.sqrt(iter))):
            pos = np.array(cfs[drone_number-1].initialPosition) + np.array([0, 0.0, 0.4])
            cfs[drone_number-1].goTo(pos, 0, 6.0)
            drone_number -= 1
        timeHelper.sleep(0.5)
    timeHelper.sleep(5.0)

    allcfs.land(targetHeight=0.6, duration=4.0)
    timeHelper.sleep(5.0)
