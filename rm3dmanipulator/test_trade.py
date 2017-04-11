from trade import GenericTrade
import unittest

class testGenericTrade(unittest.TestCase):

    rm3d_list_cap = \
                ['cap',	'VAL_CAP_C&F:2526:0',	'-1500000.000000',	
                 'EUR',	'EUR Swap',	'0.000001',	'',	'4',	'',	'',	'',	'20190909',	'0.000000',	'',	'',	'',	
                 'Portfolio|BLB',	'1',	'EU.EUR.ISC',	'',	'0',	'',	'',	'CapFloorDeals:2526',	
                 '',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'0',	'',	'',	'']
    rm3d_list_cashflow_str = 'cashFlow	BondsDealsFixed:XFBL00077285_KAP-NEUEM	20170710|EUR|-597579.16011678|EUR Swap|20170710|EUR|-10000000|EUR Swap	Portfolio|BLB|Portfolio1|SALES|Portfolio2|KAP-NEUEM|Portfolio3|cashFlow|Portfolio4|BondsDealsFixed:XFBL00077285_KAP-NEUEM|BookType|BankingBook|BLBReportLevel1|BLB|BLBReportLevel2|KB|BLBReportLevel3|SALES|BLBReportLevel4|SALES|BLBReportLevel5|SALES|BLBReportLevel6|SALES|BLBReportLevel7|INST|BLBReportLevel8|KAP-NEUEM|Usage|BLBeod|userbucket1|LB|InstituteInternalGenericTrade|false|TypeOfInstr|DOB|Collateralization|false|CountryID|004|IFRS|OL|Nominal1|10000000|Currency1|EUR	1				BondsDealsFixed:593	265295												1				'
    rm3d_list_cashflow = rm3d_list_cashflow_str.split('\t')

 
    def test_deserialize_serialize(self):
        t = GenericTrade(self.rm3d_list_cap)
        s = t.get_serialized()
        self.assertEqual(s[0], 'cap')
        self.assertEqual(s[7], '4')

    def test_set_ignore_fx(self):
        t = GenericTrade(self.rm3d_list_cap)
        t.set_ignore_fx('0')
        s = t.get_serialized()
        self.assertEqual(self.rm3d_list_cap[17],'1')
        self.assertEqual(s[17], '0')

    def test_set_discount_curve(self):
        t = GenericTrade(self.rm3d_list_cap)
        t.set_discount_curve('EUR OIS')
        s = t.get_serialized()
        self.assertEqual(s[26], 'EUR OIS')

    def test_set_discount_curve_cf(self):
        t = GenericTrade(self.rm3d_list_cashflow)
        t.set_discount_curve('EUR OIS')
        s = t.get_serialized()
        self.assertEqual(s[2], '20170710|EUR|-597579.16011678|EUR OIS|20170710|EUR|-10000000|EUR OIS')
