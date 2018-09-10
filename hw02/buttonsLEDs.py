#!/usr/bin/env python3
import Adafruit_BBIO.GPIO as GPIO 
import time 

LED_1 = "P9_11"
LED_2 ="P9_13"
LED_3 ="P9_12"
LED_4 ="P9_14"

button_1 = "P9_15"
button_2 = "P9_17"
button_3 = "P9_16"
button_4 = "P9_18"

# Set the GPIO pins
GPIO.setup(LED_1, GPIO.OUT)
GPIO.setup(LED_2, GPIO.OUT)
GPIO.setup(LED_3, GPIO.OUT)
GPIO.setup(LED_4, GPIO.OUT)

GPIO.setup(button_1, GPIO.IN)
GPIO.setup(button_2, GPIO.IN)
GPIO.setup(button_3, GPIO.IN)
GPIO.setup(button_4, GPIO.IN)

# Map buttons to LEDs

map = {button_1: LED_1, button_2: LED_2, button_3: LED_3, button_4: LED_4}

def updateLEDs(channel):
    state = GPIO.input(channel)
    GPIO.output(map[channel], state)

GPIO.add_event_detect(button_1, GPIO.BOTH, callback=updateLEDs)
GPIO.add_event_detect(button_2, GPIO.BOTH, callback=updateLEDs)
GPIO.add_event_detect(button_3, GPIO.BOTH, callback=updateLEDs)
GPIO.add_event_detect(button_4, GPIO.BOTH, callback=updateLEDs)
try:
    while True:
        time.sleep(100)
except KeyboardInterrupt:
    GPIO.cleanup()

GPIO.cleanup()
