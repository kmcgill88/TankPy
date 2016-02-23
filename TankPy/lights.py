#!/usr/bin/python
import RPi.GPIO as GPIO
import sys

#Pins options:
#26,19,16,20

#sudo python lights.py 26 ON
#sudo python lights.py 26 OFF

pinNumber = int(sys.argv[1])
status = sys.argv[2]

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(pinNumber, GPIO.OUT)

if status == "ON":
  lowOrHigh = GPIO.LOW
else:
  lowOrHigh = GPIO.HIGH

try:
  GPIO.output(pinNumber, lowOrHigh)
  print status 
  if status == "OFF":
    GPIO.cleanup()



# End program cleanly with keyboard
except KeyboardInterrupt:
  print "  Quit"

  # Reset GPIO settings
  GPIO.cleanup()
