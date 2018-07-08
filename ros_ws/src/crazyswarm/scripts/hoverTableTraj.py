import numpy as np
from pycrazyswarm import *
import uav_trajectory
import datetime
import os
from subprocess import call
import auto_yaw_trajectory as auto_yaw

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

    def run_trajectory_generation_tool(self, input_filename, output_filename, path_to_generator, amax, vmax):
        command = path_to_generator + "/genTrajectory"
        call([command, "-i", input_filename, "--v_max", str(vmax), "--a_max", str(amax), "-o", output_filename])

    def generate_trajectory(self, fname, amax = 1.0, vmax = 1.0):
        folder_basename = os.path.dirname(os.path.abspath(__file__)) + "/trajectories/"
        # waypoint_csv = folder_basename + ".csv"
        trajectory_csv = folder_basename + fname
        fname = os.path.dirname(os.path.abspath(__file__)) + "/" + fname
        # with open(waypoint_csv, "w+") as waypoint_csv_file:
        #     for waypoint in waypoints:
        #         waypoint_csv_file.write(','.join(str(coordinate) for coordinate in waypoint) + "\n")
        self.run_trajectory_generation_tool(fname, trajectory_csv, "../../../../../../uav_trajectories/build", amax, vmax)
        return trajectory_csv

def group_1(swarmmover): # 1 2 3 4
    z_start = 0.2
    start_time = 1.0
    z_land = 0.0
    land_time = 1.0
    z_movement = 0.15
    # --------------------------------------------------------------------------
    # os.remove(output_filename)
    amax = 1.4
    vmax = 3.0
    timescale1 = 0.50#0.55
    timescale2 = 0.52#0.55
    trajectory_csv = swarmmover.generate_trajectory("race_one.csv", amax, vmax)
    trajectory_csv2 = swarmmover.generate_trajectory("race_two.csv", amax, vmax)
    # trajectory_csv = "trajectories/firstTraj_autoyaw.csv"

    traj1 = uav_trajectory.Trajectory()
    traj2 = uav_trajectory.Trajectory()
    traj1.loadcsv(trajectory_csv)
    traj2.loadcsv(trajectory_csv2)
    # cf1 = allcfs.crazyflies[0]
    # cf1.setGroupMask(0b00000001) # 8 bits setzen, und wenn nur ein bit der cf mit der maske stimmt dann fliegt die
    # cf2 = allcfs.crazyflies[1]
    # cf2.setGroupMask(0b00000010)
    # allcfs.startTrajectory(0, timescale=TIMESCALE, groupMask=0b00000001)
    cf1 = swarmmover.allcfs.crazyfliesById[6]
    cf2 = swarmmover.allcfs.crazyfliesById[18]

    # for cf in swarmmover.allcfs.crazyflies:
        # cf.uploadTrajectory(0, 0, traj1) # req.trajectoryId, req.pieceOffset, pieces

    cf1.setGroupMask(0b00000001)
    cf2.setGroupMask(0b00000010)
    cf1.uploadTrajectory(0, 0, traj1)
    cf2.uploadTrajectory(0, 0, traj2)
    #allcfs.startTrajectory(0, timescale=TIMESCALE, groupMask=0b00000001)
    ## -------------------------------------------------------------------------
    swarmmover.takeoff_by_id(z_start, [6,18,25,26], start_time)
    swarmmover.wait(start_time + 0.5)


    swarmmover.move_absolute_by_id( [0.0, 0.0, z_movement], [6], 6.0)
    swarmmover.move_absolute_by_id( [-0.3, -0.3, z_movement], [18], 6.0)

    # swarmmover.move_absolute_by_id( [-0.4, 0.0, z_movement], [25], 4.0)
    # swarmmover.wait(0.5)
    # swarmmover.move_absolute_by_id( [-0.6,-0.5, z_movement], [26], 4.0)
    swarmmover.wait(6.5)

    swarmmover.allcfs.startTrajectory(0, timescale1, groupMask=0b00000001)
    swarmmover.allcfs.startTrajectory(0, timescale2, groupMask=0b00000010)
    swarmmover.wait(traj1.duration * timescale2 + 0.5)
    #---------------------------------------------------------------------------
    swarmmover.land_by_id(0.00, [6,18,25,26], 0.6)
    swarmmover.wait(0.65)
    swarmmover.takeoff_by_id(0.04, [6,18,25,26], 0.2)
    swarmmover.wait(0.25)
    swarmmover.land_by_id(0.00, [6,18,25,26], 0.1)
    swarmmover.wait(0.15)
    swarmmover.takeoff_by_id(0.04, [6,18,25,26], 0.2)
    swarmmover.wait(0.25)
    swarmmover.land_by_id(0.00, [6,18,25,26], 0.1)
    swarmmover.wait(0.15)
    swarmmover.takeoff_by_id(0.04, [6,18,25,26], 0.2)
    swarmmover.wait(0.25)
    swarmmover.land_by_id(0.00, [6,18,25,26], 0.1)
    swarmmover.wait(0.15)
    #---------------------------------------------------------------------------
    # swarmmover.wait(10.5)
    swarmmover.takeoff_by_id(0.03, [6,18,25,26], 1)
    swarmmover.wait(1.5)
    swarmmover.move_by_id( [0.0, 0.0, z_movement], [6,18,25,26], 3.0)
    swarmmover.wait(3.5)
    swarmmover.land_by_id(z_land, [6,18,25,26], land_time)
    swarmmover.wait(land_time + 0.5)

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
