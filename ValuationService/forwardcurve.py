
from Utils.value_object import ValueObject
from numpy import interp


class IRForwardCurve(ValueObject):
    def __init__(self, ccy, name):
        pass


class IRDiscountFactorForwardCurve(IRForwardCurve):
    def __init__(self, ccy, name, curve_date, discount_factors):
        pass

    def get_discount_factor(self, d):
        xp = [df[0].toordinal() for df in self.discount_factors]
        fp = [df[1] for df in self.discount_factors]
        f = interp(d.toordinal(), xp, fp)
        return f


class FXForwardCurve(ValueObject):
    def __init__(self, ccy_domestic, ccy_foreign):
        pass
