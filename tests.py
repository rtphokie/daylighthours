import unittest
from daylighthours.daylighthours import daylighthours
from pprint import pprint


class MyTestCase(unittest.TestCase):
    def test_something(self):
        result = daylighthours(35.78, -78.64, startdate='2022-01-01', enddate='2022-12-31')
        result = daylighthours(35.78, -78.64)
        pprint(result)


if __name__ == '__main__':
    unittest.main()
