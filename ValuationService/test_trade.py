from ValuationService.trade import AbstractTrade
from ValuationService.trade import FutureCashFlowTrade
from ValuationService.utils import FixedCashFlow
from ValuationService.ccy import EUR
from datetime import date
from unittest import TestCase
from unittest.mock import Mock

class TestTrade(TestCase):
    def test_abstract_trade(self):
        abstract_trade = AbstractTrade(dict())
        env = None
        self.assertRaises(NotImplementedError, abstract_trade.present_value, env)
        self.assertRaises(NotImplementedError, abstract_trade.required_curves)
        
    def test_FutureCashFlowTrade_1(self):
        data_dict_wrong = {'cash flows wrong': 0 }

        self.assertRaises(AssertionError, FutureCashFlowTrade, data_dict_wrong)
        
    def test_FutureCashFlowTrade_2(self):
        data_dict = {'cash_flows': [ FixedCashFlow(date(2018,1,1), 100, EUR) ] }
        dc = Mock()
        env = Mock()
        dc.get_discount_factor = Mock(return_value=0.9)
        env.get_discount_curve = Mock(return_value=dc)
        
        cf_trade = FutureCashFlowTrade(data_dict)
        pv = cf_trade.present_value(env)
        
        self.assertEqual(pv, 100 * 0.9)
        