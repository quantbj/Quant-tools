import unittest

modules = [ 'rm3dmanipulator' ]

if __name__ == "__main__":
    for mod in modules:
        suite = unittest.TestLoader().discover(mod)
        unittest.TextTestRunner(verbosity=2).run(suite)
