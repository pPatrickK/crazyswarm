#!/usr/bin/env python

import numpy as np
from pycrazyswarm import *
import rospy
from tf import TransformListener
import time

mPoint = [0.0, 0.0, 0.0] # middle point of spiral [x, y, z]
r = 1.5
turns = 2

swarm = Crazyswarm()
timeHelper = swarm.timeHelper
allcfs = swarm.allcfs

# constants
ALTITUDE = 2.5
XMIN = -4.5
YMIN = -3.5
XMAX = 7.5
YMAX = 5
DISTANCE = 2# distance between 2 drones
################
iter = 0
cfs = []
# [1,2,3,4,5,6,7 ,8 ,9 ,10,11,12,13,14,15,16]
# [1,2,3,4,6,8,10,14,15,16,17,18,20,21,25,26]
for id in [1,2,3,4,6,8,10,14,15,16,17,18,20,21,25,26]:
    cfs.append(allcfs.crazyfliesById[id])
    iter = iter + 1
n = len(cfs)

circle_pos = [np.cos(np.linspace(0,2*np.pi*4,16)),np.sin(np.linspace(0,2*np.pi*4,16)), 0.0]
alpha = np.linspace(0,2*np.pi,17)

def rectform(flytime):
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
        print("position of cf:" + str(iteration)+" = "+ str(pos))
        cf.goTo(pos, 0, flytime)
    timeHelper.sleep(flytime + 1.0)

def spiralform():
    k = 0
    for i in [2,3,8,9,10,11,15,14,13,12,7,6,5,4,0,1]:
        cpos = mPoint + np.array([r*np.cos(alpha[k]), r*np.sin(alpha[k]), 0.8+k*0.1])
        cfs[i].goTo(cpos, 0, 6.0)
        k = k + 1
        timeHelper.sleep(0.5)
    timeHelper.sleep(8.0)

# loop
    for beta in np.linspace(0,2*np.pi*turns,10*turns):
        start = time.time()
        k = 0
        for i in [2,3,8,9,10,11,15,14,13,12,7,6,5,4,0,1]:
            cpos = mPoint + np.array([r*np.cos(alpha[k]+beta), r*np.sin(alpha[k]+beta), 0.8+k*0.1])
            cfs[i].goTo(cpos, 0, 2.0)
            k = k+1
        diff = time.time()-start
        print(time.time()-start)
        if diff < 0.5:
            timeHelper.sleep(0.5-diff)
    timeHelper.sleep(1.5)

def flyhomepos(flytime):
    for cf in cfs:
        pos = np.array(cf.initialPosition) + np.array([0, 0.0, 0.4])
        cf.goTo(pos, 0, flytime)
    timeHelper.sleep(flytime+1.0)

if __name__ == "__main__":

# takeoff and rectangle
    for cf in cfs:
        cf.takeoff(targetHeight=1.0, duration=2.0)
    timeHelper.sleep(2.0)
    # fly to start-position
    rectform(12.0)
    # iteration = 0
    # for cf in cfs:
    #     if iteration < 4:
    #         pos = np.array([XMAX, (YMAX+YMIN)/2+(-1.5+iteration%4)*DISTANCE, ALTITUDE])
    #     elif iteration < 8:
    #         pos = np.array([(XMAX+XMIN)/2+(1.5-iteration%4)*DISTANCE, YMIN, ALTITUDE])
    #     elif iteration < 12:
    #         pos = np.array([(XMAX+XMIN)/2+(1.5-iteration%4)*DISTANCE, YMAX, ALTITUDE])
    #     elif iteration < 16:
    #         pos = np.array([XMIN, (YMAX+YMIN)/2+(-1.5+iteration%4)*DISTANCE, ALTITUDE])
    #     iteration +=1
    #     print("position of cf:" + str(iteration)+" = "+ str(pos))
    #     cf.goTo(pos, 0, 8.0)
    # timeHelper.sleep(12.0)

# fly in circle
    # lsit for cricle
    # [7,8,13,14,15,16,12,11,10,9,4,3,2,1,5,6]
    #for i in reversed(range(0,n)):
    #-----
    spiralform()
    rectform(6.0)
#     k = 0
#     for i in [2,3,8,9,10,11,15,14,13,12,7,6,5,4,0,1]:
#         cpos = mPoint + np.array([r*np.cos(alpha[k]), r*np.sin(alpha[k]), 0.8+k*0.1])
#         cfs[i].goTo(cpos, 0, 6.0)
#         k = k + 1
#         timeHelper.sleep(0.5)
#     timeHelper.sleep(8.0)
#
# # loop
#     for beta in np.linspace(0,2*np.pi*turns,10*turns):
#         start = time.time()
#         k = 0
#         for i in [2,3,8,9,10,11,15,14,13,12,7,6,5,4,0,1]:
#             cpos = mPoint + np.array([r*np.cos(alpha[k]+beta), r*np.sin(alpha[k]+beta), 0.8+k*0.1])
#             cfs[i].goTo(cpos, 0, 2.0)
#             k = k+1
#         diff = time.time()-start
#         print(time.time()-start)
#         if diff < 0.5:
#             timeHelper.sleep(0.5-diff)
#     timeHelper.sleep(3.0)

# fly home
    flyhomepos(12.0)
    # iteration = 0
    # for cf in cfs:
    #     if iteration < 4:
    #         pos = np.array([XMAX, (YMAX+YMIN)/2+(-1.5+iteration%4)*DISTANCE, ALTITUDE])
    #     elif iteration < 8:
    #         pos = np.array([(XMAX+XMIN)/2+(1.5-iteration%4)*DISTANCE, YMIN, ALTITUDE])
    #     elif iteration < 12:
    #         pos = np.array([(XMAX+XMIN)/2+(1.5-iteration%4)*DISTANCE, YMAX, ALTITUDE])
    #     elif iteration < 16:
    #         pos = np.array([XMIN, (YMAX+YMIN)/2+(-1.5+iteration%4)*DISTANCE, ALTITUDE])
    #     iteration +=1
    #     print("position of cf:" + str(iteration)+" = "+ str(pos))
    #     cf.goTo(pos, 0, 6.0)
    # timeHelper.sleep(7.0)
    # for i in range(0,n):
    #     pos = np.array(cfs[i].initialPosition) + np.array([0, 0.0, 0.4])
    #     cfs[i].goTo(pos, 0, 8.0)
    #     timeHelper.sleep(0.5)
    # timeHelper.sleep(8.0)

    allcfs.land(targetHeight=0.6, duration=4.0)
    timeHelper.sleep(5.0)
