from unittest import TestCase
from unittest.mock import Mock
from datetime import date
from ccy import Ccy


class TestCcy(TestCase):
    def test_convert_one_to_pricing_currency(self):
        EUR = Ccy('EUR')
        USD = Ccy('USD')
        pricing_date = date(2017, 4, 19)
        d = date(2018, 4, 19)

        fxc = Mock()
        env = Mock()
        fxc.get_forward_fx_rate = Mock(return_value=0.95)
        env.get_fx_forward_curve = Mock(return_value=fxc)
        env.get_pricing_currency = Mock(return_value=EUR)

        usd_in_eur = USD.convert_one_to_pricing_currency(env, d)

        self.assertEqual(usd_in_eur, 0.95)
