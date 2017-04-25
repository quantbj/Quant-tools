from ValuationService.environment import Environment
from ValuationService.ccy import EUR, USD
from ValuationService.forwardcurve import IRForwardCurve, FXForwardCurve
from ValuationService.ir_indices import EURIBOR6M
from datetime import date
from unittest import TestCase
from unittest.mock import Mock


class EnvTest(TestCase):
    def test_get_set_static(self):
        env = Environment()
        env.set_pricing_date(date(2017, 4, 20))
        self.assertEqual(env.get_pricing_date(), date(2017, 4, 20))

        env.set_pricing_currency(EUR)
        self.assertEqual(env.get_pricing_currency(), EUR)

    def test_get_discount_curve(self):
        env = Environment()
        env.set_pricing_currency(EUR)
        eonia = IRForwardCurve(EUR, 'Eonia')

        env.set_discount_curve(EUR, eonia)
        dc = env.get_discount_curve(EUR)
        self.assertEqual(dc, env.get_discount_curve(EUR))

    def test_get_fx_forward_curve(self):
        env = Environment()
        env.set_pricing_currency(EUR)
        fxEURUSD = FXForwardCurve(EUR, USD)

        fxc = env.get_fx_forward_curve(USD)
        self.assertEqual(fxc, fxEURUSD)

    def test_add_ir_forward_curve(self):
        env = Environment()
        env.set_pricing_currency(EUR)
        forward_curve = IRForwardCurve(EUR, 'Euribor-6m')
        env.add_ir_forward_curve(EURIBOR6M, forward_curve)

        self.assertEqual(forward_curve, env._ir_forward_curves[EURIBOR6M])

    def test_get_ir_index_forward_curve(self):
        env = Environment()
        env.set_pricing_currency(EUR)
        forward_curve = IRForwardCurve(EUR, 'Euribor-6m')
        env.add_ir_forward_curve(EURIBOR6M, forward_curve)

        self.assertEqual(
            forward_curve,
            env.get_ir_index_forward_curve(EURIBOR6M))
