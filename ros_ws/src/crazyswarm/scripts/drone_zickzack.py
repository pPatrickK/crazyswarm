#!/usr/bin/env python

import numpy as np
from pycrazyswarm import *
import rospy
from tf import TransformListener

if __name__ == "__main__":
    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper
    allcfs = swarm.allcfs

    iter = 0
    cfs = []
    # [1,2,3,4,6,8,10,14,15,16,17,18,20,21,25,26]
    for id in [1,2,3,4,6,8,10,14,15,16,17,18,20,21,25,26]:
        cfs.append(allcfs.crazyfliesById[id])
        iter = iter + 1

    for cf in cfs:
        cf.takeoff(targetHeight=1.0, duration=2.0)
    timeHelper.sleep(2.0)

    # fly to first position
    for i in range(0,len(cfs)):
        cf = cfs[len(cfs)-1-i]
        pos = np.array([-2+i, 0, 1.6])
        cf.goTo(pos, 0, 6.0)
        #timeHelper.sleep(0.5)
    timeHelper.sleep(8.0)


    # first drone fly zickzack
    init_pos = cfs[len(cfs)-1].position()+np.array([0.5,0,0])
    cfs[len(cfs)-1].goTo(init_pos,0,1)
    timeHelper.sleep(0.4)
    for i in range(0,len(cfs)):
        for Ts in range(0,4):
            pos = init_pos+np.array([i+float(Ts)/4,2*np.sin(np.pi*i+float(Ts)/4),0])
            cfs[len(cfs)-1].goTo(pos,-np.pi*np.cos(np.pi*i+float(Ts)/4),1)
            timeHelper.sleep(0.25)
    timeHelper.sleep(8.0)


    # fly home
    for cf in cfs:
        pos = np.array(cf.initialPosition) + np.array([0, 0.0, 0.4])
        cf.goTo(pos, 0, 6.0)
    timeHelper.sleep(10.0)

    allcfs.land(targetHeight=0.6, duration=4.0)
