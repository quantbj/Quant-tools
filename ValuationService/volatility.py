from Utils.value_object import ValueObject
from scipy.interpolate import interp2d


class CapletVolSurface(ValueObject):
    def __init__(self, tenors, strikes, caplet_vols, f=None):
        self._f = f if f else interp2d(
            x=self.strikes,
            y=self.tenors,
            z=self.caplet_vols,
            kind='linear',
            copy=False)

    def get_vol(self, tenor, strike):

        return float(self._f(strike, tenor))
