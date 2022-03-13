#!/usr/bin/env python3
import cayenne.client #Cayenne MQTT Client
import time

username = "55656590-9b20-11ec-8da3-474359af83d7"
password = "3f5970ed8c45a61103ae0bef382df719b4fb981e"
clientid = "0ecc0210-9d78-11ec-8c44-371df593ba58"


def on_message(message):
    print("message received: " + str(message.value))


client = cayenne.client.CayenneMQTTClient()
client.on_message = on_message #When message recieved from Cayenne run on_message function
client.begin(username  , password, clientid,port=8883)
client.loop()

topic_1 = "v1/" + username + "/things/" + clientid + "/data/1"


while True:
  client.loop()
  client.virtualWrite(1, 10.5, "temp", "°C")
