#!/usr/bin/env python3

import time
from grove.button import Button
from grove.grove_ryb_led_button import GroveLedButton

button = GroveLedButton(22)

def on_event(index, event, tm):
    if event & Button.EV_SINGLE_CLICK:
        print('single click')
        button.led.light(True)

    elif event & Button.EV_LONG_PRESS:
        print('long press')
        button.led.light(False)

    elif event & Button.EV_DOUBLE_CLICK:
        print(' press')
        button.led.blink()  

def main():
    #button = GroveLedButton(22)
    button.on_event = on_event

    while True:
        time.sleep(1)

if __name__ == '__main__':
    main()
