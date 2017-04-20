import unittest
from rm3d_reader import RM3DReader


class TestWriter(unittest.TestCase):
    def test_1(self):
        s = 'START-OF-FILE\nDATEFORMAT=YYYYMMDD\nFIELDSEPARATOR=TAB\nSUBFIELDSEPARATOR=PIPE\nDECIMALSEPARATOR=PERIOD\nSTART-OF-DATA\n' + \
            'cash	FXSpotPosCF:AED_SPOT4	19201693.030000	AED	Portfolio|BLB|Portfolio1|DH|Portfolio2|SPOT4|Portfolio3|cash|Portfolio4|FXSpotPosCF:AED_SPOT4|BookType|TradingBook|BLBReportLevel1|BLB|BLBReportLevel2|KB|BLBReportLevel3|KBOS|BLBReportLevel4|FM|BLBReportLevel5|GDDRH|BLBReportLevel6|DH|BLBReportLevel7|FX-SPOT|BLBReportLevel8|SPOT4|Usage|BLBeod|userbucket1|LB|TypeOfInstr|SPOT|Collateralization|false|IFRS|GuV|Nominal1|19201693.03|Currency1|AED	0				FXSpotPosCF:AED_SPOT4			\n' + \
            'END-OF-DATA\nEND-OF-FILE'

        reader = RM3DReader()
        result = reader.process(s)
        self.assertEqual(result[0][0], 'cash')
