from decimal import Decimal

from django.test import TestCase
from django.contrib.auth.models import User
from calc.models import PlantProfile


class TestWithK(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='12345')
        # login = self.client.login(username='testuser', password='12345')
        fields = {"name": "for_test.hpg", "user": self.user, "ec": "0.000", "ppm": "0.000", "calc_mode": "K",
                  "n": "220.000",
                  "no3": "200.000", "nh4": "20.000", "p": "40.000", "k": "180.000", "ca": "200.000", "mg": "50.000",
                  "s": "68.527", "cl": "10.000", "fe": "6000.000", "mn": "550.000", "b": "500.000", "zn": "60.000",
                  "cu": "60.000", "mo": "60.000", "co": "50.000", "si": "0.000", "cano3_ca": "16.972",
                  "cano3_no3": "11.863", "cano3_nh4": "0.000", "kno3_k": "38.672", "kno3_no3": "13.854",
                  "nh4no3_nh4": "17.499", "nh4no3_no3": "17.499", "mgso4_mg": "9.861", "mgso4_s": "13.010",
                  "kh2po4_k": "28.731", "kh2po4_p": "22.761", "k2so4_k": "44.874", "k2so4_s": "18.401",
                  "mgno3_mg": "9.483", "mgno3_no3": "10.930", "cacl2_ca": "18.294", "cacl2_cl": "32.366"}
        pp = PlantProfile(**fields)
        pp.save()
        self.profile = pp
    
    def tearDown(self):
        # Очистка после каждого метода
        pass
    
    def test_calc_s(self):
        print(self.profile.calc_s())
    
    def test_kh2po4(self):
        self.assertTrue(round(self.profile.kh2po4(), 5) == Decimal('1.75739'))
    
    def test_kno3(self):
        self.assertTrue(round(self.profile.kno3(), 5) == Decimal('3.18745'))
    
    def test_cano3(self):
        self.assertTrue(round(self.profile.cano3(), 5) == Decimal('11.45108'))
    
    def test_mgso4(self):
        self.assertTrue(round(self.profile.mgso4(), 5) == Decimal('5.07048'))
    
    def test_k2so4(self):
        self.assertTrue(round(self.profile.k2so4(), 5) == Decimal('0.13913'))
    
    def test_nh4no3(self):
        self.assertTrue(round(self.profile.nh4no3(), 5) == Decimal('1.14292'))
    
    def test_cacl2(self):
        self.assertTrue(round(self.profile.cacl2(), 5) == Decimal('0.30897'))


class TestWithMg(TestCase):
    
    def setUp(self):
     
        self.user = User.objects.create_user(username='test_user', password='12345')
        # login = self.client.login(username='testuser', password='12345')
        fields = {"name": "for_test.hpg", "user": self.user, "ec": "0.000", "ppm": "0.000",
                  "calc_mode": "Mg",
                  "n": "0.000",
                  "no3": "204.610", "nh4": "17.500", "p": "22.760", "k": "67.400", "ca": "242.900", "mg": "57.260",
                  "s": "13.018", "cl": "129.460", "fe": "6000.000", "mn": "550.000", "b": "500.000", "zn": "60.000",
                  "cu": "60.000", "mo": "60.000", "co": "50.000", "si": "0.000", "cano3_ca": "16.972",
                  "cano3_no3": "11.863", "cano3_nh4": "0.000", "kno3_k": "38.672", "kno3_no3": "13.854",
                  "nh4no3_nh4": "17.499", "nh4no3_no3": "17.499", "mgso4_mg": "9.861", "mgso4_s": "13.010",
                  "kh2po4_k": "28.731", "kh2po4_p": "22.761", "k2so4_k": "44.874", "k2so4_s": "18.401",
                  "mgno3_mg": "9.483", "mgno3_no3": "10.930", "cacl2_ca": "18.294", "cacl2_cl": "32.366"}
        pp = PlantProfile(**fields)
        pp.save()
        self.profile = pp
    
    def tearDown(self):
        # Очистка после каждого метода
        pass
    
    def test_calc_s(self):
        print(self.profile.calc_s())
        
    def test_kh2po4(self):
        self.assertTrue(round(self.profile.kh2po4(), 5) == Decimal('0.99996'))
    
    def test_kno3(self):
        self.assertTrue(round(self.profile.kno3(), 5) == Decimal('0.99996'))
    
    def test_cano3(self):
        self.assertTrue(round(self.profile.cano3(), 5) == Decimal('10.00037'))
    
    def test_mgso4(self):
        self.assertTrue(round(self.profile.mgso4(), 5) == Decimal('1.00061'))
    
    def test_nh4no3(self):
        self.assertTrue(round(self.profile.nh4no3(), 5) == Decimal('1.00006'))
    
    def test_cacl2(self):
        self.assertTrue(round(self.profile.cacl2(), 5) == Decimal('3.99988'))
    
    def test_mgno3(self):
        self.assertTrue(round(self.profile.mgno3(), 5) == Decimal('4.99767'))


class TestMatrix(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='12345')
        # login = self.client.login(username='testuser', password='12345')
        fields = {"name": "for_test.hpg", "user": self.user, "ec": "0.000", "ppm": "0.000", "calc_mode": "K",
                  "n": "220.000",
                  "no3": "200.000", "nh4": "20.000", "p": "40.000", "k": "180.000", "ca": "200.000", "mg": "50.000",
                  "s": "68.527", "cl": "10.000", "fe": "6000.000", "mn": "550.000", "b": "500.000", "zn": "60.000",
                  "cu": "60.000", "mo": "60.000", "co": "50.000", "si": "0.000", "cano3_ca": "16.972",
                  "cano3_no3": "11.863", "cano3_nh4": "0.000", "kno3_k": "38.672", "kno3_no3": "13.854",
                  "nh4no3_nh4": "17.499", "nh4no3_no3": "17.499", "mgso4_mg": "9.861", "mgso4_s": "13.010",
                  "kh2po4_k": "28.731", "kh2po4_p": "22.761", "k2so4_k": "44.874", "k2so4_s": "18.401",
                  "mgno3_mg": "9.483", "mgno3_no3": "10.930", "cacl2_ca": "18.294", "cacl2_cl": "32.366"}
        pp = PlantProfile(**fields)
        pp.save()
        self.profile = pp
    
    def tearDown(self):
        # Очистка после каждого метода
        pass
    
    def test_calc_s(self):
        pushed_element = 'matrix-n-p'
        a = Decimal(self.profile.n)
        b = Decimal(self.profile.p)
        t_old = a / b
        t_new = Decimal('6')
        c = a/t_new
   
        print(
            'old a', "{:.2f}".format(a),
            'old b', "{:.2f}".format(b),
            't_old', "{:.2f}".format(t_old),
            't_new', "{:.2f}".format(t_new),
    
            'a/c', "{:.2f}".format(a/c),
            'c', "{:.2f}".format(c),
            
    
        )
  