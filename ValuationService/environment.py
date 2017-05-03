from ValuationService.forwardcurve import IRForwardCurve, FXForwardCurve, SimIRDiscountFactorForwardCurve
from ValuationService.ccy import EUR
from Utils.correlation import CKey
from numpy.random import multivariate_normal
from numpy import zeros, array


class Environment:
    def __init__(self, pricing_currency=EUR):
        self._pricing_currency = pricing_currency
        self._ir_forward_curves = dict()
        self._discount_curves = dict()
        self._ir_caplet_vol_surface = dict()

    def set_pricing_currency(self, ccy):
        self._pricing_currency = ccy

    def get_pricing_currency(self):
        return self._pricing_currency

    def set_pricing_date(self, d):
        self.pricing_date = d

    def get_pricing_date(self):
        return self.pricing_date

    def set_discount_curve(self, ccy, curve):
        self._discount_curves[ccy] = curve

    def get_discount_curve(self, ccy):
        return self._discount_curves[ccy]

    def get_fx_forward_curve(self, ccy):
        return FXForwardCurve(self._pricing_currency, ccy)

    def add_ir_forward_curve(self, index, curve):
        self._ir_forward_curves[index] = curve

    def get_ir_index_forward_curve(self, index):
        return self._ir_forward_curves[index]

    def add_caplet_vol_surface(self, index, volatility_surface):
        self._ir_caplet_vol_surface[index] = volatility_surface

    def get_caplet_vol_surface(self, index):
        return self._ir_caplet_vol_surface[index]


class VaREnvironmentCurvesFactory():
    def __init__(self, env):
        self.env = env

    def set_number_of_paths(self, n):
        self.number_of_paths = n

    def set_cov_matrix(self, cov_matrix):
        self.cov_matrix = cov_matrix

    def _generate_mean_cov(self, curve_elems):
        dim = len(curve_elems)

        mean = zeros(dim)
        cov = array([[self.cov_matrix[CKey(e1, e2)]
                      for e1 in curve_elems] for e2 in curve_elems])

        return (mean, cov)

    def _add_zero_rate_to_discount_factors(self, dfs, rate):
        implied_rates = [
            (d, df**(-365.0 / (d - self.env.pricing_date).days) - 1.0) for d, df in dfs]
        new_dfs = [(d, (1.0 + r + rate)**(-(d - self.env.pricing_date).days / 365.0))
                   for d, r in implied_rates]

        return new_dfs

    def produce(self):
        new_env = Environment()
        new_env.set_pricing_currency(self.env.get_pricing_currency())
        new_env.set_pricing_date(self.env.get_pricing_date())
        new_env._ir_caplet_vol_surface = self.env._ir_caplet_vol_surface

        curve_elems = [key.e1 for key in self.cov_matrix if key.e1 == key.e2]
        mean, cov = self. _generate_mean_cov(curve_elems)
        rng = multivariate_normal(mean, cov, self.number_of_paths).T
        curve_dict = dict(zip(curve_elems, rng))

        for index, curve in self.env._ir_forward_curves.items():
            new_dfs = self._add_zero_rate_to_discount_factors(
                curve.discount_factors, curve_dict[curve])
            new_env.add_ir_forward_curve(
                index, SimIRDiscountFactorForwardCurve(
                    name=curve.name, discount_factors=new_dfs))

        for ccy, curve in self.env._discount_curves.items():
            new_dfs = self._add_zero_rate_to_discount_factors(
                curve.discount_factors, curve_dict[curve])
            new_env.set_discount_curve(
                ccy, SimIRDiscountFactorForwardCurve(
                    name=curve.name, discount_factors=new_dfs))

        return(new_env)
