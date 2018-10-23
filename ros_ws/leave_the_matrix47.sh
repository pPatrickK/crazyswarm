#!/bin/bash
echo Test start
#-----------------------------------Gruppe 4------------------------------------

mosquitto_pub -h gopher.phynetlab.com -p 8883 -m '{"id":2, "data": [0.0, 9.0] }' -t crazyflie/movehome
mosquitto_pub -h gopher.phynetlab.com -p 8883 -m '{"id":4, "data": [0.0, 9.0] }' -t crazyflie/movehome
mosquitto_pub -h gopher.phynetlab.com -p 8883 -m '{"id":6, "data": [0.0, 9.0] }' -t crazyflie/movehome
mosquitto_pub -h gopher.phynetlab.com -p 8883 -m '{"id":8, "data": [0.0, 9.0] }' -t crazyflie/movehome
mosquitto_pub -h gopher.phynetlab.com -p 8883 -m '{"id":10, "data": [0.0, 9.0] }' -t crazyflie/movehome
mosquitto_pub -h gopher.phynetlab.com -p 8883 -m '{"id":12, "data": [0.0, 9.0] }' -t crazyflie/movehome
mosquitto_pub -h gopher.phynetlab.com -p 8883 -m '{"id":14, "data": [0.0, 9.0] }' -t crazyflie/movehome


mosquitto_pub -h gopher.phynetlab.com -p 8883 -m '{"id":2, "data":[9.0, 1.8, 0.4]}' -t crazyflie/landwithheight
mosquitto_pub -h gopher.phynetlab.com -p 8883 -m '{"id":4, "data":[9.0, 1.8, 0.4]}' -t crazyflie/landwithheight
mosquitto_pub -h gopher.phynetlab.com -p 8883 -m '{"id":6, "data":[9.0, 1.8, 0.4]}' -t crazyflie/landwithheight
mosquitto_pub -h gopher.phynetlab.com -p 8883 -m '{"id":8, "data":[9.0, 1.8, 0.4]}' -t crazyflie/landwithheight
mosquitto_pub -h gopher.phynetlab.com -p 8883 -m '{"id":10, "data":[9.0, 1.8, 0.4]}' -t crazyflie/landwithheight
mosquitto_pub -h gopher.phynetlab.com -p 8883 -m '{"id":12, "data":[9.0, 1.8, 0.4]}' -t crazyflie/landwithheight
mosquitto_pub -h gopher.phynetlab.com -p 8883 -m '{"id":14, "data":[9.0, 1.8, 0.4]}' -t crazyflie/landwithheight

#-----------------------------------Gruppe 3------------------------------------

mosquitto_pub -h gopher.phynetlab.com -p 8883 -m '{"id":1, "data": [11.0, 9.0] }' -t crazyflie/movehome
mosquitto_pub -h gopher.phynetlab.com -p 8883 -m '{"id":3, "data": [11.0, 9.0] }' -t crazyflie/movehome
mosquitto_pub -h gopher.phynetlab.com -p 8883 -m '{"id":5, "data": [11.0, 9.0] }' -t crazyflie/movehome
mosquitto_pub -h gopher.phynetlab.com -p 8883 -m '{"id":7, "data": [11.0, 9.0] }' -t crazyflie/movehome
mosquitto_pub -h gopher.phynetlab.com -p 8883 -m '{"id":9, "data": [11.0, 9.0] }' -t crazyflie/movehome
mosquitto_pub -h gopher.phynetlab.com -p 8883 -m '{"id":11, "data": [11.0, 9.0] }' -t crazyflie/movehome
mosquitto_pub -h gopher.phynetlab.com -p 8883 -m '{"id":13, "data": [11.0, 9.0] }' -t crazyflie/movehome


mosquitto_pub -h gopher.phynetlab.com -p 8883 -m '{"id":1, "data":[20.0, 1.8, 0.4]}' -t crazyflie/landwithheight
mosquitto_pub -h gopher.phynetlab.com -p 8883 -m '{"id":3, "data":[20.0, 1.8, 0.4]}' -t crazyflie/landwithheight
mosquitto_pub -h gopher.phynetlab.com -p 8883 -m '{"id":5, "data":[20.0, 1.8, 0.4]}' -t crazyflie/landwithheight
mosquitto_pub -h gopher.phynetlab.com -p 8883 -m '{"id":7, "data":[20.0, 1.8, 0.4]}' -t crazyflie/landwithheight
mosquitto_pub -h gopher.phynetlab.com -p 8883 -m '{"id":9, "data":[20.0, 1.8, 0.4]}' -t crazyflie/landwithheight
mosquitto_pub -h gopher.phynetlab.com -p 8883 -m '{"id":11, "data":[20.0, 1.8, 0.4]}' -t crazyflie/landwithheight
mosquitto_pub -h gopher.phynetlab.com -p 8883 -m '{"id":13, "data":[20.0, 1.8, 0.4]}' -t crazyflie/landwithheight

#-----------------------------------Gruppe 2------------------------------------

mosquitto_pub -h gopher.phynetlab.com -p 8883 -m '{"id":16, "data": [22.0, 9.0] }' -t crazyflie/movehome
mosquitto_pub -h gopher.phynetlab.com -p 8883 -m '{"id":18, "data": [22.0, 9.0] }' -t crazyflie/movehome
mosquitto_pub -h gopher.phynetlab.com -p 8883 -m '{"id":20, "data": [22.0, 9.0] }' -t crazyflie/movehome
mosquitto_pub -h gopher.phynetlab.com -p 8883 -m '{"id":22, "data": [22.0, 9.0] }' -t crazyflie/movehome
mosquitto_pub -h gopher.phynetlab.com -p 8883 -m '{"id":24, "data": [22.0, 9.0] }' -t crazyflie/movehome
mosquitto_pub -h gopher.phynetlab.com -p 8883 -m '{"id":26, "data": [22.0, 9.0] }' -t crazyflie/movehome
mosquitto_pub -h gopher.phynetlab.com -p 8883 -m '{"id":28, "data": [22.0, 9.0] }' -t crazyflie/movehome


mosquitto_pub -h gopher.phynetlab.com -p 8883 -m '{"id":16, "data":[31.0, 1.8, 0.4]}' -t crazyflie/landwithheight
mosquitto_pub -h gopher.phynetlab.com -p 8883 -m '{"id":18, "data":[31.0, 1.8, 0.4]}' -t crazyflie/landwithheight
mosquitto_pub -h gopher.phynetlab.com -p 8883 -m '{"id":20, "data":[31.0, 1.8, 0.4]}' -t crazyflie/landwithheight
mosquitto_pub -h gopher.phynetlab.com -p 8883 -m '{"id":22, "data":[31.0, 1.8, 0.4]}' -t crazyflie/landwithheight
mosquitto_pub -h gopher.phynetlab.com -p 8883 -m '{"id":24, "data":[31.0, 1.8, 0.4]}' -t crazyflie/landwithheight
mosquitto_pub -h gopher.phynetlab.com -p 8883 -m '{"id":26, "data":[31.0, 1.8, 0.4]}' -t crazyflie/landwithheight
mosquitto_pub -h gopher.phynetlab.com -p 8883 -m '{"id":28, "data":[31.0, 1.8, 0.4]}' -t crazyflie/landwithheight


#-----------------------------------Gruppe 1------------------------------------

mosquitto_pub -h gopher.phynetlab.com -p 8883 -m '{"id":15, "data": [33.0, 9.0] }' -t crazyflie/movehome
mosquitto_pub -h gopher.phynetlab.com -p 8883 -m '{"id":17, "data": [33.0, 9.0] }' -t crazyflie/movehome
mosquitto_pub -h gopher.phynetlab.com -p 8883 -m '{"id":19, "data": [33.0, 9.0] }' -t crazyflie/movehome
mosquitto_pub -h gopher.phynetlab.com -p 8883 -m '{"id":21, "data": [33.0, 9.0] }' -t crazyflie/movehome
mosquitto_pub -h gopher.phynetlab.com -p 8883 -m '{"id":23, "data": [33.0, 9.0] }' -t crazyflie/movehome
mosquitto_pub -h gopher.phynetlab.com -p 8883 -m '{"id":25, "data": [33.0, 9.0] }' -t crazyflie/movehome
mosquitto_pub -h gopher.phynetlab.com -p 8883 -m '{"id":29, "data": [33.0, 9.0] }' -t crazyflie/movehome


mosquitto_pub -h gopher.phynetlab.com -p 8883 -m '{"id":15, "data":[42.0, 1.8, 0.4]}' -t crazyflie/landwithheight
mosquitto_pub -h gopher.phynetlab.com -p 8883 -m '{"id":17, "data":[42.0, 1.8, 0.4]}' -t crazyflie/landwithheight
mosquitto_pub -h gopher.phynetlab.com -p 8883 -m '{"id":19, "data":[42.0, 1.8, 0.4]}' -t crazyflie/landwithheight
mosquitto_pub -h gopher.phynetlab.com -p 8883 -m '{"id":21, "data":[42.0, 1.8, 0.4]}' -t crazyflie/landwithheight
mosquitto_pub -h gopher.phynetlab.com -p 8883 -m '{"id":23, "data":[42.0, 1.8, 0.4]}' -t crazyflie/landwithheight
mosquitto_pub -h gopher.phynetlab.com -p 8883 -m '{"id":25, "data":[42.0, 1.8, 0.4]}' -t crazyflie/landwithheight
mosquitto_pub -h gopher.phynetlab.com -p 8883 -m '{"id":29, "data":[42.0, 1.8, 0.4]}' -t crazyflie/landwithheight
