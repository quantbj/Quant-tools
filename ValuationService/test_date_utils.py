from ValuationService.date_utils import DatePeriod
from datetime import date
from unittest import TestCase


class TestDatePeriod(TestCase):
    def test_duration(self):
        d1 = date(2017, 4, 20)
        d2 = date(2017, 10, 20)
        dp = DatePeriod(d1, d2)
        dur = dp.get_duration()

        self.assertEqual((d2 - d1).days, dur)
