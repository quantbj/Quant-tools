from ValuationService.forwardcurve import IRDiscountFactorForwardCurve
from ValuationService.ccy import EUR
from datetime import date
from unittest import TestCase
from unittest.mock import Mock


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
