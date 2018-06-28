#!/usr/bin/env python
# this on patricks computer
# ros python lib
import rospy

# for parsing ros msgs to python structs
import yaml, json

# beautiful debug msgs
from pprint import pprint

# specific msg type of the positions
from tf2_msgs.msg import TFMessage

#mqtt imports
import paho.mqtt.client as paho

#defines
TF_TOPIC = 'tf'
MQTT_BROKER = '192.168.2.189'
MQTT_PORT = '1883'
MQTT_TOPIC = 'test1'

#prototype test
PROTOTYPE_TEST = False
PROTOTYPE = {
	"header": {
		"stamp": {"secs": 1527075825, "nsecs": 446688634}, 
		"frame_id": "world", "seq": 0
		},
	"transform": {
		"translation": {"y": -0.730628550053, "x": 1.22334706783, "z": 0.0395280644298}, 
		"rotation": {"y": -0.0111685172939, "x": 0.00285034257295, "z": -0.844045171385, "w": 0.536148196332}
		}, 
	"child_frame_id": "cf2"
}

def send_msg_once():
	data_as_json = json.dumps(PROTOTYPE)
	publish_mqtt(data_as_json)								#data is sent as a json string
	
def on_publish():
	print('published')

def publish_mqtt(data_as_json):
	ret= client1.publish(MQTT_TOPIC,(data_as_json))				#publish

def parse_callback(data):
	y = yaml.load(str(data.transforms[0]))
	data_as_json = json.dumps(y)
	publish_mqtt(data_as_json)								#data is sent as a json string

def mqtt_tf_publisher():
	rospy.init_node('mqtt_tf_publisher', anonymous=False)
	rospy.Subscriber(TF_TOPIC, TFMessage, parse_callback)
	rospy.spin()

if __name__ == '__main__':
	#mqtt init stuff
	client1= paho.Client("tf_publisher")		#create client object
	#client1.on_publish = on_publish 			#assign function to callback
	client1.connect(MQTT_BROKER,MQTT_PORT)		#establish connection
	#ros subscribe node
	if PROTOTYPE_TEST:
		send_msg_once()
	else:	
		mqtt_tf_publisher()
    
