from Utils.date_utils import DatePeriod
from Utils.date_utils import DayCountConvention, ACT360
from datetime import date
from unittest import TestCase


class TestDatePeriod(TestCase):
    def test_duration(self):
        d1 = date(2017, 4, 20)
        d2 = date(2017, 10, 20)
        dp = DatePeriod(d1, d2)
        dur = dp.get_duration()

        self.assertEqual((d2 - d1).days, dur)


class TestDCC(TestCase):
    def test_abstract(self):
        dcc = DayCountConvention()
        self.assertRaises(NotImplementedError, dcc.dcf, None)

    def test_act360(self):
        dcc = ACT360
        d1 = date(2017, 4, 20)
        d2 = date(2017, 10, 20)
        dp = DatePeriod(d1, d2)
        dur = dp.get_duration()
        self.assertAlmostEqual(dur / 360.0, dcc.dcf(dp))
