
import datetime
from dateutil import tz

on_off = "OFF"
now = datetime.now(tz=tz.gettz('America/Chicago'))

print "%s: %s" % (now, on_off)
