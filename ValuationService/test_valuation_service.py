from unittest import TestCase

from ValuationService.environment import Environment
from ValuationService.ccy import EUR
from ValuationService.forwardcurve import IRDiscountFactorForwardCurve
from ValuationService.ir_indices import EURIBOR6M
from ValuationService.volatility import CapletVolSurface
from ValuationService.cash_flow import PlainVanillaCapletSLN
from ValuationService.trade import IRCapTrade
from Utils.date_utils import DatePeriod
from datetime import date

EXPECTED_PV_PLAIN_VANILLA_CAP = 2308.594078374


class IntTestCapPricing(TestCase):
    def setUp(self):
        pricing_date = date(2017, 3, 30)
        dfs_disc = [(date(2017, 4, 27), 1.0)]
        dfs_forw = [(date(2017, 4, 27), 1.0)]
        vol_strikes = [-0.125, 0, 0.125, 0.25]
        vol_tenors = [1, 1.5, 2]
        cvols = [
            [0.0740, 0.0936, 0.1105, 0.1254],
            [0.0828, 0.1027, 0.1195, 0.1343],
            [0.0943, 0.1123, 0.1277, 0.1414]
        ]

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
        self.env.add_caplet_vol_surface(EURIBOR6M, caplet_surface)

    def generate_caplets(self, env, n_caplets, strike):
        from dateutil.relativedelta import relativedelta

        caplets = list()
        forw_start_dates = [env.get_pricing_date() + relativedelta(months=+(6 * (n + 1)))
                            for n in range(n_caplets)]

        for d in forw_start_dates:
            caplets.append(
                PlainVanillaCapletSLN(
                    index=EURIBOR6M,
                    fixing_date=d + relativedelta(days=-2),
                    forward_period=DatePeriod(d, d + relativedelta(months=6)),
                    pay_date=d + relativedelta(months=6),
                    nominal=1000000,
                    ccy=EUR,
                    strike=strike,
                    shift=0.03))

        return caplets

    def test_captrade_pricing(self):
        caplets = self.generate_caplets(env=self.env, n_caplets=3, strike=0.0)
        
        #shocked_env = ShockedIRCurve(env, {EURIBOR6M: (ALWAYS, 1e-4)})
        
        cap = IRCapTrade(caplets)
        pv = cap.present_value(self.env)
        # pv_shocked = cap.present_value(self.shocked_env)

        self.assertAlmostEqual(EXPECTED_PV_PLAIN_VANILLA_CAP, pv)
        # print(pv, pv_shocked)