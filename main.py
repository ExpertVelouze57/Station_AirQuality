#!/usr/bin/env python3

#Global librairy
import os
import sys
import time
import logging
from csv import writer
from datetime import datetime

#Librairy for Cayenne and thread
import cayenne.client 
import threading

#Librairy for modules grove
from grove.adc import ADC
from seeed_dht import DHT
from grove.button import Button
from grove.display.jhd1802 import JHD1802
from grove.grove_ryb_led_button import GroveLedButton
from grove.grove_light_sensor_v1_2 import GroveLightSensor

#Recuperation de la date en global (pour les fichiers de log et data)
date_start = datetime.today().strftime('%Y-%m-%d_%H:%M:%S')


#Création d'un fichier de log si besoins
'''
logging.basicConfig(filename="/home/pi/log_"+ date_start  +".log",
                    format='%(asctime)s %(message)s',
                    filemode='w'
                  )

logger = logging.getLogger()
# Setting the threshold of logger to DEBUG
logger.setLevel(logging.DEBUG)
'''


### Variable globale
name_of_file = "data_"+ date_start  +".csv"

## variable gestion de page
ip_activation = False
cmd_ready = False
important = False
page = 1

## Variable données capteurs
temp = 0.0
hum = 0.0
light_value = 0.0
CO2_value = 0.0

## variale input par default
alarm_ready = 1
alarm_in_progress =0
wait_b_send = 5
triger_co2 = 1100


### Definition des pin des différents modules
PIN_DHT = 5
PIN_CO2 = 6
PIN_BUTTON = 22
PIN_LIGHT_SENSOR = 2

### Definition des instances des composant
DHT_sensor = DHT('11', PIN_DHT)
CO2_adc = ADC()
LCD = JHD1802()
Red_button = GroveLedButton(PIN_BUTTON)
Light_sensor = GroveLightSensor(PIN_LIGHT_SENSOR)

#definition des données MQTT
username = #mettre les information données par cayenne
password = #mettre les information données par cayenne
clientid = #mettre les information données par cayenne



#Definition des fonctions pour le stockage des données
def init_csv():
  #Generation des en-tete
  list_data=["Date","Température","Humidité", "Luminosité", "CO2 "]

  with open('/home/pi/'+name_of_file, 'a', newline='') as f_object:  
    writer_object = writer(f_object)
    writer_object.writerow(list_data)  
    f_object.close()

def save_csv():
  #Save data 
  id = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
  list_data=[id,temp,hum, light_value, CO2_value]

  with open('/home/pi/'+name_of_file, 'a', newline='') as f_object:  
    writer_object = writer(f_object)
    writer_object.writerow(list_data)  
    f_object.close()



#Definition de la fonction de traitement des message recu (MQTT)
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
  #logger.info("new paramter : alarme : {}, time : {}, trigger : {}".format(alarm_ready, wait_b_send, triger_co2))




#Fonction récuperation des donnée provenant de capteur
def catch_sensors_values():
  global hum, temp, CO2_value, light_value, important, alarm_in_progress
  
  while True:
    #DHT11 values
    hum, temp = DHT_sensor.read()

    #CO2 value
    CO2_volt= CO2_adc.read_voltage( PIN_CO2 )
    CO2_value=int( ( CO2_volt - 400 ) * 50.0 / 16.0 )

    #Triger sur la valeur CO2, si detecter envoie message
    if CO2_value >= triger_co2:
      if important == False and alarm_ready == 0:
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
        client.loop()
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


#fonction de récuperation de l'adresse ip
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


#Affichage température et humidité ecran LCD
def show_dht_screen():
  global page

  if page != 1:
    LCD.clear()
    page = 1

  LCD.setCursor(0,0)
  LCD.write('Temp : {0:1}C'.format(temp))
  LCD.setCursor(1,0)
  LCD.write('Hum : {0:2}%'.format(hum))

#Affichage Co2 et light ecran lcd
def show_C02_lignt_screen():
  global page

  if page != 2:
    LCD.clear()
    page = 2

  LCD.setCursor(0,0)
  LCD.write('Lum : {0:2}'.format(light_value))
  LCD.setCursor(1,0)
  LCD.write('CO2 : {0:2}ppm'.format(CO2_value))

#Affichage des ips
def show_ips():
  global page

  if page != 3:
    LCD.clear()
    page = 3

  LCD.setCursor(0,0)
  LCD.write('{}'.format( ip_eth() ))
  LCD.setCursor(1,0)
  LCD.write('{}'.format( ip_wifi() ))

#Classe pour la gestion de l'affichage des écran
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


#Fonction de capture information provenant du button
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
  #logger.info("Welcome on station Liphy")
  count =  wait_b_send*60+10

  #definition fct pour event button
  Red_button.on_event = on_event

  #démmarage thread écran
  m = thread_screen()
  m.start()

  #Demarage thread pour récupération des données
  x = threading.Thread(target=catch_sensors_values)
  x.start()

  #Initialisation connexion avec cayenne
  client = cayenne.client.CayenneMQTTClient()
  client.on_message = on_message #When message recieved from Cayenne run on_message function
  client.begin(username, password, clientid)

  #Petit pause et récupération des données drivers mqtt
  time.sleep(5)
  client.loop()

  #init save of data
  init_csv()


  while True:    
    if cmd_ready == True:
      #mode cmd, i catch more frequently
      client.loop()

    elif (count >=  (wait_b_send*60)):#time in minutes
      count = 0
      #refresh connexion
      client.begin(username, password, clientid)
      
      #prepare to publish
      client.virtualWrite(4, temp, "temp", "c" )
      client.virtualWrite(5, hum, "rel_hum", "p")
      client.virtualWrite(6, light_value, "lighting_sense", "lux")
      client.virtualWrite(7, CO2_value, "co2", "ppm")
      client.virtualWrite(8, alarm_in_progress, "digital_sensor", "d")

      client.virtualWrite(9, alarm_ready, "digital_sensor", "d")
      client.virtualWrite(10, wait_b_send, "analog_sensor")
      client.virtualWrite(11, triger_co2, "analog_sensor")

      #Envoie des données
      client.loop()
      #logger.info("Data send")


      #Enregistrement en local
      save_csv()
      #logger.info("Data save")

 
    if cmd_ready == False:
      count+=1
      #logger.info(count)
      print(count)
    time.sleep(1)

  m.join()
  x.join()
