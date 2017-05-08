from Utils.correlation import CKey
from unittest import TestCase

class TestCKey(TestCase):
    def test_eq(self):
        a = 1
        b = 2
        c = 3
        k1 = CKey(a,b)
        k2 = CKey(b,a)
        k3 = CKey(a,c)
        
        self.assertEqual(k1,k2)
        self.assertNotEqual(k1,k3)        
