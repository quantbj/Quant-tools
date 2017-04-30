from ValuationService.cash_flow import FixedCashFlow, FloatingCashFlow, \
    PlainVanillaCapletSLN, PlainVanillaFloorletSLN
from ValuationService.ir_indices import EURIBOR6M
from ValuationService.ccy import EUR, USD
from Utils.date_utils import DatePeriod
from datetime import date
from math import log, sqrt
from Utils.math import phi
from unittest import TestCase
from unittest.mock import Mock
from numpy import array
from numpy.testing import assert_array_almost_equal


class TestFixedCashFlow(TestCase):
    def test_present_value_1(self):
        d = date(2017, 4, 19)
        dc = Mock()
        env = Mock()
        fxc = Mock()
        fxc.get_forward_fx_rate = Mock(return_value=1.0)
        env.get_fx_forward_curve = Mock(return_value=fxc)
        env.get_pricing_currency = Mock(return_value=EUR)
        dc.get_discount_factor = Mock(return_value=0.95)
        env.get_discount_curve = Mock(return_value=dc)

        fcf = FixedCashFlow(d, 100.0, EUR)
        pv = fcf.present_value(env)
        self.assertEqual(pv, 95.0)

    def test_present_value_2(self):
        d = date(2017, 4, 19)
        dc = Mock()
        env = Mock()
        fxc = Mock()
        fxc.get_forward_fx_rate = Mock(return_value=0.95)
        env.get_fx_forward_curve = Mock(return_value=fxc)
        env.get_pricing_currency = Mock(return_value=EUR)
        dc.get_discount_factor = Mock(return_value=0.85)

        fcf = FixedCashFlow(d, 100.0, USD, dc)
        pv = fcf.present_value(env)
        self.assertEqual(pv, 100 * 0.85 * 0.95)

    def test_present_value_array(self):
        d = date(2017, 4, 19)
        dc = Mock()
        env = Mock()
        fxc = Mock()
        fxc.get_forward_fx_rate = Mock(return_value=1.0)
        env.get_fx_forward_curve = Mock(return_value=fxc)
        env.get_pricing_currency = Mock(return_value=EUR)
        dc.get_discount_factor = Mock(return_value=array([0.95, 0.99]))
        env.get_discount_curve = Mock(return_value=dc)

        fcf = FixedCashFlow(d, 100.0, EUR)
        pv = fcf.present_value(env)
        assert_array_almost_equal(pv, [95.0, 99.0])
        

class TestFloatingCashFlow(TestCase):
    def test_present_value(self):
        index = 'EURIBOR06M'
        fixing_date = date(2017, 4, 22)
        forward_period = DatePeriod(date(2017, 4, 24), date(2017, 10, 24))
        pay_date = date(2017, 10, 24)
        dc = Mock()
        env = Mock()
        fxc = Mock()
        fc = Mock()
        fxc.get_forward_fx_rate = Mock(return_value=1.0)
        fc.get_forward_rate = Mock(return_value=0.01)
        env.get_fx_forward_curve = Mock(return_value=fxc)
        env.get_pricing_currency = Mock(return_value=EUR)
        env.get_pricing_date = Mock(return_value=date(2017, 4, 20))
        env.get_ir_index_forward_curve = Mock(return_value=fc)
        dc.get_discount_factor = Mock(return_value=0.95)
        env.get_discount_curve = Mock(return_value=dc)

        fcf = FloatingCashFlow(
            index,
            fixing_date,
            forward_period,
            pay_date,
            1000000,
            EUR)
        pv = fcf.present_value(env)
        self.assertAlmostEqual(pv, 0.01 * 1000000 * 183 / 360 * 0.95)

    def test_present_value_array(self):
        index = 'EURIBOR06M'
        fixing_date = date(2017, 4, 22)
        forward_period = DatePeriod(date(2017, 4, 24), date(2017, 10, 24))
        pay_date = date(2017, 10, 24)
        dc = Mock()
        env = Mock()
        fxc = Mock()
        fc = Mock()
        fxc.get_forward_fx_rate = Mock(return_value=1.0)
        fc.get_forward_rate = Mock(return_value=array([0.01, 0.02]))
        env.get_fx_forward_curve = Mock(return_value=fxc)
        env.get_pricing_currency = Mock(return_value=EUR)
        env.get_pricing_date = Mock(return_value=date(2017, 4, 20))
        env.get_ir_index_forward_curve = Mock(return_value=fc)
        dc.get_discount_factor = Mock(return_value=array([0.95, 0.99]))
        env.get_discount_curve = Mock(return_value=dc)

        fcf = FloatingCashFlow(
            index,
            fixing_date,
            forward_period,
            pay_date,
            1000000,
            EUR)
        pv = fcf.present_value(env)
        res = array([0.01 * 1000000 * 183 / 360 * 0.95, 0.02 * 1000000 * 183 / 360 * 0.99])
        assert_array_almost_equal(pv, res)
        

class TestCaplet(TestCase):

    def test_caplet_pv(self):
        index = EURIBOR6M
        fixing_date = date(2017, 10, 22)
        forward_period = DatePeriod(date(2017, 10, 24), date(2018, 4, 24))
        pay_date = date(2018, 4, 24)
        strike = 0.0
        shift = 0.03

        pricing_date = date(2017, 4, 20)
        fr = 0.01
        df = 0.95
        nominal = 1000000
        T = (forward_period.end - pricing_date).days / 360
        dcf = (forward_period.end - forward_period.start).days / 360
        sigma = 0.4

        dc = Mock()
        env = Mock()
        fxc = Mock()
        fc = Mock()
        volsurf = Mock()
        fxc.get_forward_fx_rate = Mock(return_value=1.0)
        fc.get_forward_rate = Mock(return_value=fr)
        volsurf.get_vol = Mock(return_value=sigma)
        env.get_caplet_vol_surface = Mock(return_value=volsurf)
        env.get_fx_forward_curve = Mock(return_value=fxc)
        env.get_pricing_currency = Mock(return_value=EUR)
        env.get_pricing_date = Mock(return_value=pricing_date)
        env.get_ir_index_forward_curve = Mock(return_value=fc)
        dc.get_discount_factor = Mock(return_value=df)
        env.get_discount_curve = Mock(return_value=dc)

        caplet = PlainVanillaCapletSLN(
            index=index,
            fixing_date=fixing_date,
            forward_period=forward_period,
            pay_date=pay_date,
            nominal=nominal,
            ccy=EUR,
            strike=strike,
            shift=shift)

        pv = caplet.present_value(env)

        d1 = (log((fr + shift) / (strike + shift)) +
              sigma**2 * T / 2) / (sigma * sqrt(T))
        d2 = d1 - sigma * sqrt(T)
        pv_test = dcf * df * nominal * \
            ((fr + shift) * phi(d1) - (strike + shift) * phi(d2))

        self.assertAlmostEqual(pv_test, pv)

    def test_floorlet_pv(self):
        index = EURIBOR6M
        fixing_date = date(2017, 10, 22)
        forward_period = DatePeriod(date(2017, 10, 24), date(2018, 4, 24))
        pay_date = date(2018, 4, 24)
        strike = 0.0
        shift = 0.03

        pricing_date = date(2017, 4, 20)
        fr = 0.01
        df = 0.95
        nominal = 1000000
        T = (forward_period.end - pricing_date).days / 360
        dcf = (forward_period.end - forward_period.start).days / 360
        sigma = 0.4

        dc = Mock()
        env = Mock()
        fxc = Mock()
        fc = Mock()
        volsurf = Mock()
        fxc.get_forward_fx_rate = Mock(return_value=1.0)
        fc.get_forward_rate = Mock(return_value=fr)
        volsurf.get_vol = Mock(return_value=sigma)
        env.get_caplet_vol_surface = Mock(return_value=volsurf)
        env.get_fx_forward_curve = Mock(return_value=fxc)
        env.get_pricing_currency = Mock(return_value=EUR)
        env.get_pricing_date = Mock(return_value=pricing_date)
        env.get_ir_index_forward_curve = Mock(return_value=fc)
        dc.get_discount_factor = Mock(return_value=df)
        env.get_discount_curve = Mock(return_value=dc)

        floorlet = PlainVanillaFloorletSLN(
            index=index,
            fixing_date=fixing_date,
            forward_period=forward_period,
            pay_date=pay_date,
            nominal=nominal,
            ccy=EUR,
            strike=strike,
            shift=shift)

        pv = floorlet.present_value(env)

        d1 = (log((fr + shift) / (strike + shift)) +
              sigma**2 * T / 2) / (sigma * sqrt(T))
        d2 = d1 - sigma * sqrt(T)
        pv_test = dcf * df * nominal * \
            (-(fr + shift) * phi(-d1) + (strike + shift) * phi(-d2))

        self.assertAlmostEqual(pv_test, pv)

    def test_caplet_array(self):
        index = EURIBOR6M
        fixing_date = date(2017, 10, 22)
        forward_period = DatePeriod(date(2017, 10, 24), date(2018, 4, 24))
        pay_date = date(2018, 4, 24)
        strike = 0.0
        shift = 0.03

        pricing_date = date(2017, 4, 20)
        fr1 = 0.01
        fr2 = 0.02
        df1 = 0.95
        df2 = 0.9
        nominal = 1000000
        T = (forward_period.end - pricing_date).days / 360
        dcf = (forward_period.end - forward_period.start).days / 360
        sigma = 0.4

        dc = Mock()
        env = Mock()
        fxc = Mock()
        fc = Mock()
        volsurf = Mock()
        fxc.get_forward_fx_rate = Mock(return_value=1.0)
        fc.get_forward_rate = Mock(return_value=array([fr1,fr2]))
        volsurf.get_vol = Mock(return_value=sigma)
        env.get_caplet_vol_surface = Mock(return_value=volsurf)
        env.get_fx_forward_curve = Mock(return_value=fxc)
        env.get_pricing_currency = Mock(return_value=EUR)
        env.get_pricing_date = Mock(return_value=pricing_date)
        env.get_ir_index_forward_curve = Mock(return_value=fc)
        dc.get_discount_factor = Mock(return_value=array([df1,df2]))
        env.get_discount_curve = Mock(return_value=dc)

        caplet = PlainVanillaCapletSLN(
            index=index,
            fixing_date=fixing_date,
            forward_period=forward_period,
            pay_date=pay_date,
            nominal=nominal,
            ccy=EUR,
            strike=strike,
            shift=shift)

        pv = caplet.present_value(env)

        d1_1 = (log((fr1 + shift) / (strike + shift)) +
              sigma**2 * T / 2) / (sigma * sqrt(T))
        d2_1 = d1_1 - sigma * sqrt(T)
        d1_2 = (log((fr2 + shift) / (strike + shift)) +
              sigma**2 * T / 2) / (sigma * sqrt(T))
        d2_2 = d1_2 - sigma * sqrt(T)
        pv_test1 = dcf * df1 * nominal * \
            ((fr1 + shift) * phi(d1_1) - (strike + shift) * phi(d2_1))
        pv_test2 = dcf * df2 * nominal * \
            ((fr2 + shift) * phi(d1_2) - (strike + shift) * phi(d2_2))

        assert_array_almost_equal(array([pv_test1, pv_test2]), pv)
