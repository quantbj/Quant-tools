from ValuationService.forwardcurve import IRForwardCurve, FXForwardCurve
from ValuationService.ccy import EUR

class Environment:
    def __init__(self, pricing_currency=EUR):
        self._pricing_currency = pricing_currency
        self._ir_forward_curves = dict()
        self._discount_curves = dict()
        self._ir_caplet_vol_surface = dict()

    def set_pricing_currency(self, ccy):
        self._pricing_currency = ccy

    def get_pricing_currency(self):
        return self._pricing_currency

    def set_pricing_date(self, d):
        self.pricing_date = d

    def get_pricing_date(self):
        return self.pricing_date

    def set_discount_curve(self, ccy, curve):
        self._discount_curves[ccy] = curve

    def get_discount_curve(self, ccy):
        return self._discount_curves[ccy]

    def get_fx_forward_curve(self, ccy):
        return FXForwardCurve(self._pricing_currency, ccy)

    def add_ir_forward_curve(self, index, curve):
        self._ir_forward_curves[index] = curve

    def get_ir_index_forward_curve(self, index):
        return self._ir_forward_curves[index]

    def add_caplet_vol_surface(self, index, volatility_surface):
        self._ir_caplet_vol_surface[index] = volatility_surface

    def get_caplet_vol_surface(self, index):
        return self._ir_caplet_vol_surface[index]

def HistVaREnvironment(Environment):
    def __init__(self, pricing_currency=EUR, historic_returns=None):
        super().__init__(pricing_currency)
        self.historic_returns = historic_returns
        
