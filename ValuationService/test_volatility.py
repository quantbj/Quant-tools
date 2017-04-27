from unittest import TestCase
from ValuationService.volatility import CapletVolSurface


class TestVol(TestCase):
    def test_caplet_vol_interp(self):
        vol_strikes = [-0.125, 0, 0.125, 0.25]
        vol_tenors = [0.5, 1, 1.5, 2]
        cvols = [[41.0, 42.0, 43.0, 44.0],
                 [45.0, 46.0, 47.0, 48.0],
                 [49.0, 50.0, 51.0, 52.0],
                 [53.0, 54.0, 55.0, 56.0]]
        caplet_surface = CapletVolSurface(
            tenors=vol_tenors,
            strikes=vol_strikes,
            caplet_vols=cvols)

        self.assertAlmostEqual(46.0,
                               caplet_surface.get_vol(tenor=1.0, strike=0))
        self.assertAlmostEqual(56.0,
                               caplet_surface.get_vol(tenor=2.0, strike=0.25))
        self.assertAlmostEqual(41.5,
                               caplet_surface.get_vol(tenor=0.5, strike=-0.125 / 2))
        self.assertAlmostEqual(((49.0 + 50.0) / 2 + (53.0 + 54.0) / 2) / 2,
                               caplet_surface.get_vol(tenor=1.75, strike=-0.125 / 2))
        self.assertAlmostEqual(44.0,
                               caplet_surface.get_vol(tenor=0.5, strike=0.5))
        self.assertAlmostEqual(56.0,
                               caplet_surface.get_vol(tenor=5, strike=0.5))
