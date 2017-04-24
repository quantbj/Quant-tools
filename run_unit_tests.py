import unittest
import sys

modules = ['rm3dmanipulator', 'ValuationService', 'Utils']

if __name__ == "__main__":
    for mod in modules:
        suite = unittest.TestLoader().discover(mod)
        result = unittest.TextTestRunner(verbosity=2).run(suite)
        if not result.wasSuccessful():
            sys.exit(not result.wasSuccessful())
