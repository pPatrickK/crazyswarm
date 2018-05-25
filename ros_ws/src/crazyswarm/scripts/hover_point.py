#!/usr/bin/env python

import numpy as np
from pycrazyswarm import *

class SwarmMover(object):
    def __init__(self):
        self.swarm = Crazyswarm()
        self.timeHelper = self.swarm.timeHelper
        self.allcfs = self.swarm.allcfs
        self.startTime = 1.0
        self.landTime = 2.5

    def all_takeoff(self, z):
        self.allcfs.takeoff(targetHeight=1.05+z, duration=self.startTime)
        self.timeHelper.sleep(self.startTime+1)

    def all_land(self):
        self.allcfs.land(targetHeight=0.05, duration=self.landTime)
        self.timeHelper.sleep(self.landTime+1)

    def move(self, delta_position, fly_time, individual_time = 0.0, delta_wait = 0.5):
        if delta_wait >= individual_time:
            delta_wait = individual_time + 1.0
        for cf in self.allcfs.crazyflies:
            pos = np.array(cf.initialPosition) + np.array(delta_position)
            cf.goTo(pos, 0, fly_time)
            self.timeHelper.sleep(individual_time)
        self.timeHelper.sleep(fly_time + delta_wait)

    def waitInput(self):
        print("press button to continue...")
        self.swarm.input.waitUntilButtonPressed()

    def notPressed(self):
        return (not self.swarm.input.checkKeyboardPressed())

def main():
    swarmmover = SwarmMover()

    swarmmover.all_takeoff(0.3)

    swarmmover.waitInput()

    while (swarmmover.notPressed()):
        swarmmover.move(np.array([1, 0, 0.3]), 1)
        swarmmover.move(np.array([0, 0, 0.3]), 1)

    swarmmover.waitInput()

    swarmmover.all_land()

if __name__ == "__main__":
    main()
