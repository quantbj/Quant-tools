from ValuationService.utils import FixedCashFlow
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
