#!/usr/bin/env python3
import paho.mqtt.client as mqtt
import time

time.sleep(30)

username = "A remplire"
password = "A remplire"
clientid = "A remplire"

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
