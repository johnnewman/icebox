"""Entry point for the Icebox temperature monitor.

This program will continuously monitor the system on chip temperature of a
Raspberry Pi. If the temperature passes the threshold defined in MAX_TEMP, the
SIGNAL_PIN will be set to high. Use this high signal with a transistor or relay
to turn on a high-current or high-voltage cooling fan.
"""

import RPi.GPIO as GPIO
import time
import os

__author__ = "John Newman"
__copyright__ = "Copyright 2020, John Newman"
__license__ = "MIT"
__version__ = "1.1.0"
__maintainer__ = "John Newman"
__status__ = "Production"

MAX_TEMP = 50 # Celcius 
SIGNAL_PIN = 29 # Board numbering, not BCM
COOLING_TIME = 60 # Seconds
TEMP_CHECK_INTERVAL = 10 # Seconds

GPIO.setmode(GPIO.BOARD)
GPIO.setup(SIGNAL_PIN, GPIO.OUT)
while True:
    try:
        stream = os.popen('vcgencmd measure_temp | egrep -o \'[0-9]*\.[0-9]*\'')
        temp = float(stream.read())
        if temp > MAX_TEMP:
            print("SoC temp of %.1f'C past %i'C threshold. Signaling pin %i." % (temp, MAX_TEMP, SIGNAL_PIN))
            GPIO.output(SIGNAL_PIN, GPIO.HIGH)
            time.sleep(COOLING_TIME)
        else:
            GPIO.output(SIGNAL_PIN, GPIO.LOW)
    except Exception as e:
        print('Exception %s' % e)
    time.sleep(TEMP_CHECK_INTERVAL)
GPIO.cleanup()
