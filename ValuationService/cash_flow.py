from Utils.value_object import ValueObject


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
        if self.discount_curve:
            dc = self.discount_curve
        else:
            dc = env.get_discount_curve(self.ccy)
        fc = env.get_index_forward_curve(self.index)

        df = dc.get_discount_factor(self.pay_date)

        return df \
            * self.amount\
            * self.ccy.convert_one_to_pricing_currency(env, self.pay_date)\
            * fc.get_forward_rate(self.forward_period)\
            * self.forward_period.get_duration() / 360
