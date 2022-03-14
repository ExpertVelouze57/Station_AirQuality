#!/usr/bin/env python3

import os

import sys

#Import all librairy
import cayenne.client #Cayenne MQTT Client
import threading
import logging
import time

from csv import writer
from grove.adc import ADC
from seeed_dht import DHT
from datetime import datetime
from grove.button import Button
from grove.display.jhd1802 import JHD1802
from grove.grove_ryb_led_button import GroveLedButton
from grove.grove_light_sensor_v1_2 import GroveLightSensor




#Variable globale
ip_activation = False
cmd_ready = False

important = False
already_send = False

page = 1

temp = 0.0
hum = 0.0
light_value = 0.0
CO2_value = 0.0

alarm_ready = 1
alarm_in_progress =0
wait_b_send = 3
triger_co2 = 1500

id =0
### Definition of all pin 
PIN_DHT = 5
PIN_CO2 = 6
PIN_BUTTON = 22
PIN_LIGHT_SENSOR = 2

#defiçnition of instance
DHT_sensor = DHT('11', PIN_DHT)
CO2_adc = ADC()
LCD = JHD1802()
Red_button = GroveLedButton(PIN_BUTTON)
Light_sensor = GroveLightSensor(PIN_LIGHT_SENSOR)

#definition des données MQTT
username = "55656590-9b20-11ec-8da3-474359af83d7"
password = "3f5970ed8c45a61103ae0bef382df719b4fb981e"
clientid = "0ecc0210-9d78-11ec-8c44-371df593ba58"

def save_csv():
  global id
  id = datetime.today().strftime('%Y-%m-%d_ %H:%M:%S')
  list_data=[id,temp,hum, light_value, CO2_value]

  with open('/home/pi/base.csv', 'a', newline='') as f_object:  
    # Pass the CSV  file object to the writer() function
    writer_object = writer(f_object)
    # Result - a writer object
    # Pass the data in the list as an argument into the writerow() function
    writer_object.writerow(list_data)  
    # Close the file object
    f_object.close()

def on_message(message):
  global alarm_ready, wait_b_send, triger_co2
  if cmd_ready ==  True : 
    if message.topic == "cmd":
      if message.channel == 1:
        alarm_ready = int(message.value)

      elif  message.channel == 2:
        wait_b_send = int(message.value)

      elif  message.channel == 3:
        triger_co2 = int(message.value)
    client.virtualWrite(9, alarm_ready, "digital_sensor", "d")
    client.virtualWrite(10, wait_b_send, "analog_sensor")
    client.virtualWrite(11, triger_co2, "analog_sensor")
  #print("new paramter : alarme : {}, time : {}, trigger : {}".format(alarm_ready, wait_b_send, triger_co2))




#Fonction

def catch_sensors_values():
  global hum, temp, CO2_value, light_value, important, alarm_in_progress
  
  while True:
    #DHT11 values
    hum, temp = DHT_sensor.read()

    #CO2 value
    CO2_volt= CO2_adc.read_voltage( PIN_CO2 )
    CO2_value=int( ( CO2_volt - 400 ) * 50.0 / 16.0 )

    
    if CO2_value >= triger_co2:
      if important == False:
        important = True
        alarm_in_progress = 1
        client.virtualWrite(4, temp, "temp", "c" )
        client.virtualWrite(5, hum, "rel_hum", "p")
        client.virtualWrite(6, light_value, "lighting_sense", "lux")
        client.virtualWrite(7, CO2_value, "co2", "ppm")
        client.virtualWrite(8, alarm_in_progress, "digital_sensor", "d")
        client.loop()
    else:
      if important == True :
        important =False
        alarm_in_progress = 0
        client.virtualWrite(4, temp, "temp", "c" )
        client.virtualWrite(5, hum, "rel_hum", "p")
        client.virtualWrite(6, light_value, "lighting_sense", "lux")
        client.virtualWrite(7, CO2_value, "co2", "ppm")
        client.virtualWrite(8, alarm_in_progress, "digital_sensor", "d")
        client.loop()    

    #light value
    light_value = Light_sensor.light
    #print('Get value')
    time.sleep(10)


def ip_wifi():
  temp = os.popen('ip -4 addr show wlan0 | grep -oP "(?<=inet ).*(?=/)"').read()
  if len(temp) ==0:
    temp = 'not co'
  
  return temp.replace('\n','')

def ip_eth():
  temp = os.popen('ip -4 addr show eth0 | grep -oP "(?<=inet ).*(?=/)"').read()
  if len(temp) ==0:
    temp = 'not co'

  return temp.replace('\n','')



def show_dht_screen():
  global page

  if page != 1:
    LCD.clear()
    page = 1

  LCD.setCursor(0,0)
  LCD.write('Temp : {0:1}C'.format(temp))
  LCD.setCursor(1,0)
  LCD.write('Hum : {0:2}%'.format(hum))

def show_C02_lignt_screen():
  global page

  if page != 2:
    LCD.clear()
    page = 2

  LCD.setCursor(0,0)
  LCD.write('Lum : {0:2}'.format(light_value))
  LCD.setCursor(1,0)
  LCD.write('CO2 : {0:2}ppm'.format(CO2_value))

def show_ips():
  global page

  if page != 3:
    LCD.clear()
    page = 3

  LCD.setCursor(0,0)
  LCD.write('{}'.format( ip_eth() ))
  LCD.setCursor(1,0)
  LCD.write('{}'.format( ip_wifi() ))

class thread_screen(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)  # ne pas oublier cette ligne

  def run(self):
    global page
    frst_page = True
    time_counter = 0

    while True:
      if cmd_ready == True:
        if page !=4:
          LCD.clear()
          page =4

        LCD.setCursor(0,0)
        LCD.write('Commands ready')

      elif ip_activation == True :
        show_ips()
      else :
        if frst_page ==True:
          show_dht_screen()
        else :
          show_C02_lignt_screen()
      
      time_counter +=1
      if time_counter > 5:
        frst_page = not frst_page
        time_counter =0

      time.sleep(1)



def on_event(index, event, callback):
  global ip_activation, cmd_ready

  if event & Button.EV_SINGLE_CLICK:
    ip_activation= not ip_activation
    Red_button.led.light(True)

  elif event & Button.EV_LONG_PRESS:
    cmd_ready = False
    ip_activation= False
    Red_button.led.light(False)
    time.sleep(3)
    Red_button.led.light(True)

  elif event & Button.EV_DOUBLE_CLICK:
    cmd_ready = True
    Red_button.led.blink()  




if __name__ == '__main__':
  global client
  count =  wait_b_send*60+10
  Red_button.on_event = on_event

  m = thread_screen()
  m.start()

  x = threading.Thread(target=catch_sensors_values)
  x.start()

  client = cayenne.client.CayenneMQTTClient()
  client.on_message = on_message #When message recieved from Cayenne run on_message function
  client.begin(username, password, clientid)

  time.sleep(5)
  client.loop()
  while True:
    #Send data to Cayenne 
    
    if cmd_ready == True:
      #mode cmd, i catch more frequently
      client.loop()
    elif (count >=  (wait_b_send*60)):#Only 10 minutes 
      count = 0
      #prepare to publish
      client.virtualWrite(4, temp, "temp", "c" )
      client.virtualWrite(5, hum, "rel_hum", "p")
      client.virtualWrite(6, light_value, "lighting_sense", "lux")
      client.virtualWrite(7, CO2_value, "co2", "ppm")
      client.virtualWrite(8, alarm_in_progress, "digital_sensor", "d")

      client.virtualWrite(9, alarm_ready, "digital_sensor", "d")
      client.virtualWrite(10, wait_b_send, "analog_sensor")
      client.virtualWrite(11, triger_co2, "analog_sensor")

      client.loop()
      save_csv()
      print("data send")
 
    if cmd_ready == False:
      count+=1
    time.sleep(1)
    print("Status : {}   {} ".format(cmd_ready, count))

  m.join()
  x.join()
