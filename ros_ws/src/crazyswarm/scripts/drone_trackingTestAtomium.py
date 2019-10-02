import numpy as np
from pycrazyswarm import *
import rospy
from tf import TransformListener

if __name__ == "__main__":
    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper
    allcfs = swarm.allcfs


mPoint = [0.0, 0.0, 0.0] # middle point of spiral [x, y, z]
r_a = 2.0
r_s = 1.5
turns = 2

swarm = Crazyswarm()
timeHelper = swarm.timeHelper
allcfs = swarm.allcfs

# constants
ALTITUDE = 0.4
XMIN = -3
YMIN = -2
XMAX = 3
YMAX = 2
DISTANCE = 0.8# distance between 2 drones
################
iter = 0

cfs = []
# [1,2,3,4,5,6,7 ,8 ,9 ,10,11,12,13,14,15,16]
# [1,2,3,4,6,8,10,14,15,16,17,18,20,21,25,26]
#for photoshooting
# cf32 = allcfs.crazyfliesById[32]
#
for id in [1,2,3,4,6,8,10,14,15,16,17,18,20,21,25,26]:
    cfs.append(allcfs.crazyfliesById[id])
    iter = iter + 1
n = len(cfs)

circle_pos = [np.cos(np.linspace(0,2*np.pi*4,16)),np.sin(np.linspace(0,2*np.pi*4,16)), 0.0]
alpha = np.linspace(0,2*np.pi,17)



# fly in circle
k = 0
for i in [2,3,8,9,10,11,15,14,13,12,7,6,5,4,0,1]:
    x = r_a*np.cos(alpha[k])
    y = r_a*np.sin(alpha[k])
    if i in [2,8,10,15,13,7,5,0]:
        z = x/2 + 1.5
    else:
        z = -x/2 +1.5
    cpos = mPoint + np.array([x,y,z])
    cfs[i].goTo(cpos, 0, 6.0)
    k = k + 1
    # timeHelper.sleep(0.5)
timeHelper.sleep(8.0)
# loop                                      speed*turns
for beta in np.linspace(0,2*np.pi*turns,20*turns):
    start = time.time()
    k = 0
    for i in [2,3,8,9,10,11,15,14,13,12,7,6,5,4,0,1]:
        x = r_a*np.cos(alpha[k]+beta)
        y = r_a*np.sin(alpha[k]+beta)
        if i in [2,8,10,15,13,7,5,0]:
            z = x/2 + 1.5
        else:
            z = -x/2 +1.5
        cpos = mPoint + np.array([x,y,z])
        cfs[i].goTo(cpos, 0, 2.0)
        k = k+1
    diff = time.time()-start
    print(time.time()-start)
    if diff < 0.5:
        timeHelper.sleep(0.5-diff)
timeHelper.sleep(3.0)
