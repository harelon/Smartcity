import paho.mqtt.client as mqtt

lastLightMessage=False

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
        
    client.subscribe("city/devices/#")
    client.publish("city/devices/logic", "logic connected")

def on_message(client, userdata, msg):   
    global lastLightMessage
    print(msg.topic+" "+msg.payload.decode())
    if msg.topic=="city/devices/ldr" and msg.payload.decode()== "lighty":
        lastLightMessage=True
    elif msg.topic=="city/devices/ldr" and msg.payload.decode()== "darky":
        lastLightMessage=False
    if not lastLightMessage:
        if msg.topic == "city/devices/mds/+" and msg.payload.decode() == "Moition detected":
            topicsplit=msg.topic.split("/")
            id=int(topicsplit[len(topicsplit)-1])
            client.publish("city/devices/lb/"+id, "on")               

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
        pass                          
finally:
    client.loop_stop()
    client.disconnect()
