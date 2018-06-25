import paho.mqtt.client as mqtt
from apds9960.const import *
from apds9960 import APDS9960
import RPi.GPIO as GPIO
import smbus
from time import sleep
GPIO.cleanup()
port = 1
bus = smbus.SMBus(port)

apds = APDS9960(bus)



# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    #client.subscribe("$SYS/#")
    client.subscribe("city/devices/ldr1")
    client.publish("city/devices/ldr1", "ldr1 connected")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):   
     print(msg.topic+" "+msg.payload.decode())

client = mqtt.Client(protocol=mqtt.MQTTv31)
client.on_connect = on_connect
# client.on_message = on_message
#client.connect("iot.eclipse.org", 1883, 60)
client.connect("192.168.31.105", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_start()

try:    
        #text = input("")        
        #client.publish("city/devices/"+devicename, text)       
    # Interrupt-Event hinzufuegen, steigende Flanke    
    apds.enableLightSensor()
    oval = -1
    while True:
        sleep(0.1)
        val = apds.readAmbientLight()
        if val != oval:
            if val>100:
                client.publish("city/devices/ldr1","lighty")
            else:
                client.publish("city/devices/ldr1","darky")
            # print("AmbientLight={}".format(val))            
            oval = val            
finally:
    client.loop_stop()
    client.disconnect()
