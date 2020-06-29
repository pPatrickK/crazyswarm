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
    DISTANCE = 0.8 # in meter
    ALPHA = np.pi/4 # angle per secound
    ROTATIONSTEPS = 8 # Number of Rotations
    HEIGHT_MAX = 1
    HEIGHT_MIN = 0.4
    offset_x = 0
    offset_y = -1
    CENTROID_Z = 1
    RADIUS = 1

    #constants
    ALTITUDE = 0.5
    XMIN = -3
    YMIN = -2
    XMAX = 3
    YMAX = 2
    DISTANCE = 0.5# distance between 2 drones




    cfs = []
    # [1,3,4,6,8,10,14,15,17]
    # [1,2,3,4,6,8,10,14,15,16,17,18,20,21,25,26]

    iter = 0
    for id in [1,2,3,4,6,8,10,14,15,16,17,18,20,21,25,26]:
        cfs.append(allcfs.crazyfliesById[id])
        iter += 1

    circle_pos_x = np.sin(np.linspace(0,2*np.pi,iter+1))
    circle_pos_y = -np.cos(np.linspace(0,2*np.pi,iter+1))

    #takeoff
    for cf in cfs:
        cf.takeoff(targetHeight=1.0, duration=2.0)
    timeHelper.sleep(2.0)


    # # fly to start-position
    # iteration = 0
    # for cf in cfs:
    #     if iteration < int(iter/4):
    #         pos = np.array([XMAX, (YMAX+YMIN)/2+(-1.5+iteration%4)*DISTANCE, ALTITUDE])
    #     elif iteration < int(2*iter/4):
    #         pos = np.array([(XMAX+XMIN)/2+(1.5-iteration%4)*DISTANCE, YMIN, ALTITUDE])
    #     elif iteration < int(3*iter/4):
    #         pos = np.array([(XMAX+XMIN)/2+(1.5-iteration%4)*DISTANCE, YMAX, ALTITUDE])
    #     elif iteration < int(iter):
    #         pos = np.array([XMIN, (YMAX+YMIN)/2+(-1.5+iteration%4)*DISTANCE, ALTITUDE])
    #     iteration +=1
    #     cf.goTo(pos, 0, 8.0)
    #     timeHelper.sleep(1)
    # timeHelper.sleep(12.0)


    for cf,i in zip(cfs,range(iter)):
        #fly in parabel
        yScale = 0.5
        x = cf.position()[0]
        y = (-0.2*x**2+0.8*x+2)*yScale
        z = cf.position()[2]
        pos = np.array([x, y, z])
        cf.goTo(pos, 0, 5.0)
    timeHelper.sleep(5.0)




    k = 0.
    cfs1 = []
    cfs2 = []
    for cf in cfs:
        # split cfs into two groups
        if np.mod(k, 2):
            cfs1.append(cf)
        else:
            cfs2.append(cf)
        #fly in circle
        pos = np.array([RADIUS*np.sin(k/iter*2*np.pi), -RADIUS*np.cos(k/iter*2*np.pi), CENTROID_Z])
        cf.goTo(pos, 0, 5.0)
        k += 1
    timeHelper.sleep(5.0)

    # # change altitude to atomium-alignment
    # for cf in cfs1:
    #     x = cf.position()[0]
    #     y = cf.position()[1]
    #     z = x*x+CENTROID_Z
    #     pos = np.array([x, y, z])
    #     cf.goTo(pos,0,6.0)
    #
    # for cf in cfs2:
    #     x = cf.position()[0]
    #     y = cf.position()[1]
    #     z = -x*x+CENTROID_Z
    #     pos = np.array([x, y, z])
    #     cf.goTo(pos,0,6.0)
    # timeHelper.sleep(5.0)

    turns = 4.0
    # loop                               speed*turns
    for beta in np.linspace(0,2*np.pi*turns,20*turns):
        k = 0.0
        for cf in cfs:
            x = RADIUS*np.sin(k/iter*2*np.pi + beta)
            y = -RADIUS*np.cos(k/iter*2*np.pi + beta)
            z = x*x+CENTROID_Z
            pos = np.array([x, y, z])
            cf.goTo(pos,0,6.0)
            k += 1
        timeHelper.sleep(0.5)
    timeHelper.sleep(5.0)

    for cf in cfs:
        #fly in circle
        x = cf.initialPosition[0]
        y = (-0.2*x**2+0.8*x+2)*yScale
        z = cf.position()[2]
        pos = np.array([x, y, z])
        cf.goTo(pos, 0, 5.0)
    timeHelper.sleep(5.0)

    # fly home
    for cf in cfs:
        pos = np.array(cf.initialPosition) + np.array([0, 0.0, 0.4])
        cf.goTo(pos, 0, 6.0)
    timeHelper.sleep(5.0)

    allcfs.land(targetHeight=0.0, duration=4.0)
    timeHelper.sleep(5.0)
