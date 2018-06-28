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

def old(): # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    z = 0.3
    individual_takeoff = 0.015
    individual_move = 0.1
    swarmmover = SwarmMover()
    swarmmover.takeoff(z, individual_takeoff)

    swarmmover.move_parallel_new([[5.0, 4.0, z], [5.0, 4.5, z], [5.0, 5.0, z], [5.0, 5.5, z], [5.0, 6.0, z], [5.0, 6.5, z], [5.0, 7.0, z], [5.0, 7.5, z], [5.0, 8.0, z],
         [1.5, 2.0, z], [1.0, 2.0, z],
         [-4.0, 7.75, z], [-4.0, 7.25, z], [-4.0, 6.75, z], [-4.0, 6.25, z], [-4.0, 5.75, z], [-4.0, 5.25, z], [-4.0, 4.75, z], [-4.0, 4.25, z], [-4.0, 3.75, z]] , 20.0, 1.5)
         #[5.0, 8.0, z], [5.0, 7.5, z], [5.0, 7.0, z], [5.0, 6.5, z], [5.0, 6.0, z], [5.0, 5.5, z], [5.0, 5.0, z], [5.0, 4.5, z] ,[5.0, 4.0, z],
         #[-4.0, 3.75, z], [-4.0, 4.25, z], [-4.0, 4.75, z], [-4.0, 5.25, z], [-4.0, 5.75, z], [-4.0, 6.25, z], [-4.0, 6.75, z], [-4.0, 7.25, z], [-4.0, 7.75, z]
    #swarmmover.move_reverse([0.0, 0.0, z], 10.0, 1.5)
    swarmmover.move_group_reversed([0.0, 0.0, z], 12, 20, 20.0, 1.5)
    swarmmover.move_group([0.0, 0.0, z], 1, 12, 20.0, 1.5)
    swarmmover.all_land()
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

def group_1(swarmmover): # 1 2 3 4
    z_start = 1.0
    start_time = 2.0
    z_land = 0.2
    land_time = 2.0
    z_movement = 1.0

    swarmmover.takeoff_by_id(z_start, [1,2,3,4,5,6,7,8,9,10], start_time)
    swarmmover.wait(start_time + 0.5)

    swarmmover.move_by_id( [1.0, 0.0, z_movement], [1,2,3,4,5,6,7,8,9,10], 3.0)
    swarmmover.wait(3.5)



    swarmmover.takeoff_by_id(z_start, [20,21,22,23,24,25,26,27,28,29], start_time)
    swarmmover.wait(start_time + 0.5)

    swarmmover.move_by_id( [-1.0, 0.0, z_movement], [20,21,22,23,24,25,26,27,28,29], 3.0)
    swarmmover.wait(3.5)



    swarmmover.takeoff_by_id(z_start, [11,12,13,14,15,16,17,18,19], start_time)
    swarmmover.wait(start_time + 0.5)

    swarmmover.move_by_id( [-0.5, 0.0, z_movement], [11,12,13,14,15,16,17,18,19], 2.0)
    swarmmover.wait(2.5)
    swarmmover.move_by_id( [1.0, 0.0, z_movement], [11,12,13,14,15,16,17,18,19], 3.0)
    swarmmover.wait(3.5)
    swarmmover.move_by_id( [0.0, 0.0, z_movement], [11,12,13,14,15,16,17,18,19], 2.0)
    swarmmover.wait(2.5)

    swarmmover.move_by_id( [0.0, 0.0, z_movement], [1,2,3,4,5,6,7,8,9,10], 3.0)
    swarmmover.land_by_id(z_land, [11,12,13,14,15,16,17,18,19], land_time)
    swarmmover.wait(3.5)

    swarmmover.move_by_id( [0.0, 0.0, z_movement], [20,21,22,23,24,25,26,27,28,29], 3.0)
    swarmmover.wait(3.5)

    swarmmover.land_by_id(z_land, [20,21,22,23,24,25,26,27,28,29], land_time)
    swarmmover.wait(land_time + 0.5)

def group_2(swarmmover): #17 18 19 20
    swarmmover.takeoff_by_id(0.1, [17, 18, 19, 20], 1.0)
    swarmmover.wait(1.5)

    swarmmover.move_by_id( [2.0, 0.0, 2.0], [20], 5.0)
    swarmmover.move_by_id( [2.0, 0.5, 0.5], [19], 5.0)
    swarmmover.move_by_id( [2.0, -0.5, 0.5], [18], 5.0)
    swarmmover.move_by_id( [2.0, 0.0, 2.0], [17], 5.0)
    swarmmover.wait(5.5)

    swarmmover.move_absolute_by_id( [1.0, 3.5, 2.0], [20], 5.0)
    swarmmover.move_absolute_by_id( [1.0, 5.0, 2.0], [19], 5.0)
    swarmmover.move_absolute_by_id( [1.0, 5.0, 0.5], [18], 5.0)
    swarmmover.move_absolute_by_id( [1.0, 3.5, 0.5], [17], 5.0)
    swarmmover.wait(5.5)

    swarmmover.move_by_id( [0.0, 0.0, 0.0], [20], 4.0)
    swarmmover.wait(0.5)
    swarmmover.move_by_id( [0.0, 0.0, 0.0], [19], 4.0)
    swarmmover.wait(0.5)
    swarmmover.move_by_id( [0.0, 0.0, 0.0], [18], 4.0)
    swarmmover.wait(0.5)
    swarmmover.move_by_id( [0.0, 0.0, 0.0], [17], 4.0)
    swarmmover.wait(4.5)

    swarmmover.land_by_id(0.0, [17, 18, 19, 20], 0)
    swarmmover.wait(0.2)

def group_3_start(swarmmover): # 5 6 7 8
    swarmmover.takeoff_by_id(1.5, [5], 2.5)
    swarmmover.wait(0.5)
    swarmmover.takeoff_by_id(1.5, [6], 2.5)
    swarmmover.wait(0.5)
    swarmmover.takeoff_by_id(1.5, [7], 2.5)
    swarmmover.wait(0.5)
    swarmmover.takeoff_by_id(1.5, [8], 2.5)
    swarmmover.wait(1.0)
    swarmmover.move_by_id( [0.25, 0.0, 1.5], [5], 1.5)
    swarmmover.wait(0.5)
    swarmmover.move_by_id( [0.5, 0.0, 1.5], [6], 1.5)
    swarmmover.wait(0.5)
    swarmmover.move_by_id( [0.75, 0.0, 1.5], [7], 1.5)
    swarmmover.wait(0.5)
    swarmmover.move_by_id( [1.0, 0.0, 1.5], [8], 1.5)
    swarmmover.wait(1.5)
    swarmmover.move_absolute_by_id([5.0, 9.8, 1.3], [8], 8.0)
    swarmmover.wait(0.5)
    swarmmover.move_absolute_by_id([3.2, 9.75, 1.3], [7], 8.0)
    swarmmover.wait(0.5)
    swarmmover.move_absolute_by_id([1.1, 9.8, 1.3], [6], 8.0)
    swarmmover.wait(0.5)
    swarmmover.move_absolute_by_id([-0.9, 9.8, 1.3], [5], 8.0)
    swarmmover.wait(8.5)

    swarmmover.land_by_id(1.05, [5, 6, 7, 8], 3)
    swarmmover.wait(3.5)

def group_3_home(swarmmover):
    swarmmover.takeoff_by_id(1.5, [5, 6, 7, 8], 1.5)
    swarmmover.wait(2.0)
    swarmmover.move_by_id( [0.0, 5.0, 1.3], [5, 6, 7, 8], 7.0)
    swarmmover.wait(8.0)
    swarmmover.move_by_id( [0.0, 0.0, 0.05], [5, 6, 7, 8], 9.0)
    swarmmover.wait(9.5)
    swarmmover.land_by_id(0.0, [5, 6, 7, 8], 1)
    swarmmover.wait(1.5)

def group_3(swarmmover):
    group_3_start(swarmmover)
    group_3_home(swarmmover)

def group_4(swarmmover): # 9 10 11 12 13 14 15 16
    swarmmover.takeoff_by_id(1.0, [9], 2.0)
    swarmmover.takeoff_by_id(1.0, [10], 2.0)
    swarmmover.takeoff_by_id(1.0, [11], 2.0)
    swarmmover.takeoff_by_id(1.0, [12], 2.0)
    swarmmover.takeoff_by_id(1.0, [13], 2.0)
    swarmmover.takeoff_by_id(1.0, [14], 2.0)
    swarmmover.takeoff_by_id(1.0, [15], 2.0)
    swarmmover.takeoff_by_id(1.0, [16], 2.0)
    swarmmover.wait(2.5)

    swarmmover.move_absolute_by_id([2.0, 2.0, 0.5], [9], 8.0)
    swarmmover.wait(1)
    swarmmover.move_absolute_by_id([2.0, 3.5, 0.5], [10], 8.0)
    swarmmover.wait(1)
    swarmmover.move_absolute_by_id([0.5, 2.0, 0.5], [11], 8.0)
    swarmmover.wait(1)
    swarmmover.move_absolute_by_id([0.5, 3.5, 0.5], [12], 8.0)
    swarmmover.wait(1)
    swarmmover.move_absolute_by_id([0.5, 2.0, 2.0], [13], 8.0)
    swarmmover.wait(1)
    swarmmover.move_absolute_by_id([0.5, 3.5, 2.0], [14], 8.0)
    swarmmover.wait(1)
    swarmmover.move_absolute_by_id([2.0, 2.0, 2.0], [15], 8.0)
    swarmmover.wait(1)
    swarmmover.move_absolute_by_id([2.0, 3.5, 2.0], [16], 8.0)
    swarmmover.wait(8.5)

    swarmmover.move_absolute_by_id([3.0, 2.0, 0.5], [9], 2.0)
    swarmmover.move_absolute_by_id([3.0, 3.5, 0.5], [10], 2.0)
    swarmmover.move_absolute_by_id([1.5, 2.0, 0.5], [11], 2.0)
    swarmmover.move_absolute_by_id([1.5, 3.5, 0.5], [12], 2.0)
    swarmmover.move_absolute_by_id([1.5, 2.0, 2.0], [13], 2.0)
    swarmmover.move_absolute_by_id([1.5, 3.5, 2.0], [14], 2.0)
    swarmmover.move_absolute_by_id([3.0, 2.0, 2.0], [15], 2.0)
    swarmmover.move_absolute_by_id([3.0, 3.5, 2.0], [16], 2.0)
    swarmmover.wait(3.0)
    swarmmover.move_absolute_by_id([2.0, 2.0, 0.5], [9], 8.0)
    swarmmover.move_absolute_by_id([3.0, 3.0, 0.5], [9], 2.0)
    swarmmover.move_absolute_by_id([3.0, 4.5, 0.5], [10], 2.0)
    swarmmover.move_absolute_by_id([1.5, 3.0, 0.5], [11], 2.0)
    swarmmover.move_absolute_by_id([1.5, 4.5, 0.5], [12], 2.0)
    swarmmover.move_absolute_by_id([1.5, 3.0, 2.0], [13], 2.0)
    swarmmover.move_absolute_by_id([1.5, 4.5, 2.0], [14], 2.0)
    swarmmover.move_absolute_by_id([3.0, 3.0, 2.0], [15], 2.0)
    swarmmover.move_absolute_by_id([3.0, 4.5, 2.0], [16], 2.0)
    swarmmover.wait(3.0)

    swarmmover.move_absolute_by_id([2.0, 2.0, 0.5], [9], 2.0)
    swarmmover.move_absolute_by_id([2.0, 3.5, 0.5], [10], 2.0)
    swarmmover.move_absolute_by_id([0.5, 2.0, 0.5], [11], 2.0)
    swarmmover.move_absolute_by_id([0.5, 3.5, 0.5], [12], 2.0)
    swarmmover.move_absolute_by_id([0.5, 2.0, 2.0], [13], 2.0)
    swarmmover.move_absolute_by_id([0.5, 3.5, 2.0], [14], 2.0)
    swarmmover.move_absolute_by_id([2.0, 2.0, 2.0], [15], 2.0)
    swarmmover.move_absolute_by_id([2.0, 3.5, 2.0], [16], 2.0)
    swarmmover.wait(2.5)

    swarmmover.move_by_id([0.0, 0.0, 0.3], [9, 10], 8.0)
    swarmmover.wait(1.0)
    swarmmover.move_by_id([0.0, 0.0, 0.3], [11, 12], 8.0)
    swarmmover.wait(1.0)
    swarmmover.move_by_id([0.0, 0.0, 0.3], [13, 14], 8.0)
    swarmmover.wait(1.0)
    swarmmover.move_by_id([0.0, 0.0, 0.3], [15, 16], 8.0)
    swarmmover.wait(10.0)

    swarmmover.land_by_id(0.00, [9, 10, 11, 12, 13, 14, 15, 16], 2)
    swarmmover.wait(2.5)

def choreo(swarmmover):
    group_1(swarmmover)
    group_2(swarmmover)
    group_3_start(swarmmover)
    group_4(swarmmover)
    group_3_home(swarmmover)

def move_all(swarmmover):
    swarmmover.takeoff_by_id(0.3, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 2.0)
    swarmmover.wait(2.5)
    for i in range(4):
        swarmmover.move_by_id( [2.0, 2.0, 0.3], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 8.0)
        swarmmover.wait(4.5)
        swarmmover.move_by_id( [4.0, 2.0, 0.3], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 6.0)
        swarmmover.wait(2.5)
        swarmmover.move_by_id( [4.0, 0.0, 0.3], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 4.0)
        swarmmover.wait(2.5)
        swarmmover.move_by_id( [0.0, 0.0, 0.3], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 8.0)
        swarmmover.wait(4.5)
    swarmmover.land_by_id(0.05, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 2)
    swarmmover.wait(2.5)

def testing(swarmmover):
    move_time_short = 8.0
    move_time_mid = 6.0
    move_time_long = 12.0
    start_time = 2.0
    land_time = start_time
    time_delta = 0.5
    z = 0.3
    z_land = 0.0
    drone_ids = [1, 2, 3, 4, 5]

    swarmmover.takeoff_by_id(z, drone_ids, start_time)
    swarmmover.wait(start_time + time_delta)
    print("press a key...")
    swarmmover.swarm.input.waitUntilButtonPressed()

    swarmmover.move_by_id( [8.0, 0.0, z], drone_ids, move_time_mid)
    swarmmover.wait(move_time_mid + time_delta)

    swarmmover.move_by_id( [8.0, 3.0, z], drone_ids, move_time_short)
    swarmmover.wait(move_time_short + time_delta)

    swarmmover.move_by_id( [-3.0, 3.0, z], drone_ids, move_time_long)
    swarmmover.wait(move_time_long + time_delta)

    swarmmover.move_by_id( [-3.0, 0.0, z], drone_ids, move_time_short)
    swarmmover.wait(move_time_short + time_delta)

    swarmmover.move_by_id( [0.0, 0.0, z], drone_ids, move_time_mid)
    swarmmover.wait(move_time_mid + time_delta)

    swarmmover.land_by_id(z_land, drone_ids, land_time)
    swarmmover.wait(land_time + time_delta)

def main():
    swarmmover = SwarmMover()
    # testing(swarmmover)
    # swarmmover.takeoff_by_id(0.3, [1], 2.0)
    # swarmmover.move_by_id([-6.0, 0.0, 0.3], [1], 12.0)
    # swarmmover.move_by_id([6.0, 0.0, 0.3], [1], 12.0)
    # swarmmover.land_by_id(0.05, [1], 2.0)
    # move_all(swarmmover)
    # choreo(swarmmover) # 1, 2, 3 start, 4, 3 landet
    group_1(swarmmover) # 1 komplett
    # group_2(swarmmover) #2 komplett
    # group_3(swarmmover) # 3 startet und landed
    #group_3_start(swarmmover) # 3 startet
    # group_3_home(swarmmover) # 3 landet
    #group_4(swarmmover) # 4 komplett

if __name__ == "__main__":
    main()
