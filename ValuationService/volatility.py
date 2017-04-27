from Utils.value_object import ValueObject
from scipy.interpolate import interp2d


class CapletVolSurface():
    def __init__(self, tenors, strikes, caplet_vols):
        self.tenors = tenors
        self.strikes = strikes
        self.caplet_vols = caplet_vols
        self.f = interp2d(
            x=self.strikes,
            y=self.tenors,
            z=self.caplet_vols,
            kind='linear',
            copy=False)

    def get_vol(self, tenor, strike):

        return float(self.f(strike, tenor))
