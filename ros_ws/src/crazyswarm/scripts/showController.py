#!/usr/bin/env python

import numpy as np
from pycrazyswarm import *
import pygame
import sys
import math
import time
from pycrazyswarm import *
import rospy
from tf import TransformListener
import yaml, json
import paho.mqtt.client as paho

#defines MQTT
MQTT_BROKER = "192.168.2.9" #'192.168.2.189'
MQTT_PORT = 1883 #'1883'
MQTT_TOPIC = 'crazyflie/positions'


mPoint = [0.0, 0.0, 0.0] # middle point of spiral [x, y, z]
r_a = 2.0
r_s = 1.5
turns = 2

swarm = Crazyswarm()
timeHelper = swarm.timeHelper
allcfs = swarm.allcfs

# constants
ALTITUDE = 2.5
XMIN = -4.5
YMIN = -3.5
XMAX = 7.5
YMAX = 5
DISTANCE = 2# distance between 2 drones
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
    mPoint = [x,y,0.0]

def droneRect(flytime):
    iteration = 0
    for cf in cfs:
        if iteration < 4:
            pos = np.array([XMAX, (YMAX+YMIN)/2+(-1.5+iteration%4)*DISTANCE, ALTITUDE])
        elif iteration < 8:
            pos = np.array([(XMAX+XMIN)/2+(1.5-iteration%4)*DISTANCE, YMIN, ALTITUDE])
        elif iteration < 12:
            pos = np.array([(XMAX+XMIN)/2+(1.5-iteration%4)*DISTANCE, YMAX, ALTITUDE])
        elif iteration < 16:
            pos = np.array([XMIN, (YMAX+YMIN)/2+(-1.5+iteration%4)*DISTANCE, ALTITUDE])
        iteration +=1
        print("position of cf:" + str(iteration)+" = "+ str(pos))
        cf.goTo(pos, 0, flytime)
    timeHelper.sleep(flytime + 1.0)

def droneSpiral():
# fly in cricle
    #singe spiral
    # k = 0
    # for i in [2,3,8,9,10,11,15,14,13,12,7,6,5,4,0,1]:
    #     cpos = mPoint + np.array([r_s*np.cos(alpha[k]), r_s*np.sin(alpha[k]), 0.8+k*0.1])
    #     cfs[i].goTo(cpos, 0, 6.0)
    #     k = k + 1
    #     timeHelper.sleep(0.5)
    # timeHelper.sleep(8.0)
    # double spiral
    # [2,3,8,9,10,11,15,14,13,12,7,6,5,4,0,1]
    # [2,  8,  10,   15,   13,   7,  5,  0, ]
    # [  3,  9,   11,   14,   12,  6,  4,  1] -> [12,  6,  4,  1,  3,  9,   11,   14]
    #                                            [1.0,1.2,1.4,1.6, 1.8,2.0,2.2,2.4]
    height1 = [1.0,1.2,1.4,1.6,  1.8,2.0,2.2,2.4]
    height2 = [ 1.8,2.0,2.2,2.4, 1.0,1.2,1.4,1.6]
    k = 0
    k1 = 0
    k2 = 0
    for i in [2,3,8,9,10,11,15,14,13,12,7,6,5,4,0,1]:
        if i in [2,  8,  10,   15,   13,   7,  5,  0]:
            cpos = mPoint + np.array([r_s*np.cos(alpha[k]), r_s*np.sin(alpha[k]), height1[k1]])
            k1 = k1 + 1
        else:
            cpos = mPoint + np.array([r_s*np.cos(alpha[k]), r_s*np.sin(alpha[k]), height2[k2]])
            k2 = k2 + 1
        k = k+1
        cfs[i].goTo(cpos, 0, 6.0)
        timeHelper.sleep(0.5)
    timeHelper.sleep(8.0)
# loop
    #SINGLE
    # for beta in np.linspace(0,2*np.pi*turns,15*turns):
    #     start = time.time()
    #     k = 0
    #     for i in [2,3,8,9,10,11,15,14,13,12,7,6,5,4,0,1]:
    #         cpos = mPoint + np.array([r_s*np.cos(alpha[k]+beta), r_s*np.sin(alpha[k]+beta), 0.8+k*0.1])
    #         cfs[i].goTo(cpos, 0, 2.0)
    #         k = k+1
    #     diff = time.time()-start
    #     print(time.time()-start)
    #     if diff < 0.5:
    #         timeHelper.sleep(0.5-diff)
    #DOUBLE
    height1 = [1.0,1.2,1.4,1.6,  1.8,2.0,2.2,2.4]
    height2 = [ 1.8,2.0,2.2,2.4, 1.0,1.2,1.4,1.6]
    for beta in np.linspace(0,2*np.pi*turns,15*turns):
        start = time.time()
        k1 = 0
        k2 = 0
        k = 0
        for i in [2,3,8,9,10,11,15,14,13,12,7,6,5,4,0,1]:
            if i in [2,  8,  10,   15,   13,   7,  5,  0]:
                cpos = mPoint + np.array([r_s*np.cos(alpha[k]+beta), r_s*np.sin(alpha[k]+beta), height1[k1]])
                k1 = k1 + 1
            else:
                cpos = mPoint + np.array([r_s*np.cos(alpha[k]+beta), r_s*np.sin(alpha[k]+beta), height2[k2]])
                k2 = k2 + 1
            cfs[i].goTo(cpos, 0, 2.0)
            k = k+1
        diff = time.time()-start
        print(time.time()-start)
        if diff < 0.5:
            timeHelper.sleep(0.5-diff)
    timeHelper.sleep(3.0)

def droneAtomium():
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

# def droneCirclePhoto():
# # fly in circle
#     k = 0
#     for i in [2,3,8,9,10,11,15,14,13,12,7,6,5,4,0,1]:
#         x = r_s*np.cos(alpha[k])
#         y = r_s*np.sin(alpha[k])
#         if i in [2,8,10,15,13,7,5,0]:
#             z = x/1 + 1.7
#         else:
#             z = x/1 + 1.7
#         cpos = mPoint + np.array([x,y,z])
#         cfs[i].goTo(cpos, 0, 6.0)
#         k = k + 1
#         # timeHelper.sleep(0.5)
#     #timeHelper.sleep(6.0)
#
# def bringCf32():
# # fly in circle
#     cf32.takeoff(targetHeight=1.4, duration=3.0)
#     timeHelper.sleep(3.5)
#     cf32.goTo(np.array([2.5,0.0,1.4]), 0, 4.0)
#     timeHelper.sleep(4.0)
#
# def landCf32():
# # fly in circle
#     cf32.goTo(cf32.initialPosition + np.array([0.0,0.0,1.4]), 0, 4.0)
#     timeHelper.sleep(6.0)
#     cf32.land(targetHeight=0.0, duration=3.0)

def droneHome(flytime):
    for cf in cfs:
        pos = np.array(cf.initialPosition) + np.array([0, 0.0, 0.4])
        cf.goTo(pos, 0, flytime)
    timeHelper.sleep(flytime+1.0)

def droneTakeoff():
    for cf in cfs:
        cf.takeoff(targetHeight=1.0, duration=2.0)
    timeHelper.sleep(2.0)

def droneLand():
    allcfs.land(targetHeight=0.6, duration=4.0)
    timeHelper.sleep(5.0)

def format_decimal(number):
    return '{0:.2f}'.format(number)

# init MQTT -------------------------------------------
client1= paho.Client("moroKopf_subscriber")		#create client object
#client1.on_publish = on_publish 			#assign function to callback
client1.on_connect = on_connect_doTHIS
client1.on_message = on_message_doTHIS
client1.connect(MQTT_BROKER,MQTT_PORT)		#establish connection
client1.loop_start()
client1.subscribe('moroKopf/positions')

# init MQTT end ---------------------------------------

def main():
    # define und init shit

    # window shit
    pygame.init()
    pygame.font.init()
    font = pygame.font.SysFont("ubuntumono", 30)
    window_size = 800, 600
    screen = pygame.display.set_mode(window_size)
    fill_color = 0, 0, 0
    running = True
    # display key instructions
    text_surface = font.render("s = takeoff and go to rectangle", False, (250, 250, 250))
    screen.blit(text_surface, (10, 10))
    text_surface = font.render("l = go home, sin, and land", False, (250, 250, 250))
    screen.blit(text_surface, (10, 40))
    text_surface = font.render("1 = spiral around moritz", False, (250, 250, 250))
    screen.blit(text_surface, (10, 70))
    text_surface = font.render("2 = tube around moritz", False, (250, 250, 250))
    screen.blit(text_surface, (10, 100))
    text_surface = font.render("3 = atomium", False, (250, 250, 250))
    screen.blit(text_surface, (10, 130))
    # text_surface = font.render("4 = place for photoshooting (with cf32)", False, (250, 250, 250))
    # screen.blit(text_surface, (10, 160))
    # text_surface = font.render("5 = back to rect (land cf32)", False, (250, 250, 250))
    # screen.blit(text_surface, (10, 190))
    pygame.display.flip()

    # start loop
    while running:
        # do scripted shit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                continue
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    continue
                elif event.key == pygame.K_s:
                    # takeoff and go to rectangle
                    droneTakeoff()
                    droneRect(12.0)
                elif event.key == pygame.K_l:
                    # go home, sin, and land
                    droneHome(12.0)
                    droneLand()
                elif event.key == pygame.K_1:
                    # spiral around moritz
                    droneSpiral()
                    droneRect(8.0)
                    #allcfs.land(targetHeight=0.6, duration=4.0)
                elif event.key == pygame.K_2:
                    # tube around moritz
                    droneSpiral()
                    droneRect(8.0)
                elif event.key == pygame.K_3:
                    # atomium
                    droneAtomium()
                    droneRect(8.0)
                # elif event.key == pygame.K_4:
                #     # place for photoshooting
                #     droneCirclePhoto()
                #     bringCf32()
                #
                # elif event.key == pygame.K_5:
                #     # back to rect
                #     landCf32()
                #     droneRect(8.0)

        # display info
        # screen.fill(fill_color)
        # text_surface = font.render("time for starting:" + format_decimal(cfs.start_time), False, (250, 250, 250))
        # screen.blit(text_surface, (10, 10))
        # text_surface = font.render("time for landing:" + format_decimal(cfs.land_time), False, (250, 250, 250))
        # screen.blit(text_surface, (10, 45))
        # text_surface = font.render("time for moving:" + format_decimal(cfs.movement_time), False, (250, 250, 250))
        # screen.blit(text_surface, (10, 80))
        # text_surface = font.render("amount of moving:" + format_decimal(cfs.movement_amount), False, (250, 250, 250))
        # screen.blit(text_surface, (10, 115))
        # text_surface = font.render("height:" + format_decimal(cfs.height), False, (250, 250, 250))
        # screen.blit(text_surface, (10, 150))
        # pygame.display.flip()
    # end loop
    pygame.quit()

if __name__ == "__main__":
    main()
    #TEST
    # droneTakeoff()
    # droneRect(12.0)
    # droneCirclePhoto()
    # bringCf32()
    # landCf32()
    # droneRect(12.0)
    # droneHome(12.0)
    # droneLand()
    # droneSpiral()
    # droneRect(8.0)
    # droneAtomium()
    # droneRect(8.0)
    # droneHome(12.0)
    # droneLand()
