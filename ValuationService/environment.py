from ValuationService.forwardcurve import IRForwardCurve, FXForwardCurve
from ValuationService.ccy import EUR, USD

standard_discount_curve = {
    EUR: IRForwardCurve(EUR, 'Eonia'),
    USD: IRForwardCurve(USD, 'OIS')}


# TODO: Register forward curves with env created elsewhere

class Environment:
    def __init__(self):
        self._pricing_currency = EUR
        self._forward_curves = dict()

    def set_pricing_currency(self, ccy):
        self._pricing_currency = ccy

    def get_pricing_currency(self):
        return self._pricing_currency

    def set_pricing_date(self, d):
        self.pricing_date = d

    def get_pricing_date(self):
        return self.pricing_date

    def get_discount_curve(self):
        return standard_discount_curve[self._pricing_currency]

    def get_fx_forward_curve(self, ccy):
        return FXForwardCurve(self._pricing_currency, ccy)

    def add_curve(self, index, curve):
        self._forward_curves[index] = curve

    def get_index_forward_curve(self, index):
        return self._forward_curves[index]
