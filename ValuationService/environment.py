from CurvesService.forwardcurve import IRForwardCurve, FxForwardCurve
from ValuationService.ccy import EUR, USD

standard_discount_curve = {
    EUR: IRForwardCurve(EUR, 'Eonia'),
    USD: IRForwardCurve(USD, 'OIS')}


class Environment:
    def set_pricing_currency(self, ccy):
        self.pricing_currency = ccy

    def get_pricing_currency(self):
        return self.pricing_currency

    def set_pricing_date(self, d):
        self.pricing_date = d

    def get_pricing_date(self):
        return self.pricing_date

    def get_discount_curve(self):
        return standard_discount_curve[self.pricing_currency]

    def get_fx_forward_curve(self, ccy):
        return FxForwardCurve(self.pricing_currency, ccy)
