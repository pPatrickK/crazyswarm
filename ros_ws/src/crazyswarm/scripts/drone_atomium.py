#!/usr/bin/env python

import numpy as np
from pycrazyswarm import *
import rospy
from tf import TransformListener

if __name__ == "__main__":
    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper
    allcfs = swarm.allcfs



    nCF = 0
    cfs = []
    # [1,2,3,4,6,8,10,14,15,16,17,18,20,21,25,26]
    for id in [1,2,3,4,6,8,10,14,15,16,17,18,20,21,25,26]:
        cfs.append(allcfs.crazyfliesById[id])
        nCF += 1

    #constants
    CX = 0
    CY = 0
    CZ = 2

    n = 2# number of turns
    PHI = np.pi/4 # rotation of circle 1
    dPHI = np.pi/2 # rotation of circle 2 to circle 1
    r = 1
    rotX = np.pi/6
    rotY = 0
    rotZ = 0
    stepsize = np.pi/4
    # SPINX = 0
    # SPINY = 0
    # SPINZ = 0

    # TILT = np.pi/2
    # ROTATIONSPEED = np.pi/6
    # TIME = 100
    #
    # # rotationmatrix x
    # RX=np.matrix([[1,0,0],[0,np.cos(ROTATIONX),-np.sin(ROTATIONX)],[0,np.sin(ROTATIONX),np.cos(ROTATIONX)]])
    # # rotationmatrix y
    # RY=np.matrix([[np.cos(ROTATIONY),0,np.sin(ROTATIONY)],[0,1,0],[-np.sin(ROTATIONY),0,np.cos(ROTATIONY)]])
    # # rotationmatrix z
    # RZ=np.matrix([[np.cos(ROTATIONZ),-np.sin(ROTATIONZ),0],[np.sin(ROTATIONZ),np.cos(ROTATIONZ),0],[0,0,1]])


    # Takeoff
    for cf in cfs:
        cf.takeoff(targetHeight=1.0, duration=2.0)
    timeHelper.sleep(2.0)


    # Circle1
    # x = RADIUS * np.sin(THETA) * np.cos(PHI)
    # y = RADIUS * np.sin(THETA) * np.sin(PHI)
    # z = RADIUS * np.cos(THETA)

    # Circle 1
    print("c1 start")
    for i in range(0,len(cfs)/2):
        cf = cfs[i]
        x = r * np.sin(i*2*np.pi/(nCF/2))+ CX# * np.cos(PHI)
        y = r * np.cos(i*2*np.pi/(nCF/2))+ CY# * np.sin(PHI)
        z = x + CZ
        pos  = np.array([x,y,z])
        # print str(tempXYZ)+"\n"
        # XYZ = RX*RY*RZ*tempXYZ
        # print str(XYZ)+"\n"
        # pos = np.reshape(XYZ,(1,3))+np.array([CENTERX, CENTERY, CENTERZ])
        # pos = pos.tolist()
        # print str(np.shape(pos))
        # print str(pos)
        cf.goTo(pos, 0, 6.0)
        #timeHelper.sleep(0.5)

    print("c1 done")
    timeHelper.sleep(8)
    # Circle 2
    print("c2 start")
    for i in range(len(cfs)/2,len(cfs)):
        cf = cfs[i]
        x = r * np.sin(i*2*np.pi/(nCF/2)+ np.pi/8) + CX# * np.cos(PHI)
        y = r * np.cos(i*2*np.pi/(nCF/2)+ np.pi/8) + CY# * np.sin(PHI)
        z = -x + CZ
        pos  = np.array([x,y,z])

        cf.goTo(pos, 0, 6.0)
        #timeHelper.sleep(0.5)

    print("c2 done")
    timeHelper.sleep(8)

    # Move Circle
    for step in range(0,n*8):
        for i in range(0,len(cfs)):
            if i < (nCF/2):
                cf = cfs[i]
                x = r * np.sin(i*2*np.pi/(nCF/2)+ step*stepsize)+ CX# * np.cos(PHI)
                y = r * np.cos(i*2*np.pi/(nCF/2)+ step*stepsize )+ CY# * np.sin(PHI)
                z = x + CZ
                pos  = np.array([x,y,z])
                cf.goTo(pos, 0, 4)
            if i >= (nCF/2):
                cf = cfs[i]
                x = r * np.sin(i*2*np.pi/(nCF/2)+ np.pi/8 + step*stepsize) + CX# * np.cos(PHI)
                y = r * np.cos(i*2*np.pi/(nCF/2)+ np.pi/8 + step*stepsize) + CY# * np.sin(PHI)
                z = -x + CZ
                pos  = np.array([x,y,z])
                cf.goTo(pos, 0, 4)
        timeHelper.sleep(2)

    timeHelper.sleep(30.0)



    # fly home
    for cf in cfs:
        pos = np.array(cf.initialPosition) + np.array([0, 0.0, 0.4])
        cf.goTo(pos, 0, 6.0)
    timeHelper.sleep(10.0)

    allcfs.land(targetHeight=0.6, duration=4.0)
