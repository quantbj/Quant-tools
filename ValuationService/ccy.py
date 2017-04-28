from Utils.value_object import ValueObject


class Ccy(ValueObject):
    def __init__(self, ccy):
        pass

    def convert_one_to_pricing_currency(self, env, d):
        fxc = env.get_fx_forward_curve(self.ccy)
        return fxc.get_forward_fx_rate(env, d)


EUR = Ccy('EUR')
USD = Ccy('USD')
