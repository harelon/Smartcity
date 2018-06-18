import argparse
import time
import paho.mqtt.client as mqtt

parser = argparse.ArgumentParser(description='Start a light bulb device')
parser.add_argument('name', help='the name of the light bulb device')
parser.add_argument('port', metavar='port',type=int, nargs=1, help='GPIO port BCM')

args = parser.parse_args()

devicename = args.name
portId = args.port

light_timeout = 10

is_light_turned_on = False
turn_on_time = time.time()

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    #client.subscribe("$SYS/#")
    client.subscribe("city/devices/" + devicename)
    client.publish("city/devices/"+devicename, devicename + " connected")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global is_light_turned_on
    global turn_on_time
    print(msg.topic+" "+msg.payload.decode())
    if msg.topic == "city/devices/" + devicename and msg.payload.decode() == "on":
        is_light_turned_on = True
        client.publish("cmnd/sonoff/power", "1") 
        turn_on_time = time.time()
        print("Turning light on")

client = mqtt.Client(protocol=mqtt.MQTTv31)
client.on_connect = on_connect
client.on_message = on_message
led=LED(portId)
#client.connect("iot.eclipse.org", 1883, 60)
client.connect("192.168.31.200", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_start()

try:
    while True:
        #text = input("")        
        #client.publish("city/devices/"+devicename, text)

        if is_light_turned_on:
            now = time.time()
            if now - turn_on_time > light_timeout:
                is_light_turned_on = False
                turn_on_time = None
                print("Turning light off")
                client.publish("cmnd/sonoff/power", "0")

        print("Light is " + ("on" if is_light_turned_on else "off"))
        time.sleep(1)
        #if text == "q":
        #    break
finally:
    client.loop_stop()
    client.disconnect()
