import argparse
import time
import paho.mqtt.client as mqtt

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
    client.publish(topic="cmnd/"+devicename+"/status",payload=None)
   

def on_message(client, userdata, msg):
    global is_light_turned_on
    global turn_on_time
    print(msg.topic+" "+msg.payload.decode())
    if msg.topic == "city/devices/" + devicename and msg.payload.decode() == "on":
        is_light_turned_on = True
        client.publish("cmnd/"+devicename+"/power", "1") 
        turn_on_time = time.time()
        print("Turning light on")
    if msg.topic == "stat/"+devicename+"/STATUS":
        client.unsubscribe("stat/"+devicename+"/STATUS")
        list=msg.payload.decode().split(",")
        for section in list:
            if "Power\"" in section:
                print("succeeded")
                list2=section.split(":")                
                if list2[1]=="0":
                    is_light_turned_on=False
                else:                    
                    is_light_turned_on=True
    
client = mqtt.Client(protocol=mqtt.MQTTv31)
client.on_connect = on_connect
client.on_message = on_message
#read from a file to get the ip of the server
with open('/home/pi/server/ips.txt') as f:
    ip = f.readline().rstrip()
    client.connect(ip, 1883, 60)

client.loop_start()
try:
    while True:    
        if is_light_turned_on:
            now = time.time()
            if now - turn_on_time > light_timeout:
                is_light_turned_on = False
                turn_on_time = None
                print("Turning light off")
                client.publish("cmnd/"+devicename+"/power", "0")

        print("Light is " + ("on" if is_light_turned_on else "off"))                
finally:
    client.loop_stop()
    client.disconnect()
