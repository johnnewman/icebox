"""Entry point for the Icebox temperature monitor.

This program will continuously monitor the system on chip temperature of a
Raspberry Pi. If the temperature passes the threshold defined in MAX_TEMP, the
SIGNAL_PIN will be set to high. Use this high signal with a transistor or relay
to turn on a high-current or high-voltage cooling fan.

After COOLING_TIME, if the temperature has lowered below the threshold, the pin
is set back to low.
"""

import os
import RPi.GPIO as GPIO
import signal
import sys
import time


__author__ = "John Newman"
__copyright__ = "Copyright 2020, John Newman"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "John Newman"
__status__ = "Production"

MAX_TEMP = 53 # Celcius 
SIGNAL_PIN = 29 # Board numbering, not BCM
COOLING_TIME = 300 # Seconds
TEMP_CHECK_INTERVAL = 10 # Seconds

shouldMonitor = True
tempReadTime = 0

def main_loop():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(SIGNAL_PIN, GPIO.OUT)

    highCycleStart = 0
    originalHighCycleStart = 0
    temp = 0

    while shouldMonitor:

        if time.time() - tempReadTime < TEMP_CHECK_INTERVAL:
            continue

        try:
            if highCycleStart > 0:
                if time.time() - highCycleStart >= COOLING_TIME:
                    temp = read_temperature()
                    if temp < MAX_TEMP:
                        print("SoC temp lowered to %.1f'C, below %i'C threshold. Setting pin %i to low." % (temp, MAX_TEMP, SIGNAL_PIN))
                        print("Total time to cool the system: %i sec." % (time.time() - originalHighCycleStart))
                        sys.stdout.flush()
                        GPIO.output(SIGNAL_PIN, GPIO.LOW)
                        highCycleStart = 0
                    else:
                        print("SoC temp of %.1f'C still past the %i'C threshold." % (temp, MAX_TEMP))
                        sys.stdout.flush()
                        highCycleStart = time.time()

            else:
                temp = read_temperature()
                if temp > MAX_TEMP:
                    print("SoC temp of %.1f'C past the %i'C threshold. Setting pin %i to high." % (temp, MAX_TEMP, SIGNAL_PIN))
                    sys.stdout.flush()
                    GPIO.output(SIGNAL_PIN, GPIO.HIGH)
                    highCycleStart = time.time()
                    originalHighCycleStart = highCycleStart
        
        except Exception as e:
            print('Exception %s' % e)
            sys.stdout.flush()

        time.sleep(1)
        
def read_temperature() -> float:
    global tempReadTime
    stream = os.popen("vcgencmd measure_temp | egrep -o \'[0-9]*\.[0-9]*\'")
    tempReadTime = time.time()
    return float(stream.read())

def exit(signal, frame):
    """
    Allows the program to cleanly exit by resetting the I/O status of the pins
    used by this program. cleanup() will only affect SIGNAL_PIN.
    """
    global shouldMonitor
    print("Exiting from signal %i. Resetting GPIO pin." % signal)
    sys.stdout.flush()
    GPIO.cleanup()
    shouldMonitor = False

signal.signal(signal.SIGINT, exit)
signal.signal(signal.SIGTERM, exit)

main_loop()
