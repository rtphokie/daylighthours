import datetime
from datetime import timedelta

from dateutil.parser import parse
from hijri_converter import Hijri, Gregorian
from pytz import utc
from skyfield import almanac
from skyfield.api import Loader, wgs84

load = Loader('/var/data')
ts = load.timescale(builtin=True)

eph = load('de421.bsp')


def daylighthours(lat, lng, startdate=None, enddate=None):
    '''
    Calculates the difference, in decimal days, between sunrise and sunset
    
    :param lat: latitude of the observer (float) 
    :param lng: longitude of the observer (float, remember latitudes west of the prime meridian are negative)
    :param startdate: any parsable date string, defaults to today
    :param enddate: any parsable date string, defaults 365 days from the start
    :return: dictionary of dates (string) and the fraction of a day the Sun is above the horizon
    '''
    observer = wgs84.latlon(lat, lng)

    t0, t1 = _timerange(enddate, startdate)
    t, y = almanac.find_discrete(t0, t1, almanac.sunrise_sunset(eph, observer))

    results = dict()
    if y[0] == 0:  # ensure we start with a sunrise
        start = 1
    else:
        start = 0
    for i in range(start, len(t), 2):
        if i == 0 and y[i] != 1:
            continue  # start with a sunrise
        if i == len(t) - 1 and y[i] != 0:
            continue  # end with a sunset
        results[t[i + 1].utc_strftime('%Y-%m-%d')] = t[i + 1] - t[i]

    #     chunk = ints[i:i + chunk_size]
    #     # process chunk of size <= chunk_size

    return results


def _timerange(enddate, startdate):
    # parses text start and end dates, returns SkyField date objects
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


def ramadan_dates(year):
    '''
    calculate the dates of Ramadan
    :param year: (Gregorian) year
    :return: (Gregorian) dates of the first and last day of the 9th month in the Islamic calendar
    '''
    ''' Gregorian dates of Ramadan during a given Gregorian year'''
    h = Gregorian(year, 1, 1).to_hijri()
    if h.month > 9:
        year = h.year - 1
    else:
        year = h.year
    g = Hijri(year, 9, 1).to_gregorian()
    start = datetime.date(g.year, g.month, g.day)
    try:
        g = Hijri(year, 9, 30).to_gregorian()
    except:
        g = Hijri(year, 9, 29).to_gregorian()
    end = datetime.date(g.year, g.month, g.day)
    return start, end


def ramadan_daylight_hours(lat, lng, year):
    '''
    Calculates the min and max time the Sun is above the horizon during the month of Ramadan for a given (Gregorian) year

    :param lat: latitude of the observer (float) 
    :param lng: longitude of the observer (float, remember latitudes west of the prime meridian are negative)
    :param year: Gregorian year (integer)
    :return: (Gregorian) dates of the first and last day of Ramadan (str), max and min timedeltas between sunrise and sunset each day0D
    '''    start, end = ramadan_dates(year)
    end += timedelta(days=1)  # avoid off by 1 error
    hours = daylighthours(lat, lng, startdate=start.strftime('%x'), enddate=end.strftime('%x'))
    tmin = timedelta(days=min(hours.values()))
    tmax = timedelta(days=max(hours.values()))
    return start, end, tmin, tmax
