import unittest

from daylighthours.daylighthours import daylighthours, ramadan_dates, ramadan_daylight_hours


class TheTestCases(unittest.TestCase):
    def test_daylighthours_specific_dates(self):
        result = daylighthours(35.78, -78.64, startdate='2022-01-01', enddate='2022-12-31')
        self.assertTrue('2022-05-01' in result.keys())
        self.assertAlmostEqual(result['2022-06-08'], .604, 2)

    def test_daylighthours_relative_dates(self):
        result = daylighthours(35.78, -78.64)
        self.assertGreaterEqual(len(result), 1)

    def test_ramadan_start_end(self):
        startdate, enddate = ramadan_dates(2022)
        self.assertEqual(startdate.month, 4)
        self.assertEqual(startdate.day, 2)
        self.assertEqual(enddate.month, 5)
        self.assertEqual(enddate.day, 1)

    def test_ramadan_hours_raleigh(self):
        for year in range(1980, 2031):
            start, end, daylighthoursmin, daylighthoursmax = ramadan_daylight_hours(35.78, -78.64, year)
            print(year, start, end, daylighthoursmin, daylighthoursmax)

    def test_ramadan_hours_alaska(self):
        for year in range(1980, 2031):
            start, end, daylighthoursmin, daylighthoursmax = ramadan_daylight_hours(61.22, -149.90, year)
            print(year, start, end, daylighthoursmin, daylighthoursmax)


if __name__ == '__main__':
    unittest.main()
