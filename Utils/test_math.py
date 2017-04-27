from unittest import TestCase
from Utils.math import phi


class TestMath(TestCase):
    def test_phi(self):
        self.assertAlmostEqual(0, phi(-10))
        self.assertAlmostEqual(1, phi(10))
        self.assertAlmostEqual(0.5, phi(0))
