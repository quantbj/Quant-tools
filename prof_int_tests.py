import unittest
import cProfile

suite = unittest.TestLoader().discover('IntegrationTests')
cProfile.run('unittest.TextTestRunner(verbosity=2).run(suite)')
