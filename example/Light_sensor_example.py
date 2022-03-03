#!/usr/bin/env python3

import time

from grove.grove_light_sensor_v1_2 import GroveLightSensor

def main():
    # Grove - Light Sensor connected to port A0
    sensor = GroveLightSensor(2)

    while True:
        print('light value {}'.format(sensor.light))

        time.sleep(1)

if __name__ == '__main__':
    main()
