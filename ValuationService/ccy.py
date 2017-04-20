class Ccy:
    def __init__(self, ccy):
        self.ccy = ccy

    def convert_one_to_pricing_currency(self, env, d):
        fxc = env.get_fx_forward_curve(self.ccy)
        return fxc.get_forward_fx_rate(env, d)

EUR = Ccy('EUR')
USD = Ccy('USD')