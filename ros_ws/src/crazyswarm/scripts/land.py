#!/usr/bin/env python

import numpy as np
from pycrazyswarm import *

if __name__ == "__main__":
    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper
    allcfs = swarm.allcfs

    allcfs.land(targetHeight=0.0, duration=3.0)
    timeHelper.sleep(3.5)
