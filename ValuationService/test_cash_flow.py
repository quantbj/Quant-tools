from ValuationService.cash_flow import FixedCashFlow, FloatingCashFlow
from ValuationService.date_utils import DatePeriod
from ValuationService.ccy import EUR, USD
from datetime import date
from unittest import TestCase
from unittest.mock import Mock


class TestFixedCashFlow(TestCase):
    def test_present_value_1(self):
        d = date(2017, 4, 19)
        dc = Mock()
        env = Mock()
        fxc = Mock()
        fxc.get_forward_fx_rate = Mock(return_value=1.0)
        env.get_fx_forward_curve = Mock(return_value=fxc)
        env.get_pricing_currency = Mock(return_value=EUR)
        dc.get_discount_factor = Mock(return_value=0.95)
        env.get_discount_curve = Mock(return_value=dc)

        fcf = FixedCashFlow(d, 100.0, EUR)
        pv = fcf.present_value(env)
        self.assertEqual(pv, 95.0)

    def test_present_value_2(self):
        d = date(2017, 4, 19)
        dc = Mock()
        env = Mock()
        fxc = Mock()
        fxc.get_forward_fx_rate = Mock(return_value=0.95)
        env.get_fx_forward_curve = Mock(return_value=fxc)
        env.get_pricing_currency = Mock(return_value=EUR)
        dc.get_discount_factor = Mock(return_value=0.85)

        fcf = FixedCashFlow(d, 100.0, USD, dc)
        pv = fcf.present_value(env)
        self.assertEqual(pv, 100 * 0.85 * 0.95)


class TestFloatingCashFlow(TestCase):
    def test_present_value(self):
        index = 'EURIBOR06M'
        fixing_date = date(2017, 4, 22)
        forward_period = DatePeriod(date(2017, 4, 24), date(2017, 10, 24))
        pay_date = date(2017, 10, 24)
        dc = Mock()
        env = Mock()
        fxc = Mock()
        fc = Mock()
        fxc.get_forward_fx_rate = Mock(return_value=1.0)
        fc.get_forward_rate = Mock(return_value=0.01)
        env.get_fx_forward_curve = Mock(return_value=fxc)
        env.get_pricing_currency = Mock(return_value=EUR)
        env.get_pricing_date = Mock(return_value=date(2017, 4, 20))
        env.get_index_forward_curve = Mock(return_value=fc)
        dc.get_discount_factor = Mock(return_value=0.95)
        env.get_discount_curve = Mock(return_value=dc)

        fcf = FloatingCashFlow(
            index,
            fixing_date,
            forward_period,
            pay_date,
            1000000,
            EUR)
        pv = fcf.present_value(env)
        self.assertAlmostEqual(pv, 0.01 * 1000000 * 183 / 360 * 0.95)
