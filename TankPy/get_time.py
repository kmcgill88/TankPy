#!/usr/bin/python
import urllib2
import os

dir = "%s/time.txt" % os.getcwd()
#dir = "/home/pi/fishtank/time.txt"

json = urllib2.urlopen("http://api.sunrise-sunset.org/json?lat=41.679249&lng=-93.785765&date=today&formatted=0").read()
with open(dir, 'w') as text_file:
    text_file.write(json)