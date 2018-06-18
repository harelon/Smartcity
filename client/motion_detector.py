import argparse
import time
import paho.mqtt.client as mqtt
from gpiozero import MotionSensor
parser = argparse.ArgumentParser(description='Start a motion detector device')
parser.add_argument('name', help='the name of the motion detector device')
parser.add_argument('port', metavar='port',type=int, nargs=1, help='GPIO port BCM')

args = parser.parse_args()

devicename = args.name
portId = args.port[0]
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    #client.subscribe("$SYS/#")
    client.subscribe("city/devices/+")
    client.publish("city/devices/"+devicename, devicename + " connected")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+ msg.payload.decode())

client = mqtt.Client(protocol=mqtt.MQTTv31)
client.on_connect = on_connect
# client.on_message = on_message

#client.connect("iot.eclipse.org", 1883, 60)
client.connect("192.168.31.200", 1883, 60)
pir=MotionSensor(portId)
# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_start()

try:
    while True:
        time.sleep(1)
        if pir.motion_detected:
            text = "Moition detected"
            client.publish("city/devices/"+devicename, text)
            
finally:
    client.loop_stop()
    client.disconnect()
