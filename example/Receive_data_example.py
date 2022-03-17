#!/usr/bin/env python3
import cayenne.client #Cayenne MQTT Client
import time

username = "A remplire"
password = "A remplire"
clientid = "A remplire"


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

