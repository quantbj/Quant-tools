
from Utils.value_object import ValueObject
from Utils.date_utils import ACT360
from numpy import interp


class IRForwardCurve(ValueObject):
    def __init__(self, ccy, name):
        pass


class IRDiscountFactorForwardCurve(IRForwardCurve):
    def __init__(self, discount_factors, dcc=ACT360):
        pass

    def get_discount_factor(self, d):
        xp = [df[0].toordinal() for df in self.discount_factors]
        fp = [df[1] for df in self.discount_factors]
        f = interp(d.toordinal(), xp, fp)
        return f

    def get_forward_rate(self, date_period):
        df1 = self.get_discount_factor(date_period.start)
        df2 = self.get_discount_factor(date_period.end)
        fr = (df1 / df2 - 1) / self.dcc.dcf(date_period)

        return fr


class FXForwardCurve(ValueObject):
    def __init__(self, ccy_domestic, ccy_foreign):
        pass
