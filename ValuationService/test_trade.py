from ValuationService.trade import AbstractTrade
from ValuationService.trade import FutureCashFlowTrade
from ValuationService.cash_flow import FixedCashFlow
from ValuationService.ccy import EUR, USD
from datetime import date
from unittest import TestCase
from unittest.mock import Mock


class TestTrade(TestCase):
    def test_abstract_trade(self):
        abstract_trade = AbstractTrade(dict())
        env = None
        self.assertRaises(
            NotImplementedError,
            abstract_trade.present_value,
            env)
        self.assertRaises(NotImplementedError, abstract_trade.required_curves)

    def test_FutureCashFlowTrade_1(self):
        data_dict_wrong = {'cash flows wrong': 0}

        self.assertRaises(AssertionError, FutureCashFlowTrade, data_dict_wrong)

    def test_FutureCashFlowTrade_2(self):
        d1 = date(2018, 1, 1)
        d2 = date(2019, 1, 1)
        data_dict = {'cash_flows': [FixedCashFlow(d1, 100, EUR),
                                    FixedCashFlow(d2, 200, EUR)]}
        dc = Mock()
        env = Mock()
        fxc = Mock()
        fxc.get_forward_fx_rate = Mock(return_value=1.0)
        env.get_fx_forward_curve = Mock(return_value=fxc)
        env.get_pricing_currency = Mock(return_value=EUR)

        discount_factors = {d1: 0.9, d2: 0.8}
        dc.get_discount_factor = Mock(
            side_effect=lambda d: discount_factors[d])
        env.get_discount_curve = Mock(return_value=dc)

        cf_trade = FutureCashFlowTrade(data_dict)
        pv = cf_trade.present_value(env)

        self.assertEqual(pv, 100 * 0.9 + 200 * 0.8)

    def test_FutureCashFlowTrade_3(self):
        d1 = date(2018, 1, 1)
        d2 = date(2019, 1, 1)
        data_dict = {'cash_flows': [FixedCashFlow(d1, 100, EUR),
                                    FixedCashFlow(d2, 200, USD)]}
        dc = Mock()
        env = Mock()
        fxcEUR = Mock()
        fxcUSD = Mock()
        fxcEUR.get_forward_fx_rate = Mock(return_value=1.0)
        fxcUSD.get_forward_fx_rate = Mock(return_value=0.95)
        fx_curves = {'EUR': fxcEUR, 'USD': fxcUSD}
        env.get_fx_forward_curve = Mock(side_effect=lambda ccy: fx_curves[ccy])
        env.get_pricing_currency = Mock(return_value=EUR)

        discount_factors = {d1: 0.9, d2: 0.8}
        dc.get_discount_factor = Mock(
            side_effect=lambda d: discount_factors[d])
        env.get_discount_curve = Mock(return_value=dc)

        cf_trade = FutureCashFlowTrade(data_dict)
        pv = cf_trade.present_value(env)

        self.assertEqual(pv, 100 * 0.9 + 200 * 0.8 * 0.95)
