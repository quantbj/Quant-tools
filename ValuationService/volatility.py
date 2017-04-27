from Utils.value_object import ValueObject
from scipy.interpolate import interp2d


class CapletVolSurface(ValueObject):
    def __init__(self, tenors, strikes, caplet_vols):
        pass

    def get_vol(self, tenor, strike):

        f = interp2d(
            x=self.strikes,
            y=self.tenors,
            z=self.caplet_vols,
            kind='linear',
            copy=False)

        return float(f(strike, tenor))
