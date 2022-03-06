#!/usr/bin/env python3

import time

from grove.display.jhd1802 import JHD1802

def main():
    # Grove - 16x2 LCD(White on Blue) connected to I2C port
    lcd = JHD1802()

    while True:
        lcd.setCursor(0, 0)
        lcd.write('HelloWorld !!!')

        lcd.setCursor(1, 0)
        lcd.write('app is running ')

        time.sleep(1)

if __name__ == '__main__':
    main()
