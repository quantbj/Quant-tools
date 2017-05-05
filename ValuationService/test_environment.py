from ValuationService.environment import Environment, VaREnvironmentCurvesFactory
from ValuationService.ccy import EUR, USD
from ValuationService.forwardcurve import IRForwardCurve, FXForwardCurve, \
    IRDiscountFactorForwardCurve
from ValuationService.ir_indices import EURIBOR6M
from Utils.correlation import CKey
from unittest import TestCase
from unittest.mock import Mock
from datetime import date
from numpy import array, mean
from collections import OrderedDict


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
        eonia = IRDiscountFactorForwardCurve(name='eonia', discount_factors=[])

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
        forward_curve = IRDiscountFactorForwardCurve(
            name='euribor6m', discount_factors=[])
        env.add_ir_forward_curve(EURIBOR6M, forward_curve)

        self.assertEqual(forward_curve, env._ir_forward_curves[EURIBOR6M])

    def test_get_ir_index_forward_curve(self):
        env = Environment()
        env.set_pricing_currency(EUR)
        forward_curve = IRDiscountFactorForwardCurve(
            name='eonia', discount_factors=[])
        env.add_ir_forward_curve(EURIBOR6M, forward_curve)

        self.assertEqual(
            forward_curve,
            env.get_ir_index_forward_curve(EURIBOR6M))


class TestVaREnvFactory(TestCase):
    def test_produce(self):
        today = date(2017, 4, 21)
        dfs_eonia = [
            (date(2017, 4, 24), 1.),
            (date(2017, 5, 24), 0.995),
            (date(2017, 6, 24), 0.99),
            (date(2017, 7, 25), 0.985),
            (date(2019, 6, 25), 0.98)]
        dfs_euribor = [
            (date(2017, 4, 24), 1.0),
            (date(2017, 5, 24), 1.05),
            (date(2017, 6, 24), 1.0028),
            (date(2017, 7, 25), 1.0032),
            (date(2019, 6, 25), 1.1)]
        n_paths = 10000
        env = Environment()
        env.set_pricing_date(today)
        eonia = IRDiscountFactorForwardCurve(
            name='eonia', discount_factors=dfs_eonia)
        env.set_discount_curve(EUR, eonia)
        euribor6m = IRDiscountFactorForwardCurve(
            name='euribor6m', discount_factors=dfs_euribor)
        env.add_ir_forward_curve(EURIBOR6M, euribor6m)

        cov_matrix = OrderedDict({CKey(euribor6m, euribor6m): 0.01**2, CKey(eonia, eonia): 0.005**2,
                                  CKey(euribor6m, eonia): 0.01 * 0.005 * 0.8})
        env_factory = VaREnvironmentCurvesFactory(env)
        env_factory.set_number_of_paths(n_paths)
        env_factory.set_cov_matrix(cov_matrix)
        var_env = env_factory.produce()

        var_euribor6m = var_env.get_ir_index_forward_curve(EURIBOR6M)
        self.assertEqual(
            n_paths, len(var_euribor6m.get_discount_factor(date(2017, 5, 24))))
        self.assertAlmostEqual(
            euribor6m.get_discount_factor(date(2017, 5, 24)),
            mean(var_euribor6m.get_discount_factor(date(2017, 5, 24))), 4)

        var_eonia = var_env.get_discount_curve(EUR)
        self.assertEqual(
            n_paths, len(var_eonia.get_discount_factor(date(2017, 5, 24))))
        self.assertAlmostEqual(
            eonia.get_discount_factor(date(2017, 5, 24)),
            mean(var_eonia.get_discount_factor(date(2017, 5, 24))), 4)
