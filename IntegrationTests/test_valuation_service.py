from unittest import TestCase

from ValuationService.environment import Environment
from ValuationService.ccy import EUR
from ValuationService.forwardcurve import IRDiscountFactorForwardCurve
from ValuationService.ir_indices import EURIBOR6M
from datetime import date


class TestFixedCashFlow(TestCase):
    def setUp(self):
        pricing_date = date(2017, 3, 30)
        dfs_disc = [(date(2017, 4, 27), 1.0)]
        dfs_forw = [(date(2017, 4, 27), 1.0)]
        vol_strikes = [-0.125, 0, 0.125, 0.25]
        vol_mats = [0.5, 1, 1.5, 2]
        cvols = []

        self.env = Environment()
        self.env.set_pricing_currency(EUR)
        self.env.set_pricing_date(pricing_date)

        # Discount curve
        eur_discount_curve = IRDiscountFactorForwardCurve(
            discount_factors=dfs_disc)
        self.env.set_discount_curve(EUR, eur_discount_curve)
        # Forward curve
        eurib6m_forward_curve = IRDiscountFactorForwardCurve(
            discount_factors=dfs_forw)
        self.env.add_ir_forward_curve(EURIBOR6M, eurib6m_forward_curve)
        # Caplet surface
        caplet_surface = CapletVolSurface(
            tenors=vol_tenors,
            strikes=vol_strikes,
            caplet_vols=cvols)
        self.env.set_caplet_vol_surface(EURIBOR6M, caplet_surface)

    def generate_caplets(env, n_caplets, strike):
        from dateutil.relativedelta import relativedelta

        caplets = list()
        forw_start_dates = [env.get_pricing_date + relativedelta(months=+6 * n)
                            for n in range(n_caplets)]

        for d in forw_start_dates:
            caplets.append(
                Caplet(
                    index=EURIBOR6M,
                    fixing_date=d + relativedelta(days=-2),
                    forward_period=DatePeriod(
                        d, d + relativedelta(months=6)),
                    pay_date=d + relativedelta(months=6),
                    strike=strike))

        return caplets

    def test_capfloor_pricing(self):
        caplets = generate_caplets(self.env, n_caplets=4, strike=0.0)
        cap = CapTrade(caplets)

        pv = cap.present_value(self.env)

        print(pv)
