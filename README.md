# daylighthours

Calculates the time the Sun is above the horizon (sunset - sunrise) over a date range, returning the min and max.
Based on data from the [Jet Propulsion Laboratory Development Ephemeris](https://en.wikipedia.org/wiki/Jet_Propulsion_Laboratory_Development_Ephemeris) DE421.

Created to support an [article for WRAL.com](https://www.wral.com/look-for-moon-and-mercury-early-next-week/20256284/)
describing the varying experiences of fasting during the daylight hours during Ramadan.
```
daylighthours(latitude, longitude, startdate, enddate)
inputs:
latitude: latitude of the observer (e.g. 39.82)
longitude: longitude of the observer (e.g. -98.58)
startdate (optional): (str) date to start calculations (default: today)
enddate (optional): (str) date to end calculations (default: 365 days from start date)

returns:
dictionary of dates (str) and the fraction (float) of a day the Sun is above
the horizon 
```   

Also calculates, via the [hijri-converter](https://pypi.org/project/hijri-converter/) package, the daylight hours 
across the month of Ramadan in the Islamic calendar.

```
ramadan_daylight_hours(latitude (float), longitude (float), year (integer))
inputs:
latitude: latitude of the observer (e.g. 39.82)
longitude: longitude of the observer (e.g. -98.58)
year: integer

returns:
first day of Ramadan (Gregorian)
laste day of Ramadan (Gregorian)
shortest daylight hours
longest daylight hours
```   

###Limitations:
* Islamic calendar calculations are limited to 1925-2077.
* Daylight calculations are limited to 1900 to 2050, this could easily be adjusted (to varying degrees of accuracy by 
substituting the ephemeris used)

###Note
Months begin in the Islamic calendar when the Moon is first sighted after a new Moon.  Calculations are approximate based on lunar phases.
Like the underlying hijri-converter package, this is not intended for guiding religious observance.