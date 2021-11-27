import Adafruit_SSD1306
import RPi.GPIO as GPIO

import display
import voice

disp = Adafruit_SSD1306.SSD1306_128_32(rst=0)
disp.begin()
disp.clear()
disp.display()

if __name__ == '__main__':
    pass