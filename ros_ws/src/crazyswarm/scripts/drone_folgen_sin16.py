#!/usr/bin/env python

import numpy as np
from pycrazyswarm import *
import rospy
from tf import TransformListener
import time

HEIGHT = 1.5

turns = 4
s = 6

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
    t = np.hstack((np.linspace(0,np.pi*2*(turns),s*(turns)),np.zeros(n)))

    # start positions
    for i in range(0,n):
        cfs[i].takeoff(targetHeight=HEIGHT+np.sin(t[i])*0.5, duration=2.0)
    timeHelper.sleep(2.0)

    #for cf in cfs:
    #    pos = np.array(cf.initialPosition) + np.array([0, -4.6, 0.4])
    #    cf.goTo(pos, 0, 6.0)
    #timeHelper.sleep(7.0)

    #print("press button to continue...")
    #swarm.input.waitUntilButtonPressed()

    for i in range(0,s*turns):
        start = time.time()
        for j in range(0,n):
            cf = cfs[j]
            cpos =  np.array(cf.initialPosition) + np.array([0.0, 0.0, HEIGHT-0.6+np.sin(t[j+i])*0.5])
            cf.goTo(cpos, 0, 2)
        diff = time.time()-start
        print(time.time()-start)
        if diff < 0.5:
            timeHelper.sleep(0.5-diff)

    for cf in cfs:
        pos = np.array(cf.initialPosition) + np.array([0, 0.0, 0.4])
        cf.goTo(pos, 0, 6.0)
    timeHelper.sleep(7.0)

    allcfs.land(targetHeight=0.6, duration=4.0)
    timeHelper.sleep(5.0)
