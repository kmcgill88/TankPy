#!/usr/bin/python
import RPi.GPIO as GPIO
import sys
import json as JSON
import os
from datetime import datetime, timedelta
from dateutil import tz

# Pins options:
# 26,19,16,20

# sudo python lights.py 26 ON
# sudo python lights.py 26 OFF

have_arguments = True

try:
    pinNumber = sys.argv[1]
    status = sys.argv[2]
except IndexError as e:
    have_arguments = False
    pass

light_dict = {'white': '26', 'blue': '19', 'moon': '20', '26': 'white', '19': 'blue', '20': 'moon'}

# dir = "%s/time.txt" % os.getcwd()
# status_dir = "%s/status.txt" % os.getcwd()

time_dir = "/home/pi/fishtank/time.txt"
status_dir = "/home/pi/fishtank/status.txt"


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
            LightTimer.set_light_status_by_num(num, on_off)
            GPIO.output(int(num), low_or_high)
            print on_off
            if on_off == "OFF":
                GPIO.cleanup()
        except Exception as e:
            print "Error: %s" % e


class LightTimer(object):

    def __init__(self):
        pass

    @staticmethod
    def get_time(time):
        utc_time = datetime.strptime(time[:-6], '%Y-%m-%dT%H:%M:%S')

        # Hard code zones
        from_zone = tz.gettz('UTC')
        to_zone = tz.gettz('America/Chicago')

        # Tell the datetime object that it's in UTC time zone since
        # datetime objects are 'naive' by default
        utc_time = utc_time.replace(tzinfo=from_zone)

        # Convert time zone
        return utc_time.astimezone(to_zone)

    @staticmethod
    def set_light_status(color, status):
        with open(status_dir, 'r') as text_file:
            d = JSON.load(text_file)

        with open(status_dir, 'w') as text_file:
            d[light_dict[color]] = status
            text_file.write(JSON.dumps(d))

    @staticmethod
    def set_light_status_by_num(num, status):
        LightTimer.set_light_status(light_dict[num], status)

    @staticmethod
    def get_light_status(color):
        if not os.path.exists(status_dir):
            with open(status_dir, 'w') as text_file:
                all_status = {light_dict['white']: "OFF", light_dict['blue']: "OFF", light_dict['moon']: "OFF"}
                text_file.write(JSON.dumps(all_status))

        with open(status_dir, 'r') as text_file:
            status = JSON.load(text_file)
        return status[light_dict[color]]


if have_arguments:
    Lights.set_light(pinNumber, status)

else:

    with open(time_dir) as data_file:
        data = JSON.load(data_file)

    sunrise = LightTimer.get_time(data['results']['sunrise'])
    sunset = LightTimer.get_time(data['results']['sunset'])
    now = datetime.now(tz=tz.gettz('America/Chicago'))

    if (now > LightTimer.get_time(data['results']['astronomical_twilight_begin'])) \
            and (LightTimer.get_light_status('moon') == 'OFF'):
        # moon on
        print "astronomical_twilight_begin: Moon ON"
        Lights.set_light(light_dict['moon'], 'ON')

    if (now > LightTimer.get_time(data['results']['nautical_twilight_begin'])) \
            and (LightTimer.get_light_status('blue') == 'OFF'):
        # blues on
        print "nautical_twilight_begin: Blues ON"
        Lights.set_light(light_dict['blue'], 'ON')

    # Skipping civil_twilight_begin

    if (now > sunrise) and (now < sunset) and (LightTimer.get_light_status('white') == 'OFF'):
        # white on
        print "Sunrise: Whites ON"
        Lights.set_light(light_dict['white'], 'ON')

    if (now > sunrise) and (now < sunset) \
            and ((LightTimer.get_light_status('blue') == 'ON') or (LightTimer.get_light_status('moon') == 'ON')):
        # blues and moon off
        print "Sunrise: Blues and Moon OFF"
        Lights.set_light(light_dict['blue'], 'OFF')
        Lights.set_light(light_dict['moon'], 'OFF')

    # -----

    if (now > sunset) and (LightTimer.get_light_status('blue') == 'OFF'):
        # blues on
        print "Sunset: Blues ON"
        Lights.set_light(light_dict['blue'], 'ON')

    # skipping civil_twilight_end

    if (now > LightTimer.get_time(data['results']['nautical_twilight_end'])) \
            and (LightTimer.get_light_status('moon') == 'OFF'):
        # moons on
        print "nautical_twilight_end: Moon ON"
        Lights.set_light(light_dict['moon'], 'ON')
    elif (now > (LightTimer.get_time(data['results']['nautical_twilight_end']) + timedelta(hours=5))) \
            and (LightTimer.get_light_status('moon') == 'ON'):
        # moons off
        print "nautical_twilight_end: +5 hrs, Moon OFF"
        Lights.set_light(light_dict['moon'], 'OFF')

    if (now > LightTimer.get_time(data['results']['astronomical_twilight_end'])) \
            and (LightTimer.get_light_status('white') == 'ON'):
        # white off
        print "astronomical_twilight_end: Whites OFF"
        Lights.set_light(light_dict['white'], 'OFF')
