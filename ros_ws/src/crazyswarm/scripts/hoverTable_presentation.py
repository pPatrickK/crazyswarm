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
        self.allcfs.land(targetHeight=1.05, duration=self.landTime)
        self.timeHelper.sleep(self.landTime+1)

    def takeoff(self, z, individual_time = 0.0, delta_wait = 0.5):
        if delta_wait >= individual_time:
            delta_wait = individual_time + 1.0
        for cf in self.allcfs.crazyflies:
            cf.takeoff(targetHeight=1.05+z, duration=self.startTime)
            self.timeHelper.sleep(individual_time)
        self.timeHelper.sleep(self.startTime + delta_wait)

    def move(self, delta_position, fly_time, individual_time = 0.0, delta_wait = 0.5):
        if delta_wait >= individual_time:
            delta_wait = individual_time + 1.0
        for cf in self.allcfs.crazyflies:
            pos = np.array(cf.initialPosition) + np.array(delta_position)
            cf.goTo(pos, 0, fly_time)
            self.timeHelper.sleep(individual_time)
        self.timeHelper.sleep(fly_time + delta_wait)

    def move_reverse(self, delta_position, fly_time, individual_time = 0.0, delta_wait = 0.5):
        if delta_wait >= individual_time:
            delta_wait = individual_time + 1.0
        for cf in reversed(self.allcfs.crazyflies):
            pos = np.array(cf.initialPosition) + np.array(delta_position)
            cf.goTo(pos, 0, fly_time)
            self.timeHelper.sleep(individual_time)
        self.timeHelper.sleep(fly_time + delta_wait)

    # def move_home(self, fly_time):
    #     for cf in reversed(self.allcfs.crazyflies):
    #         pos = np.array(cf.position())
    #         cf.hover(pos + np.array([0.0, 0.0, 0.25]), 0.0, 0.5)
    #         self.timeHelper.sleep(0.7)
    #         pos = np
    # def takeoff(self, z, individual_time = 0.0, delta_wait = 0.5):
    #     if delta_wait >= individual_time:
    #         delta_wait = individual_time + 1.0
    #     for cf in self.allcfs.crazyflies:
    #         cf.takeoff(targetHeight=1.05+z, duration=self.startTime)
    #         self.timeHelper.sleep(individual_time)
    #     self.timeHelper.sleep(self.startTime + delta_wait).array(cf.initialPosition)
    #     cf.hover(pos, 0, fly_time)
    #     self.timeHelper.sleep(individual_time)
    #
    #     pos[2] = pos[2] - 0.25
    #     cf.hover(pos, 0, 0.5)
    #     self.timeHelper.sleep(0.7)
    #
    #     self.timeHelper.sleep(fly_time + delta_wait)

    def move_group(self, delta_position, start, end, fly_time, individual_time = 0.0, delta_wait = 0.5):
        if delta_wait >= individual_time:
            delta_wait = individual_time + 1.0
        for i in range(start, end + 1):
            cf = self.allcfs.crazyfliesById[i]
            pos = np.array(cf.initialPosition) + np.array(delta_position)
            cf.goTo(pos, 0, fly_time)
            self.timeHelper.sleep(individual_time)
        self.timeHelper.sleep(fly_time + delta_wait)

    def move_group_reversed(self, delta_position, start, end, fly_time, individual_time = 0.0, delta_wait = 0.5):
        if delta_wait >= individual_time:
            delta_wait = individual_time + 1.0
        for i in range(end, start-1, -1):
            cf = self.allcfs.crazyfliesById[i]
            pos = np.array(cf.initialPosition) + np.array(delta_position)
            cf.goTo(pos, 0, fly_time)
            self.timeHelper.sleep(individual_time)
        self.timeHelper.sleep(fly_time + delta_wait)

    def move_individual(self, delta_position, id, fly_time):
        self.move_group(delta_position, id, id + 1, fly_time)

    def move_parallel(self, delta_positions, time, individual_time):
        cf_pos = zip(delta_positions, self.allcfs.crazyflies)
        for delta_pos, cf in cf_pos:
            pos = delta_pos
            cf.goTo(pos, 0, time)
            self.timeHelper.sleep(individual_time)
        self.timeHelper.sleep(time + individual_time)

    def move_parallel_new(self, delta_positions, time, individual_time):
        cf_pos = zip(delta_positions, self.allcfs.crazyflies)
        num_cfs = len(cf_pos)
        set1 = reversed(cf_pos[num_cfs/2 + 1 : ])
        set_mid = cf_pos[num_cfs/2 - 1 : num_cfs/2 + 1]
        set2 = cf_pos[ : num_cfs/2 - 1]
        set_all = zip(set1, set2)
        pos1, cf1 = set_mid[0]
        pos2, cf2 = set_mid[1]
        cf1.goTo(pos1, 0, time)
        cf2.goTo(pos2, 0, time)
        for d1, d2 in set_all:
            pos1, cf1 = d1
            pos2, cf2 = d2
            cf1.goTo(pos1, 0, time)
            cf2.goTo(pos2, 0, time)
            self.timeHelper.sleep(individual_time)
        self.timeHelper.sleep(time + individual_time)
        for d1, d2 in set_all:
            pos1, cf1 = d1
            pos2, cf2 = d2
            pos1[0] = pos1[0] + 9
            pos2[0] = pos2[0] - 9
            cf1.goTo(pos1, 0, time)
            cf2.goTo(pos2, 0, time)
            self.timeHelper.sleep(individual_time)
        self.timeHelper.sleep(time + individual_time)

    def wait(self, time):
        self.timeHelper.sleep(time)

    def takeoff_by_id(self, z, ids, start_time, individual_time = 0.0, delta_wait = 0.5):
        if delta_wait >= individual_time:
            delta_wait = individual_time + 1.0
        for id in ids:
            try:
                cf = self.allcfs.crazyfliesById[id]
                cf.takeoff(targetHeight=z, duration=start_time)
                if individual_time > 0.01:
                    self.timeHelper.sleep(individual_time + delta_wait)
            except:
                pass

    def land_by_id(self, z, ids, start_time, individual_time = 0.0, delta_wait = 0.5):
        if delta_wait >= individual_time:
            delta_wait = individual_time + 1.0
        for id in ids:
            try:
                cf = self.allcfs.crazyfliesById[id]
                cf.land(targetHeight=z, duration=start_time)
                if individual_time > 0.01:
                    self.timeHelper.sleep(individual_time + delta_wait)
            except:
                pass

    def move_by_id(self, delta_position, ids, fly_time, individual_time = 0.0, delta_wait = 0.5):
        if delta_wait >= individual_time:
            delta_wait = individual_time + 1.0
        for id in ids:
            try:
                cf = self.allcfs.crazyfliesById[id]
                pos = np.array(cf.initialPosition) + np.array(delta_position)
                cf.goTo(pos, 0, fly_time)
                if individual_time > 0.01:
                    self.timeHelper.sleep(individual_time + delta_wait)
            except:
                pass

    def move_absolute_by_id(self, delta_position, ids, fly_time, individual_time = 0.0, delta_wait = 0.5):
        if delta_wait >= individual_time:
            delta_wait = individual_time + 1.0
        for id in ids:
            try:
                cf = self.allcfs.crazyfliesById[id]
                pos = np.array(delta_position)
                cf.goTo(pos, 0, fly_time)
                if individual_time > 0.01:
                    self.timeHelper.sleep(individual_time + delta_wait)
            except:
                pass

    def move_relative_by_id(self, delta_position, ids, fly_time, individual_time = 0.0, delta_wait = 0.5):
        if delta_wait >= individual_time:
            delta_wait = individual_time + 1.0
        for id in ids:
            try:
                cf = self.allcfs.crazyfliesById[id]
                pos = cf.position() + np.array(delta_position)
                cf.goTo(pos, 0, fly_time)
                if individual_time > 0.01:
                    self.timeHelper.sleep(individual_time + delta_wait)
            except:
                pass


def present(swarmmover): # 1 2 3 4
    z_start = 1.0
    start_time = 2.0
    z_land = 0.2
    land_time = 4.0
    z_movement = 1.0

    swarmmover.takeoff_by_id(z_start, [15,16,17,18,19,20,21,22], start_time)
    swarmmover.wait(start_time + 0.5)

    swarmmover.move_absolute_by_id( [0.0, -0.9, z_movement], [22], 3.0)
    swarmmover.move_absolute_by_id( [0.3, -0.9, z_movement], [21], 3.0)
    swarmmover.move_absolute_by_id( [0.6, -0.9, z_movement], [20], 3.0)
    swarmmover.move_absolute_by_id( [0.9, -0.9, z_movement], [19], 3.0)
    swarmmover.move_absolute_by_id( [1.2, -0.9, z_movement], [18], 3.0)
    swarmmover.move_absolute_by_id( [1.5, -0.9, z_movement], [17], 3.0)
    swarmmover.move_absolute_by_id( [1.8, -0.9, z_movement], [16], 3.0)
    swarmmover.move_absolute_by_id( [2.1, -0.9, z_movement], [15], 3.0)
    swarmmover.wait(3.5)



    swarmmover.takeoff_by_id(z_start, [7,8,9,10,11,12,13,14], start_time)
    swarmmover.wait(start_time + 0.5)

    swarmmover.move_absolute_by_id( [0.0, 0.0, z_movement], [8], 3.0)
    swarmmover.move_absolute_by_id( [0.3, 0.0, z_movement], [7], 3.0)
    swarmmover.move_absolute_by_id( [0.6, 0.0, z_movement], [6], 3.0)
    swarmmover.move_absolute_by_id( [0.9, 0.0, z_movement], [5], 3.0)
    swarmmover.move_absolute_by_id( [1.2, 0.0, z_movement], [4], 3.0)
    swarmmover.move_absolute_by_id( [1.5, 0.0, z_movement], [3], 3.0)
    swarmmover.move_absolute_by_id( [1.8, 0.0, z_movement], [2], 3.0)
    swarmmover.move_absolute_by_id( [2.1, 0.0, z_movement], [1], 3.0)
    swarmmover.wait(3.5)


    ##---------------------------do something-----------------------------------




    ##--------------------------------------------------------------------------

    swarmmover.move_by_id( [0.0, 0.0, z_movement], [7,8,9,10,11,12,13,14], 3.0)
    swarmmover.wait(3.5)

    swarmmover.move_by_id( [0.0, 0.0, z_movement], [15,16,17,18,19,20,21,22], 3.0)
    swarmmover.land_by_id(z_land, [7,8,9,10,11,12,13,14], land_time)
    swarmmover.wait(3.5)

    swarmmover.land_by_id(z_land, [15,16,17,18,19,20,21,22], land_time)
    swarmmover.wait(land_time + 0.5)

def main():
    swarmmover = SwarmMover()
    present(swarmmover)

if __name__ == "__main__":
    main()
