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
    CENTERZ = 2
    PHI = np.pi/4 # rotation of circle 1
    DELTAPHI = np.pi/2 # rotation of circle 2 to circle 1
    RADIUS = 1
    ROTATIONX = np.pi/6
    ROTATIONY = 0
    ROTATIONZ = 0
    # SPINX = 0
    # SPINY = 0
    # SPINZ = 0
    TILT = np.pi/2
    ROTATIONSPEED = np.pi/6
    TIME = 100

    # rotationmatrix x
    RX=np.matrix([[1,0,0],[0,np.cos(ROTATIONX),-np.sin(ROTATIONX)],[0,np.sin(ROTATIONX),np.cos(ROTATIONX)]])
    # rotationmatrix y
    RY=np.matrix([[np.cos(ROTATIONY),0,np.sin(ROTATIONY)],[0,1,0],[-np.sin(ROTATIONY),0,np.cos(ROTATIONY)]])
    # rotationmatrix z
    RZ=np.matrix([[np.cos(ROTATIONZ),-np.sin(ROTATIONZ),0],[np.sin(ROTATIONZ),np.cos(ROTATIONZ),0],[0,0,1]])


    # Takeoff
    for cf in cfs:
        cf.takeoff(targetHeight=1.0, duration=2.0)
    timeHelper.sleep(2.0)


    # Circle1
    # x = RADIUS * np.sin(THETA) * np.cos(PHI)
    # y = RADIUS * np.sin(THETA) * np.sin(PHI)
    # z = RADIUS * np.cos(THETA)

    # Circle 1
    for i in range(0,len(cfs)/2):
        cf = cfs[i]
        x = RADIUS * np.sin(i*2*np.pi/(numberCfs/2)) * np.cos(PHI)
        y = RADIUS * np.sin(i*2*np.pi/(numberCfs/2)) * np.sin(PHI)
        z = RADIUS * np.cos(i*2*np.pi/(numberCfs/2))
        tempXYZ = np.array([x,y,z])
        tempXYZ = np.reshape(tempXYZ,(3,1))
        print str(tempXYZ)+"\n"
        XYZ = RX*RY*RZ*tempXYZ
        print str(XYZ)+"\n"
        pos = np.reshape(XYZ,(1,3))+np.array([CENTERX, CENTERY, CENTERZ])
        pos = pos.tolist()
        print str(np.shape(pos))
        print str(pos)
        cf.goTo(pos, 0, 6.0)
        #timeHelper.sleep(0.5)

    # Circle 2
    offset = 2*np.pi/(numberCfs)
    for i in range(len(cfs)/2,len(cfs)):
        cf = cfs[i]
        x = RADIUS * np.sin(i*2*np.pi/(numberCfs/2)+offset) * np.cos(PHI+DELTAPHI)
        y = RADIUS * np.sin(i*2*np.pi/(numberCfs/2)+offset) * np.sin(PHI+DELTAPHI)
        z = RADIUS * np.cos(i*2*np.pi/(numberCfs/2)+offset)
        XYZ = RX*RY*RZ*np.array([[x],[y],[z]])
        XYZ = np.transpose(XYZ)
        pos = XYZ[0]+np.array([CENTERX, CENTERY, CENTERZ])
        cf.goTo(pos, 0, 6.0)
        #timeHelper.sleep(0.5)
    timeHelper.sleep(6)

    # Move Circle
    for step in range(0,TIME):
        for i in range(0,len(cfs)):
            if i < (numberCfs/2):
                cf = cfs[i]
                x = RADIUS * np.sin(i*2*np.pi/(numberCfs/2)+step*ROTATIONSPEED) * np.cos(PHI)
                y = RADIUS * np.sin(i*2*np.pi/(numberCfs/2)+step*ROTATIONSPEED) * np.sin(PHI)
                z = RADIUS * np.cos(i*2*np.pi/(numberCfs/2)+step*ROTATIONSPEED)
                XYZ = RX*RY*RZ*np.array([[x],[y],[z]])
                XYZ = np.transpose(XYZ)
                pos = XYZ[0]+np.array([CENTERX, CENTERY, CENTERZ])
                cf.goTo(pos, 0, 1)
            if i >= (numberCfs/2):
                cf = cfs[i]
                x = RADIUS * np.sin(i*2*np.pi/(numberCfs/2)+offset+step*ROTATIONSPEED) * np.cos(PHI+DELTAPHI)
                y = RADIUS * np.sin(i*2*np.pi/(numberCfs/2)+offset+step*ROTATIONSPEED) * np.sin(PHI+DELTAPHI)
                z = RADIUS * np.cos(i*2*np.pi/(numberCfs/2)+offset+step*ROTATIONSPEED)
                XYZ = RX*RY*RZ*np.array([[x],[y],[z]])
                XYZ = np.transpose(XYZ)
                pos = XYZ[0]+np.array([CENTERX, CENTERY, CENTERZ])
                cf.goTo(pos, 0, 1)
        timeHelper.sleep(0.5)



    timeHelper.sleep(16.0)



    # fly home
    for cf in cfs:
        pos = np.array(cf.initialPosition) + np.array([0, 0.0, 0.4])
        cf.goTo(pos, 0, 6.0)
    timeHelper.sleep(10.0)

    allcfs.land(targetHeight=0.6, duration=4.0)
