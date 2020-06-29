#!/usr/bin/env python

import numpy as np
from pycrazyswarm import *
import rospy
from tf import TransformListener
import time

mPoint = [0.0, 0.0, 0.0] # middle point of spiral [x, y, z]
r = 1.5

turns = 2

circle_pos = [np.cos(np.linspace(0,2*np.pi*4,16)),np.sin(np.linspace(0,2*np.pi*4,16)), 0.0]

alpha = np.linspace(0,2*np.pi,17)

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

    n = len(cfs)

# takeoff
    for i in reversed(range(0,n)):
        cfs[i].takeoff(targetHeight=0.8+i*0.1, duration=2.0)
    timeHelper.sleep(2.0)

# fly in circle
    for i in reversed(range(0,n)):
        cpos = mPoint + np.array([r*np.cos(alpha[i]), r*np.sin(alpha[i]), 0.8+i*0.1])
        cfs[i].goTo(cpos, 0, 8.0)
        timeHelper.sleep(0.5)
    timeHelper.sleep(8.0)

# loop
    for beta in np.linspace(0,2*np.pi*turns,10*turns):
        start = time.time()
        for i in reversed(range(0,n)):
            cpos = mPoint + np.array([r*np.cos(alpha[i]+beta), r*np.sin(alpha[i]+beta), 0.8+i*0.1])
            cfs[i].goTo(cpos, 0, 2.0)
        diff = time.time()-start
        print(time.time()-start)
        if diff < 0.5:
            timeHelper.sleep(0.5-diff)
    timeHelper.sleep(3.0)

# fly home
    for i in range(0,n):
        pos = np.array(cfs[i].initialPosition) + np.array([0, 0.0, 0.4])
        cfs[i].goTo(pos, 0, 8.0)
        timeHelper.sleep(0.5)
    timeHelper.sleep(8.0)

    allcfs.land(targetHeight=0.6, duration=4.0)
    timeHelper.sleep(5.0)
