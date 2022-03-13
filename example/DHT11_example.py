#!/usr/bin/env python3

import time
from seeed_dht import DHT

def main():
    # Grove - Temperature&Humidity Sensor connected to port D5
    sensor = DHT('11', 5)

    while True:
        humi, temp = sensor.read()
        print('temperature {}C, humidity {}%'.format(temp, humi))
        print('DHT{0}, humidity {1:.1f}%, temperature {2:.1f}*'.format(sensor.dht_type, humi, temp))

        time.sleep(1)

if __name__ == '__main__':
    main()
