#!/usr/bin/env python3

import time

from grove.adc import ADC

def main():
    # Grove - Start ADC
    adc = ADC()

    while True:
        CO2volt= adc.read_voltage(6)

        CO2=int((CO2volt-400)*50.0/16.0)
        print('CO2: {}\n'.format(CO2))

        time.sleep(1)

if __name__ == '__main__':
    main()
