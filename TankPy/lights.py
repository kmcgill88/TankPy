#!/usr/bin/python
import RPi.GPIO as GPIO
import sys
import light_timer

#Pins options:
#26,19,16,20

#sudo python lights.py 26 ON
#sudo python lights.py 26 OFF

pinNumber = int(sys.argv[1])
status = sys.argv[2]


class Lights(object):

    def __init__(self):
        pass

    @staticmethod
    def set_light(num, on_off):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(int(num), GPIO.OUT)

        if on_off == "ON":
            low_or_high = GPIO.LOW
        else:
            low_or_high = GPIO.HIGH

        try:
            light_timer.LightTimer.set_light_status(light_timer.light_dict[num], on_off)
            GPIO.output(num, low_or_high)
            print on_off
            if on_off == "OFF":
                GPIO.cleanup()
        except Exception as e:
            print "Error: %s" % e


Lights.set_light(pinNumber, status)
