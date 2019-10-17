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
    CENTROID_Z = 2
    RADIUS = 1.5
    RADIUS_FORMATION = 3
    CENTER_FORMATION = (0,0)

    #constants
    ALTITUDE = 0.5
    XMIN = -3
    YMIN = -2
    XMAX = 3
    YMAX = 2
    DISTANCE = 0.5# distance between 2 drones

    flytime = 5.0


    cfs = []
    # [1,3,4,6,8,10,14,15,17]
    # [1,2,3,4,6,8,10,14,15,16,17,18,20,21,25,26]
    # [32,31,30,29,28,27,24,23,22,19,13,12,11,9,7,5,26,25,21,20,18,17,16,15,14,10,8,6,4,3,2,1]
    # [1,2,3,4,6,8,10,14,15,16,17,18,20,21,25,26,5,7,9,11,12,13,19,22,23,24,27,28,29,30,31,32]
    # [32,31,30,29,28,27,24,23,22,19,13,12,11,9,7,5,1,2,3,4,6,8,10,14,15,16,17,18,20,21,25,26]
    iter = 0
    for id in [1,2,3,4,6,8,10,14,15,16,17,18,20,21,25,26,32,31,30,29,28,27,24,23,22,19,13,12,11,9,7,5]:
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

    # fly in circle
    deltaAngle = 2*np.pi/iter
    angleOffset = 0
    for cf,i in zip(cfs,range(iter)):
        x = CENTER_FORMATION[0]+RADIUS_FORMATION*np.cos(i*deltaAngle+angleOffset)
        y = CENTER_FORMATION[1]+RADIUS_FORMATION*np.sin(i*deltaAngle+angleOffset)
        z = cf.position()[2]
        pos = np.array([x, y, z])
        cf.goTo(pos, 0, flytime)
    timeHelper.sleep(flytime)




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
        cf.goTo(pos, 0, flytime)
        k += 1
    timeHelper.sleep(flytime)

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
    betaOffset = 2*np.pi/iter
    # loop                               speed*turns
    for beta in np.linspace(0,np.pi*turns,20*turns):
        k1 = 0.0
        for cf in cfs1:
            x = RADIUS*np.sin(4*k1/iter*np.pi + beta + betaOffset)
            y = -RADIUS*np.cos(4*k1/iter*np.pi + beta + betaOffset)
            # z = x*x+CENTROID_Z
            z = x+CENTROID_Z
            pos = np.array([x, y, z])
            cf.goTo(pos,0,flytime)
            k1 += 1
        k2 = 0.0
        for cf in cfs2:
            x = RADIUS*np.sin(4*k2/iter*np.pi + beta)
            y = -RADIUS*np.cos(4*k2/iter*np.pi + beta)
            # z = x*x+CENTROID_Z
            z = -x+CENTROID_Z
            pos = np.array([x, y, z])
            cf.goTo(pos,0,flytime)
            k2 += 1
        timeHelper.sleep(0.5)
    timeHelper.sleep(flytime+1)

    # fly in circle
    deltaAngle = 2*np.pi/iter
    angleOffset = 0
    for cf,i in zip(cfs,range(iter)):
        x = CENTER_FORMATION[0]+RADIUS_FORMATION*np.cos(i*deltaAngle+angleOffset)
        y = CENTER_FORMATION[1]+RADIUS_FORMATION*np.sin(i*deltaAngle+angleOffset)
        z = cf.position()[2]
        pos = np.array([x, y, z])
        cf.goTo(pos, 0, flytime)
    timeHelper.sleep(flytime+1)

    # fly home
    for cf in cfs:
        pos = np.array(cf.initialPosition) + np.array([0, 0.0, 0.4])
        cf.goTo(pos, 0, flytime)
    timeHelper.sleep(flytime+1)

    allcfs.land(targetHeight=0.6, duration=4.0)
    timeHelper.sleep(5.0)
