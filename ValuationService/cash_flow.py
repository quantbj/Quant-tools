from Utils.value_object import ValueObject
from math import log, sqrt
from Utils.math import phi
from Utils.date_utils import DatePeriod


class FixedCashFlow(ValueObject):
    def __init__(self, pay_date, amount, ccy, discount_curve=None):
        pass

    def present_value(self, env):
        if self.discount_curve:
            dc = self.discount_curve
        else:
            dc = env.get_discount_curve(self.ccy)

        df = dc.get_discount_factor(self.pay_date)

        return df * self.amount * \
            self.ccy.convert_one_to_pricing_currency(env, self.pay_date)


class FloatingCashFlow(ValueObject):
    def __init__(
            self,
            index,
            fixing_date,
            forward_period,
            pay_date,
            amount,
            ccy,
            discount_curve=None):
        pass

    def present_value(self, env):
        assert(self.fixing_date > env.get_pricing_date())
        dc = self.discount_curve if self.discount_curve else env.get_discount_curve(
            self.ccy)
        fc = env.get_ir_index_forward_curve(self.index)

        df = dc.get_discount_factor(self.pay_date)

        return df \
            * self.amount\
            * self.ccy.convert_one_to_pricing_currency(env, self.pay_date)\
            * fc.get_forward_rate(self.forward_period)\
            * self.forward_period.get_duration() / 360


class GenericCapletFloorlet(ValueObject):
    def __init__(self, index, fixing_date, forward_period, pay_date,
                 nominal, ccy, strike, shift, discount_curve=None):
        pass

    def compute_d1_d2_df_fr_dcf(self, env):
        assert(self.fixing_date > env.get_pricing_date())

        dc = self.discount_curve if self.discount_curve else env.get_discount_curve(
            self.ccy)
        fc = env.get_ir_index_forward_curve(self.index)
        fr = fc.get_forward_rate(self.forward_period)
        df = dc.get_discount_factor(self.pay_date)
        T = self.index.dcc.dcf(
            DatePeriod(
                env.get_pricing_date(),
                self.forward_period.end))

        vol_surf = env.get_caplet_vol_surface(self.index)
        sigma = vol_surf.get_vol(tenor=T, strike=self.strike)
        dcf = self.index.dcc.dcf(self.forward_period)

        d1 = (log((fr + self.shift) / (self.strike + self.shift)) +
              sigma**2 * T / 2) / (sigma * sqrt(T))
        d2 = d1 - sigma * sqrt(T)

        return (d1, d2, df, fr, dcf)


class PlainVanillaCapletSLN(GenericCapletFloorlet):
    def present_value(self, env):
        (d1, d2, df, fr, dcf) = self.compute_d1_d2_df_fr_dcf(env)
        pv = dcf * self.nominal * df * \
            ((fr + self.shift) * phi(d1) - (self.strike + self.shift) * phi(d2))

        return pv


class PlainVanillaFloorletSLN(GenericCapletFloorlet):
    def present_value(self, env):
        (d1, d2, df, fr, dcf) = self.compute_d1_d2_df_fr_dcf(env)
        pv = dcf * self.nominal * df * \
            (-(fr + self.shift) * phi(-d1) + (self.strike + self.shift) * phi(-d2))

        return pv
