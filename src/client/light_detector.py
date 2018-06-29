import paho.mqtt.client as mqtt
from apds9960.const import *
from apds9960 import APDS9960
import RPi.GPIO as GPIO
import smbus
from time import sleep
from siteConfig import SiteConfig

siteConfig = SiteConfig()

# port = 1
# bus = smbus.SMBus(port)

# apds = APDS9960(bus)



# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("city/devices/ldr")
    client.publish("city/devices/ldr", "ldr connected")

client = mqtt.Client(protocol=mqtt.MQTTv31)
client.on_connect = on_connect
#read from a file to get the ip of the server
client.connect(siteConfig.ServerIp, 1883, 60)
# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_start()
try:        
    # apds.enableLightSensor()
    # oval = -1
    while True:
        # sleep(1)
        # val = apds.readAmbientLight()
        # if not val == oval:
        #     if val>100:
        #         client.publish("city/devices/ldr","lighty")
        #     else:
        #         client.publish("city/devices/ldr","darky")           
        #     oval = val
        sleep(1)
        client.publish("city/devices/ldr","darky") 
        print("no light detected")
finally:
    client.loop_stop()
    GPIO.cleanup()
    client.disconnect()