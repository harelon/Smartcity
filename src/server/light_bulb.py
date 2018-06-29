import argparse
import time
import paho.mqtt.client as mqtt
from siteConfig import SiteConfig
import json

siteConfig = SiteConfig()

parser = argparse.ArgumentParser(description='Start a light bulb device')
parser.add_argument('name', help='the name of the light bulb device')

args = parser.parse_args()

devicename = args.name

light_timeout = 10

is_light_turned_on = None
turn_on_time = time.time()


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    client.subscribe("city/devices/lb/" + devicename)
    client.subscribe("stat/" + devicename+"/power")
    client.publish("city/devices/lb/"+devicename, devicename + " connected")
    client.subscribe("stat/"+devicename+"/STATUS")
    client.subscribe("stat/"+devicename+"/POWER")
    client.publish(topic="cmnd/"+devicename+"/status",payload=None)        
   
def on_message(client, userdata, msg):
    global is_light_turned_on
    global turn_on_time
    print(msg.topic+" "+msg.payload.decode())
    if msg.topic == "city/devices/" + devicename and msg.payload.decode() == "on":        
        client.publish("cmnd/"+devicename+"/power", "1")         
        print("Turning light on")
    if msg.topic == "stat/"+devicename+"/STATUS":
        client.unsubscribe("stat/"+devicename+"/STATUS")
        data=json.loads(msg.payload.decode())
        PowerMode=data["Status"]["Power"]                            
        if PowerMode=="0":
            is_light_turned_on=False
        elif PowerMode=="1":                    
            is_light_turned_on=True
        else:
            is_light_turned_on=None
    if msg.topic == "stat/"+devicename+"/POWER":
        PowerMode=msg.payload.decode()
        if PowerMode=="OFF":
            is_light_turned_on=False
            turn_on_time = None
        elif PowerMode=="ON":
            turn_on_time = time.time()
            is_light_turned_on=True           
                       

client = mqtt.Client(protocol=mqtt.MQTTv31)
client.on_connect = on_connect
client.on_message = on_message

client.connect(siteConfig.ServerIp, 1883, 60)

client.loop_start()
try:
    while True:          
        if is_light_turned_on:
            now = time.time()
            if now - turn_on_time > light_timeout:
                print("Turning light off")
                client.publish("cmnd/"+devicename+"/power", "0")

        print("Light is " + ("on" if is_light_turned_on else "off"))
finally:
    client.loop_stop()
    client.disconnect()
