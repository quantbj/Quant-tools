
from Utils.value_object import ValueObject
from Utils.date_utils import ACT360
from numpy import interp, array, searchsorted


class IRForwardCurve():
    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name

    def _compute_discount_factor(self, d):
        raise NotImplementedError

    def get_discount_factor(self, d):
        return self._compute_discount_factor(d)

    def get_forward_rate(self, date_period):
        df1 = self.get_discount_factor(date_period.start)
        df2 = self.get_discount_factor(date_period.end)
        fr = (df1 / df2 - 1) / self.dcc.dcf(date_period)

        return fr


class IRDiscountFactorForwardCurve(IRForwardCurve):
    def __init__(self, name, discount_factors, dcc=ACT360):
        self.name = name
        self.discount_factors = discount_factors
        self.dcc = dcc

    def _compute_discount_factor(self, d):
        xp = [df[0].toordinal() for df in self.discount_factors]
        fp = [df[1] for df in self.discount_factors]
        f = interp(d.toordinal(), xp, fp)
        return f


class SimIRDiscountFactorForwardCurve(IRDiscountFactorForwardCurve):
    def _compute_discount_factor(self, d):
        xp = ([df[0].toordinal() for df in self.discount_factors])
        yp = array([df[1] for df in self.discount_factors])

        x = d.toordinal()
        i = searchsorted(xp, x)
        t = (x - xp[i - 1]) / (xp[i] - xp[i - 1])
        y = yp[i - 1, :] * (1-t) + yp[i, :] * t
            

        return y


class FXForwardCurve(ValueObject):
    def __init__(self, ccy_domestic, ccy_foreign):
        pass
