import paho.mqtt.client as mqtt

lastLightMessage=False

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    client.subscribe("+/")
    client.subscribe("city/devices/+")
    client.publish("city/devices/logic", "logic connected")

def on_message(client, userdata, msg):   
    global lastLightMessage
    print(msg.topic+" "+msg.payload.decode())
    if msg.topic=="city/devices/ldr1" and msg.payload.decode()== "lighty":
        lastLightMessage=True
    elif msg.topic=="city/devices/ldr1" and msg.payload.decode()== "darky":
        lastLightMessage=False
    if not lastLightMessage:
        if msg.topic == "city/devices/md1" and msg.payload.decode() == "Moition detected":
            client.publish("city/devices/ldr1", "on")               

client = mqtt.Client(protocol=mqtt.MQTTv31)
client.on_connect = on_connect
client.on_message = on_message
#read from a file to get the ip of the server
f = open('server/ips.txt')
ip=f.readline().rstrip()
client.connect(ip, 1883, 60)

client.loop_start()
try:
    while True:
        x=3                   
finally:
    client.loop_stop()
    client.disconnect()
