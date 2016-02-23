#!/usr/bin/python

import json as JSON
import os
from datetime import datetime, timedelta
from dateutil import tz
from lights import Lights

light_dict = {'white': '26', 'blue': '19', 'moon': '20', '26': 'white', '19': 'blue', '20': 'moon'}

# dir = "%s/time.txt" % os.getcwd()
# status_dir = "%s/status.txt" % os.getcwd()

dir = "/home/pi/fishtank/time.txt"
status_dir = "/home/pi/fishtank/status.txt"


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
    def get_light_status(color):
        if not os.path.exists(status_dir):
            with open(status_dir, 'w') as text_file:
                all_status = {light_dict['white']: "OFF", light_dict['blue']: "OFF", light_dict['moon']: "OFF"}
                text_file.write(JSON.dumps(all_status))

        with open(status_dir, 'r') as text_file:
            status = JSON.load(text_file)
        return status[light_dict[color]]


with open(dir) as data_file:
    data = JSON.load(data_file)


sunrise = LightTimer.get_time(data['results']['sunrise'])
sunset = LightTimer.get_time(data['results']['sunset'])
now = datetime.now(tz=tz.gettz('America/Chicago'))

if (now > LightTimer.get_time(data['results']['astronomical_twilight_begin'])) \
        and (LightTimer.get_light_status('moon') == 'OFF'):
    # moon on
    Lights.set_light(light_dict['moon'], 'ON')

if (now > LightTimer.get_time(data['results']['nautical_twilight_begin'])) \
        and (LightTimer.get_light_status('blue') == 'OFF'):
    # blues on
    Lights.set_light(light_dict['blue'], 'ON')

# Skipping civil_twilight_begin

if (now > sunrise) and (now < sunset) and (LightTimer.get_light_status('white') == 'OFF'):
    # white on
    Lights.set_light(light_dict['white'], 'ON')

if (now > sunrise) and (now < sunset) and ((LightTimer.get_light_status('blue') == 'ON') or (LightTimer.get_light_status('moon') == 'ON')):
    # blues and moon off
    Lights.set_light(light_dict['blue'], 'OFF')
    Lights.set_light(light_dict['moon'], 'OFF')


# -----

if (now > sunset) and (LightTimer.get_light_status('blue') == 'OFF'):
    # blues on
    Lights.set_light(light_dict['blue'], 'ON')


# skipping civil_twilight_end


if (now > LightTimer.get_time(data['results']['nautical_twilight_end'])) \
        and (LightTimer.get_light_status('moon') == 'OFF'):
    # moons on
    Lights.set_light(light_dict['moon'], 'ON')
elif (now > (LightTimer.get_time(data['results']['nautical_twilight_end']) + timedelta(hours=5))) \
        and (LightTimer.get_light_status('moon') == 'ON'):
    # moons off
    Lights.set_light(light_dict['moon'], 'OFF')

if (now > LightTimer.get_time(data['results']['astronomical_twilight_end'])) \
        and (LightTimer.get_light_status('white') == 'ON'):
    # white off
    Lights.set_light(light_dict['white'], 'OFF')
