#!/usr/bin/env python3
import Adafruit_BBIO.GPIO as GPIO
import time

LED_1 = "P9_11"
flag = 1
GPIO.setup(LED_1, GPIO.OUT)
try:
    while True:
        if (flag):
            GPIO.output(LED_1, 1)

        else:
            GPIO.output(LED_1, 0)
        flag = not flag
        time.sleep(0.000001)
except KeyboardInterrupt:
    GPIO.cleanup()

