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
print pinNumber
print status

def set_light(num, status):
  GPIO.setwarnings(False)
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(int(num), GPIO.OUT)

  if status == "ON":
    lowOrHigh = GPIO.LOW
  else:
    lowOrHigh = GPIO.HIGH

  try:
    light_timer.set_light_status(light_timer.light_dict[num], status)
    GPIO.output(num, lowOrHigh)
    print status
    if status == "OFF":
      GPIO.cleanup()
  except Exception as e:
    print "Error: %s" % e


set_light(pinNumber, status)