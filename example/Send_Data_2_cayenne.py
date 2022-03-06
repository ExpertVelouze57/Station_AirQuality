#!/usr/bin/env python3
import paho.mqtt.client as mqtt
import time

time.sleep(30)

username = "ced99370-4c46-11ec-8da3-474359af83d7"
password = "3eaf7469d09999b419c2f42a225e9055b006b34b"
clientid = "baef0980-9994-11ec-a681-73c9540e1265"

mqttc = mqtt.Client(client_id=clientid)
mqttc.username_pw_set(username, password=password)
mqttc.connect("mqtt.mydevices.com", port=1883, keepalive=60)
mqttc.loop_start()

topic_1 = "v1/" + username + "/things/" + clientid + "/data/1"
topic_2 = "v1/" + username + "/things/" + clientid + "/data/2"

while True:

    try:
        mqttc.publish(topic_1, payload="temp,c=24.5", retain=True)
        mqttc.publish(topic_2, payload="hum,p=45", retain=True)

        print("Data send")
        time.sleep(1)

    except (EOFError, SystemExit, KeyboardInterrupt):

        mqttc.disconnect()

        sys.exit()
