from unittest import TestCase
from ValuationService.ir_indices import EURIBOR6M
from Utils.date_utils import ACT360

class IR_IndexTest(TestCase):
    def test_EURIBOR6M(self):
        self.assertEqual(EURIBOR6M.dcc, ACT360)
