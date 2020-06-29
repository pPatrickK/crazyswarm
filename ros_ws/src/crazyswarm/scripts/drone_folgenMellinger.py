#!/usr/bin/env python

import numpy as np
from pycrazyswarm import *
import rospy
from tf import TransformListener
import math as m

yaw = 0

if __name__ == "__main__":
    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper
    allcfs = swarm.allcfs

    cf32 = allcfs.crazyfliesById[32] # hunter drone
    # cf28 = allcfs.crazyfliesById[28] # prey drone
    #allcfs.takeoff(targetHeight=0.4, duration=2.0)
    #allcfs.takeoff(targetHeight=1, duration=2.0)
    cf32.takeoff(targetHeight=0.4, duration=2.0)
    timeHelper.sleep(2.0)

    # print("press button to continue...")
    # swarm.input.waitUntilButtonPressed()

    intervall = 0.5
    override = 0.8
    sleeptime = intervall*override
    followfor = 30
    followval = followfor/sleeptime
    turns = 3

    j = 0
    for i in np.linspace(0,m.pi*2*turns,8*turns):
        cpos =  np.array([m.cos(i), m.sin(i), 0.4])
        #if (i+m.pi/2-j*2*m.pi >= 2*m.pi):
        #    j = j + 1
        cf32.goTo(cpos, i+m.pi/2+m.pi/4, 1.3)
        yaw = i+m.pi/2+m.pi/4
        print((i+m.pi/2+m.pi/4) * 180 / m.pi)
        timeHelper.sleep(0.3)
    timeHelper.sleep(2.0)
    # for i in range(0, followval):
    #
    #     v28to26 = np.array(cf26.position()) - np.array(cf28.position())
    #     distance = np.linalg.norm(v28to26)
    #     if distance >= 1.0:
    #         factor = (distance - 1) / distance
    #         finishVector = np.multiply(v28to26, factor)
    #         pos = np.array(cf28.position() + finishVector)
    #         cf28.goTo(pos, 0, sleeptime)
    #         timeHelper.sleep(intervall)
    #     else:
    #         timeHelper.sleep(intervall)

    for cf in allcfs.crazyflies:
        pos = np.array(cf.initialPosition) + np.array([0.0, 0.0, 0.4])
        cf.goTo(pos, yaw, 6.0)
    timeHelper.sleep(7.0)

    allcfs.land(targetHeight=0.0, duration=2.0)
