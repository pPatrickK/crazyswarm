#!/usr/bin/env python

import numpy as np
from pycrazyswarm import *
import rospy
from tf import TransformListener
import time
import yaml, json
import paho.mqtt.client as paho

#defines MQTT
MQTT_BROKER = "192.168.2.9" #'192.168.2.189'
MQTT_PORT = 1883 #'1883'
MQTT_TOPIC = 'crazyflie/positions'


mPoint = [0.0, 0.0, 1.2] # middle point of spiral [x, y, z]
r = 2.5
turns = 2
circle_pos = [np.cos(np.linspace(0,2*np.pi*4,16)),np.sin(np.linspace(0,2*np.pi*4,16)), 0.0]

alpha = np.linspace(0,2*np.pi,17)

# The callback for when the client receives a CONNACK response from the server.
def on_connect_doTHIS(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("moroKopf")

# The callback for when a PUBLISH message is received from the server.
def on_message_doTHIS(client, userdata, msg):
    # print('huhu')
    # print(msg.topic+" "+str(msg.payload))
    dict = json.loads(msg.payload)
    x = dict["x"]
    y = dict["y"]
    global mPoint
    mPoint = [x,y,1.2]


if __name__ == "__main__":

    # init MQTT -------------------------------------------
    client1= paho.Client("moroKopf_subscriber")		#create client object
    #client1.on_publish = on_publish 			#assign function to callback
    client1.on_connect = on_connect_doTHIS
    client1.on_message = on_message_doTHIS
    client1.connect(MQTT_BROKER,MQTT_PORT)		#establish connection
    client1.loop_start()
    client1.subscribe('moroKopf/positions')

    # init MQTT end ---------------------------------------

    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper
    allcfs = swarm.allcfs

#start
    cf = allcfs.crazyfliesById[1]
    cf.takeoff(1,2)
    timeHelper.sleep(2.0)
    cf.goTo(mPoint, 0, 4.0)
    timeHelper.sleep(4.0)
#follow
    for k in range(60):
        start = time.time()
        print(mPoint)
        cf.goTo(mPoint,0,2)

        diff = time.time()-start
        if diff < 0.5:
            timeHelper.sleep(0.5-diff)
    timeHelper.sleep(3)
#land
    cf.goTo(cf.initialPosition+np.array([0,0,0.5]), 0, 4.0)
    timeHelper.sleep(5.0)
    # for i in range(0,n):
    #     pos = np.array(cfs[i].initialPosition) + np.array([0, 0.0, 0.4])
    #     cfs[i].goTo(pos, 0, 8.0)
    #     timeHelper.sleep(0.5)
    # timeHelper.sleep(8.0)

    allcfs.land(targetHeight=0.6, duration=2.0)
    timeHelper.sleep(5.0)
