import subprocess
import yaml
import time
import pprint

cfs_number = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,29,28]

with open("ros_ws/src/crazyswarm/launch/crazyflies.yaml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

for number in cfs_number:
    for cf in range(len(cfg["crazyflies"])):
        if(cfg["crazyflies"][cf]['id'] == number):
            id = "{0:02X}".format(number)
            uri = "radio://0/{}/250K/E7E7E7E7{}".format(cfg["crazyflies"][cf]["channel"], id)
            print(number)
            subprocess.call(["rosrun crazyflie_tools reboot --uri " + uri], shell=True)
            time.sleep(1)
