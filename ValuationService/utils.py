class FixedCashFlow:
    def __init__(self, date, amount, ccy, discount_curve = None):
        self.date = date
        self.amount = amount
        self.ccy = ccy
        self.discount_curve = discount_curve
        
    def present_value(self, env):
        if self.discount_curve:
            dc = self.discount_curve
        else:
            dc = env.get_discount_curve(self.ccy)
        
        df = dc.get_discount_factor(self.date)

        return df * self.amount * self.ccy.convert_one_to_pricing_currency(env, self.date)
        