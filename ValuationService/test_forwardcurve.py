from ValuationService.forwardcurve import IRDiscountFactorForwardCurve, SimIRDiscountFactorForwardCurve
from ValuationService.ccy import EUR
from Utils.date_utils import DatePeriod, ACT360
from datetime import date
from unittest import TestCase
from unittest.mock import Mock
from numpy import array, alltrue
from numpy import searchsorted


class TestForwardCurve(TestCase):
    def test_get_discount_factor(self):
        today = date(2017, 4, 21)
        dfs = [
            (date(2017, 4, 24), 1.1),
            (date(2017, 5, 24), 1.05),
            (date(2017, 6, 24), 1.01),
            (date(2018, 6, 25), 0.99),
            (date(2019, 6, 25), 1.1)]
        fc = IRDiscountFactorForwardCurve(discount_factors=dfs)

        df = fc.get_discount_factor(date(2017, 6, 24))
        self.assertEqual(1.01, df)

        df = fc.get_discount_factor(date(2017, 12, 24))
        self.assertEqual(1.0, df)

    def test_forward_rate(self):
        today = date(2017, 4, 21)
        dfs = [
            (date(2017, 4, 24), 1.1),
            (date(2017, 5, 24), 1.05),
            (date(2017, 6, 24), 1.0028),
            (date(2017, 7, 25), 1.0032),
            (date(2019, 6, 25), 1.1)]
        fc = IRDiscountFactorForwardCurve(discount_factors=dfs, dcc=ACT360)

        d1 = date(2017, 6, 24)
        d2 = date(2017, 7, 25)
        dp = DatePeriod(d1, d2)
        df1 = fc.get_discount_factor(d1)
        df2 = fc.get_discount_factor(d2)
        print('forward test:', df1, df2)

        fr_test = 1 / ACT360.dcf(dp) * (df1 / df2 - 1)
        fr_impl = fc.get_forward_rate(dp)

        print('fr_test', fr_test)
        self.assertAlmostEqual(fr_test, fr_impl)


class TestSimForwardCurve(TestCase):
    def test_get_discount_factor(self):
        today = date(2017, 4, 21)
        dfs = [
            (date(2017, 4, 24), [1.1, 2.1]),
            (date(2017, 5, 24), [1.05, 2.05]),
            (date(2017, 6, 24), [1.01, 2.01]),
            (date(2018, 6, 25), [0.99, 1.99]),
            (date(2019, 6, 25), [1.1, 2.1])]
        fc = SimIRDiscountFactorForwardCurve(discount_factors=dfs)

        df = fc.get_discount_factor(date(2017, 6, 24))
        self.assertTrue(alltrue([1.01, 2.01] == df))

        df = fc.get_discount_factor(date(2017, 12, 24))
        self.assertTrue(alltrue([1.0, 2.0] == df))

    def test_forward_rate(self):
        today = date(2017, 4, 21)
        dfs = [
            (date(2017, 4, 24), array([1.1, 1])),
            (date(2017, 5, 24), array([1.05, 0.99])),
            (date(2017, 6, 24), array([1.0028, 0.98])),
            (date(2017, 7, 25), array([1.0032, 0.97])),
            (date(2019, 6, 25), array([1.1, 0.96]))]
        fc = SimIRDiscountFactorForwardCurve(discount_factors=dfs, dcc=ACT360)

        d1 = date(2017, 6, 24)
        d2 = date(2017, 7, 25)
        dp = DatePeriod(d1, d2)
        df1 = fc.get_discount_factor(d1)
        df2 = fc.get_discount_factor(d2)

        fr_test = 1 / ACT360.dcf(dp) * (df1 / df2 - 1)
        fr_impl = fc.get_forward_rate(dp)

        print(fr_impl)
        self.assertTrue(alltrue(fr_test == fr_impl))
