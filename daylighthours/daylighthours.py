from datetime import timedelta

from dateutil.parser import parse
from pytz import utc
from skyfield import almanac
from skyfield.api import Loader, wgs84

load = Loader('/var/data')
ts = load.timescale(builtin=True)

eph = load('de421.bsp')


def daylighthours(lat, lng, startdate=None, enddate=None):
    bluffton = wgs84.latlon(lat, lng)

    t0, t1 = timerange(enddate, startdate)
    t, y = almanac.find_discrete(t0, t1, almanac.sunrise_sunset(eph, bluffton))

    results = dict()
    for i in range(0, len(t), 2):
        if i == 0 and y[i] != 1:
            continue # start with a sunrise
        if i == len(t)-1 and y[i] != 0:
            continue # end with a sunset
        results[t[i+1].utc_strftime('%Y-%m-%d')]=t[i+1]-t[i]


    #     chunk = ints[i:i + chunk_size]
    #     # process chunk of size <= chunk_size

    return results


def timerange(enddate, startdate):
    if startdate is None:
        t0 = ts.now()
    else:
        startdate_dt = parse(startdate)
        t0 = ts.from_datetime(startdate_dt.replace(tzinfo=utc))
    if enddate is None:
        dt = t0.utc_datetime()
        t1 = ts.from_datetime(dt + timedelta(days=366))

    else:
        enddate_dt = parse(enddate)
        t1 = ts.from_datetime(enddate_dt.replace(tzinfo=utc))
    return t0, t1
