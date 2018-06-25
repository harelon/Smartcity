import paho.mqtt.client as mqtt

lastLightMessage=False

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("+/")
    client.subscribe("city/devices/+")
    client.publish("city/devices/logic", "logic connected")

# The callback for when a PUBLISH message is received from the server.
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

    # if msg.topic == "city/devices/md2" and msg.payload.decode() == "motion":
    #     client.publish("city/devices/lb1", "on")
    #     client.publish("city/devices/lb2", "on")

client = mqtt.Client(protocol=mqtt.MQTTv31)
client.on_connect = on_connect
client.on_message = on_message
#client.connect("iot.eclipse.org", 1883, 60)
client.connect("192.168.31.105", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_start()
try:
    while True:
        x=3                   
finally:
    client.loop_stop()
    client.disconnect()
