from decimal import Decimal

from django.test import TestCase
from django.contrib.auth.models import User
from calc.models import PlantProfile
import  pprint
pp = pprint.PrettyPrinter(indent=2, sort_dicts=False)
def print_macro(self):
    tt ={'persents':{}}
    for i in self.profile.macro:
        tt[i] = round(getattr(self.profile, i), 3)
    
    for k, i in self.profile.salt_gramms.items():
        tt[k] = round(getattr(self.profile, i)(),3 )
        
    for i in self.profile.salt:
        tt['persents'][i] = round(getattr(self.profile, i), 3)
    pp.pprint(  tt)


def print_micro(self):
    tt = {'persents': {}}
    
    for i in self.profile.micro:
        tt[i] = round(getattr(self.profile, i), 3)
    
    for i in self.profile.salt_micro_gramm:
        tt[i] = round(getattr(self.profile, i), 3)

    for i in self.profile.salt_micro_persent:
        tt['persents'][i] = round(getattr(self.profile, i), 3)
    
    # for i in self.profile.salt_micro_persent_bor:
    #     tt['persents'][i] = round(getattr(self.profile, i), 3)
    
    pp.pprint(tt)

   

class TestWithK(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='12345')
        # login = self.client.login(username='testuser', password='12345')
        fields =  {'name': 'for_test.hpg', 'n': '220.00', 'nh4': '20.00', 'no3': '200.00', 'p': '40.00', 'k': '180.00', 'ca': '200.00', 'mg': '50.00', 's': '68.53', 'cl': '10.00', 'cano3_ca': '16.97', 'cano3_no3': '11.86', 'cano3_nh4': '0.00', 'kno3_k': '38.67', 'kno3_no3': '13.85', 'nh4no3_nh4': '17.50', 'nh4no3_no3': '17.50', 'mgso4_mg': '9.86', 'mgso4_s': '13.01', 'kh2po4_k': '28.73', 'kh2po4_p': '22.76', 'k2so4_k': '44.87', 'k2so4_s': '18.40', 'mgno3_mg': '9.48', 'mgno3_no3': '10.93', 'cacl2_ca': '18.29', 'cacl2_cl': '32.37', 'fe': '6000.00', 'mn': '550.00', 'b': '500.00', 'zn': '60.00', 'cu': '60.00', 'mo': '60.00', 'co': '50.00', 'si': '0.00', 'dfe': '11.00', 'dmn': '32.50', 'db': '17.50', 'dzn': '22.70', 'dcu': '25.50', 'dmo': '54.30', 'dco': '13.00', 'dsi': '7.00', 'gl_cano3': '600.00', 'gl_kno3': '250.00', 'gl_nh4no3': '100.00', 'gl_mgno3': '500.00', 'gl_mgso4': '600.00', 'gl_k2so4': '100.00', 'gl_kh2po4': '150.00', 'gl_cacl2': '100.00', 'gl_cmplx': '10.00', 'gl_fe': '10.00', 'gl_mn': '10.00', 'gl_b': '10.00', 'gl_zn': '10.00', 'gl_cu': '10.00', 'gl_mo': '10.00', 'gl_co': '10.00', 'gl_si': '10.00', 'gml_cano3': '1.28', 'gml_kno3': '1.00', 'gml_nh4no3': '1.00', 'gml_mgno3': '1.00', 'gml_mgso4': '1.00', 'gml_k2so4': '1.00', 'gml_kh2po4': '1.00', 'gml_cacl2': '1.00', 'gml_cmplx': '1.00', 'gml_fe': '1.00', 'gml_mn': '1.00', 'gml_b': '1.00', 'gml_zn': '1.00', 'gml_cu': '1.00', 'gml_mo': '1.00', 'gml_co': '1.00', 'gml_si': '1.00', 'micro_calc_mode': 'u', 'calc_mode': 'K', 'litres': '10.00', 'taml': '1000.00', 'tbml': '1000.00', 'ec': 0, 'ppm': 0, 'user_id': 1}
        pp = PlantProfile(**fields)
        pp.save()
        self.profile = PlantProfile.objects.get(pk=pp.pk)
        self.old_profile = PlantProfile.objects.get(pk=pp.pk)
        self.profile.ec = self.profile.calc_ec()

    def tearDown(self):
        # Очистка после каждого метода
        self.profile = PlantProfile.objects.get(pk=self.profile.pk)
        self.profile.ec = self.profile.calc_ec()
    
    def test_calc_s(self):
        print(self.profile.calc_s())
    
    def test_kh2po4(self):
        t = round(self.profile.calc_kh2po4(), 5)
        self.assertTrue(t == 1.75747)
    
    def test_kno3(self):
        t = round(self.profile.calc_kno3(), 5)
        self.assertTrue( t == 3.18785)
    
    def test_salt_cano3(self):
        t = round(self.profile.calc_cano3(), 5)
        print(f'test_cano3 {t}')
        self.assertTrue(t  == 11.4528)
    
    def test_mgso4(self):
        t = round(self.profile.calc_mgso4(), 5)
        self.assertTrue(t  == 5.07099)
    
    def test_k2so4(self):
        t = round(self.profile.calc_k2so4(), 5)
        self.assertTrue( t == 0.13893)
    
    def test_nh4no3(self):
        t = round(self.profile.calc_nh4no3(), 5)
        self.assertTrue(t ==  1.14286)
    
    def test_cacl2(self):
        t = round(self.profile.calc_cacl2(), 5)
        self.assertTrue( t  == 0.30893 )
        
    def test_calc_change_n(self):
        self.profile.n=250
        self.profile.calc_macro(pushed_element='n', val=250)
        print_macro(self)
        tt =  { 'persents': { 'cano3_ca': 16.97,
                'cano3_no3': 11.86,
                'cano3_nh4': 0.0,
                'kno3_k': 38.67,
                'kno3_no3': 13.85,
                'nh4no3_nh4': 17.5,
                'nh4no3_no3': 17.5,
                'mgso4_mg': 9.86,
                'mgso4_s': 13.01,
                'kh2po4_k': 28.73,
                'kh2po4_p': 22.76,
                'k2so4_k': 44.87,
                'k2so4_s': 18.4,
                'mgno3_mg': 9.48,
                'mgno3_no3': 10.93,
                'cacl2_ca': 18.29,
                'cacl2_cl': 32.37},
  'n': 250,
  'no3': 227.273,
  'nh4': 22.727,
  'p': 40.0,
  'k': 180.0,
  'ca': 200.004,
  'mg': 50.0,
  's': 40.435,
  'cl': 10.0,
  'cano3': 11.453,
  'kno3': 4.96,
  'nh4no3': 1.299,
  'mgso4': 5.071,
  'kh2po4': 1.757,
  'k2so4': -1.388,
  'mgno3': 0,
  'cacl2': 0.309}


        for i in self.profile.macro:
            self.assertTrue(
                tt[i] ==  round(getattr(self.profile, i), 3)
            )

        for k, i in self.profile.salt_gramms.items():
            self.assertTrue(
                tt[k] == round(getattr(self.profile, i)(), 3)
            )
    def test_calc_change_p(self):
        pushed_elemet = 'p'
        val = 30
        setattr(self.profile, pushed_elemet, val)
        self.profile.calc_macro(pushed_element=pushed_elemet, val=val)
    
        print_macro(self)
        tt =  { 'persents': { 'cano3_ca': 16.97,
                'cano3_no3': 11.86,
                'cano3_nh4': 0.0,
                'kno3_k': 38.67,
                'kno3_no3': 13.85,
                'nh4no3_nh4': 17.5,
                'nh4no3_no3': 17.5,
                'mgso4_mg': 9.86,
                'mgso4_s': 13.01,
                'kh2po4_k': 28.73,
                'kh2po4_p': 22.76,
                'k2so4_k': 44.87,
                'k2so4_s': 18.4,
                'mgno3_mg': 9.48,
                'mgno3_no3': 10.93,
                'cacl2_ca': 18.29,
                'cacl2_cl': 32.37},
  'n': 220.0,
  'no3': 200.0,
  'nh4': 20.0,
  'p': 30,
  'k': 180.0,
  'ca': 200.004,
  'mg': 50.0,
  's': 73.706,
  'cl': 10.0,
  'cano3': 11.453,
  'kno3': 3.188,
  'nh4no3': 1.143,
  'mgso4': 5.071,
  'kh2po4': 1.318,
  'k2so4': 0.42,
  'mgno3': 0,
  'cacl2': 0.309}

        for i in self.profile.macro:
            self.assertTrue(
                tt[i] ==  round(getattr(self.profile, i), 3)
            )
            

        for k, i in self.profile.salt_gramms.items():
            self.assertTrue(
                tt[k] == round(getattr(self.profile, i)(), 3)
            )
    def test_calc_change_k(self):
        pushed_elemet = 'k'
        val = 200
        setattr(self.profile, pushed_elemet, val)
        self.profile.calc_macro(pushed_element=pushed_elemet, val=val)
        print_macro(self)
        
        tt =  { 'persents': { 'cano3_ca': 16.97,
                'cano3_no3': 11.86,
                'cano3_nh4': 0.0,
                'kno3_k': 38.67,
                'kno3_no3': 13.85,
                'nh4no3_nh4': 17.5,
                'nh4no3_no3': 17.5,
                'mgso4_mg': 9.86,
                'mgso4_s': 13.01,
                'kh2po4_k': 28.73,
                'kh2po4_p': 22.76,
                'k2so4_k': 44.87,
                'k2so4_s': 18.4,
                'mgno3_mg': 9.48,
                'mgno3_no3': 10.93,
                'cacl2_ca': 18.29,
                'cacl2_cl': 32.37},
  'n': 220.0,
  'no3': 200.0,
  'nh4': 20.0,
  'p': 40.0,
  'k': 200,
  'ca': 200.004,
  'mg': 50.0,
  's': 76.731,
  'cl': 10.0,
  'cano3': 11.453,
  'kno3': 3.188,
  'nh4no3': 1.143,
  'mgso4': 5.071,
  'kh2po4': 1.757,
  'k2so4': 0.585,
  'mgno3': 0,
  'cacl2': 0.309}

        for i in self.profile.macro:
            self.assertTrue(
                tt[i] ==  round(getattr(self.profile, i), 3)
            )
            
        for k, i in self.profile.salt_gramms.items():
            self.assertTrue(
                tt[k] == round(getattr(self.profile, i)(), 3)
            )
    def test_calc_change_ca(self):
        pushed_elemet = 'ca'
        val = 180
        setattr(self.profile, pushed_elemet, val)
        self.profile.calc_macro(pushed_element=pushed_elemet, val=val)
        # print_macro(self)
        tt =  {   'n': 220.0,
                'no3': 200.0,
                'nh4': 20.0,
                'p': 40.0,
                'k': 180.0,
                'ca': 180,
                'mg': 50.0,
                's': 52.525,
                'cl': 10.0,
                'cano3': 10.274,
                'kno3': 4.197,
                'nh4no3': 1.143,
                'mgso4': 5.071,
                'kh2po4': 1.757,
                'k2so4': -0.731,
                'mgno3': 0,
                'cacl2': 0.309}

        for i in self.profile.macro:
            self.assertTrue(
                tt[i] ==  round(getattr(self.profile, i), 3)
            )
            

        for k, i in self.profile.salt_gramms.items():
            self.assertTrue(
                tt[k] == round(getattr(self.profile, i)(), 3)
            )
    def test_calc_change_mg(self):
        pushed_elemet = 'mg'
        val = 40
        setattr(self.profile, pushed_elemet, val)
        self.profile.calc_macro(pushed_element=pushed_elemet, val=val)
        print_macro(self)
        tt =  { 'persents': { 'cano3_ca': 16.97,
                'cano3_no3': 11.86,
                'cano3_nh4': 0.0,
                'kno3_k': 38.67,
                'kno3_no3': 13.85,
                'nh4no3_nh4': 17.5,
                'nh4no3_no3': 17.5,
                'mgso4_mg': 9.86,
                'mgso4_s': 13.01,
                'kh2po4_k': 28.73,
                'kh2po4_p': 22.76,
                'k2so4_k': 44.87,
                'k2so4_s': 18.4,
                'mgno3_mg': 9.48,
                'mgno3_no3': 10.93,
                'cacl2_ca': 18.29,
                'cacl2_cl': 32.37},
  'n': 220.0,
  'no3': 200.0,
  'nh4': 20.0,
  'p': 40.0,
  'k': 180.0,
  'ca': 200.004,
  'mg': 40,
  's': 55.337,
  'cl': 10.0,
  'cano3': 11.453,
  'kno3': 3.188,
  'nh4no3': 1.143,
  'mgso4': 4.057,
  'kh2po4': 1.757,
  'k2so4': 0.139,
  'mgno3': 0,
  'cacl2': 0.309}

        for i in self.profile.macro:
            self.assertTrue(
                tt[i] ==  round(getattr(self.profile, i), 3)
            )
            

        for k, i in self.profile.salt_gramms.items():
            self.assertTrue(
                tt[k] == round(getattr(self.profile, i)(), 3)
            )
    def test_calc_change_s(self):
        pushed_elemet = 's'
        val = 40
        setattr(self.profile, pushed_elemet, val)
        self.profile.calc_macro(pushed_element=pushed_elemet, val=val)
        # print_macro(self)
        tt = {   'n': 220.0,
                'no3': 200.0,
                'nh4': 20.0,
                'p': 40.0,
                'k': 180.0,
                'ca': 164.345,
                'mg': 50.0,
                's': 40.0,
                'cl': 10.0,
                'cano3': 9.351,
                'kno3': 4.987,
                'nh4no3': 1.143,
                'mgso4': 5.071,
                'kh2po4': 1.757,
                'k2so4': -1.412,
                'mgno3': 0,
                'cacl2': 0.309}

        for i in self.profile.macro:
            self.assertTrue(
                tt[i] ==  round(getattr(self.profile, i), 3)
            )
            

        for k, i in self.profile.salt_gramms.items():
            self.assertTrue(
                tt[k] == round(getattr(self.profile, i)(), 3)
            )
    def test_calc_change_cl(self):
        pushed_elemet = 'cl'
        val = 15
        setattr(self.profile, pushed_elemet, val)
        self.profile.calc_macro(pushed_element=pushed_elemet, val=val)
        print_macro(self)
        tt = {   'n': 220.0,
                'no3': 200.0,
                'nh4': 20.0,
                'p': 40.0,
                'k': 180.0,
                'ca': 200.004,
                'mg': 50.0,
                's': 66.269,
                'cl': 15,
                'cano3': 11.286,
                'kno3': 3.33,
                'nh4no3': 1.143,
                'mgso4': 5.071,
                'kh2po4': 1.757,
                'k2so4': 0.016,
                'mgno3': 0,
                'cacl2': 0.463}


        for i in self.profile.macro:
            self.assertTrue(
                tt[i] ==  round(getattr(self.profile, i), 3)
            )
            

        for k, i in self.profile.salt_gramms.items():
            self.assertTrue(
                tt[k] == round(getattr(self.profile, i)(), 3)
            )
    def test_calc_change_no3(self):
        pushed_elemet = 'no3'
        val = 210
        setattr(self.profile, pushed_elemet, val)
        self.profile.calc_macro(pushed_element=pushed_elemet, val=val)
        print_macro(self)
        tt = { 'persents': { 'cano3_ca': 16.97,
                'cano3_no3': 11.86,
                'cano3_nh4': 0.0,
                'kno3_k': 38.67,
                'kno3_no3': 13.85,
                'nh4no3_nh4': 17.5,
                'nh4no3_no3': 17.5,
                'mgso4_mg': 9.86,
                'mgso4_s': 13.01,
                'kh2po4_k': 28.73,
                'kh2po4_p': 22.76,
                'k2so4_k': 44.87,
                'k2so4_s': 18.4,
                'mgno3_mg': 9.48,
                'mgno3_no3': 10.93,
                'cacl2_ca': 18.29,
                'cacl2_cl': 32.37},
  'n': 220.0,
  'no3': 210,
  'nh4': 10.0,
  'p': 40.0,
  'k': 180.0,
  'ca': 200.004,
  'mg': 50.0,
  's': 45.637,
  'cl': 10.0,
  'cano3': 11.453,
  'kno3': 4.631,
  'nh4no3': 0.571,
  'mgso4': 5.071,
  'kh2po4': 1.757,
  'k2so4': -1.105,
  'mgno3': 0,
  'cacl2': 0.309}



        for i in self.profile.macro:
            self.assertTrue(
                tt[i] ==  round(getattr(self.profile, i), 3)
            )
            

        for k, i in self.profile.salt_gramms.items():
            self.assertTrue(
                tt[k] == round(getattr(self.profile, i)(), 3)
            )

    def test_calc_change_nh4(self):
        pushed_elemet = 'nh4'
        val = 50
        setattr(self.profile, pushed_elemet, val)
        self.profile.calc_macro(pushed_element=pushed_elemet, val=val)
        print_macro(self)
        tt = { 'persents': { 'cano3_ca': 16.97,
                'cano3_no3': 11.86,
                'cano3_nh4': 0.0,
                'kno3_k': 38.67,
                'kno3_no3': 13.85,
                'nh4no3_nh4': 17.5,
                'nh4no3_no3': 17.5,
                'mgso4_mg': 9.86,
                'mgso4_s': 13.01,
                'kh2po4_k': 28.73,
                'kh2po4_p': 22.76,
                'k2so4_k': 44.87,
                'k2so4_s': 18.4,
                'mgno3_mg': 9.48,
                'mgno3_no3': 10.93,
                'cacl2_ca': 18.29,
                'cacl2_cl': 32.37},
  'n': 220.0,
  'no3': 170.0,
  'nh4': 50,
  'p': 40.0,
  'k': 180.0,
  'ca': 200.004,
  'mg': 50.0,
  's': 137.208,
  'cl': 10.0,
  'cano3': 11.453,
  'kno3': -1.143,
  'nh4no3': 2.857,
  'mgso4': 5.071,
  'kh2po4': 1.757,
  'k2so4': 3.871,
  'mgno3': 0,
  'cacl2': 0.309}



        for i in self.profile.macro:
            self.assertTrue(
                tt[i] ==  round(getattr(self.profile, i), 3)
            )
            

        for k, i in self.profile.salt_gramms.items():
            self.assertTrue(
                tt[k] == round(getattr(self.profile, i)(), 3)
            )
    def test_calc_change_nh4_no3_ratio(self):
        pushed_elemet = 'nh4_nh3_ratio'
        val = 0.5
        setattr(self.profile, pushed_elemet, val)
        self.profile.ec = self.profile.calc_ec()
        self.profile.calc_macro(pushed_element=pushed_elemet, val=val)
        print_macro(self)
        tt = { 'persents': { 'cano3_ca': 16.97,
                'cano3_no3': 11.86,
                'cano3_nh4': 0.0,
                'kno3_k': 38.67,
                'kno3_no3': 13.85,
                'nh4no3_nh4': 17.5,
                'nh4no3_no3': 17.5,
                'mgso4_mg': 9.86,
                'mgso4_s': 13.01,
                'kh2po4_k': 28.73,
                'kh2po4_p': 22.76,
                'k2so4_k': 44.87,
                'k2so4_s': 18.4,
                'mgno3_mg': 9.48,
                'mgno3_no3': 10.93,
                'cacl2_ca': 18.29,
                'cacl2_cl': 32.37},
  'n': 185.001,
  'no3': 123.334,
  'nh4': 61.667,
  'p': 40.0,
  'k': 151.364,
  'ca': 168.186,
  'mg': 42.046,
  's': 156.285,
  'cl': 10.0,
  'cano3': 9.578,
  'kno3': -3.748,
  'nh4no3': 3.524,
  'mgso4': 4.264,
  'kh2po4': 1.757,
  'k2so4': 5.479,
  'mgno3': 0,
  'cacl2': 0.309}
        for i in self.profile.macro:
            self.assertTrue(
                tt[i] ==  round(getattr(self.profile, i), 3)
            )
            
        for k, i in self.profile.salt_gramms.items():
            self.assertTrue(
                tt[k] == round(getattr(self.profile, i)(), 3)
            )

    def test_calc_ch_matrix_n_p(self):
        pushed_elemet = 'matrix-n-p'
        val = 4
        # val = 3
       
        setattr(self.profile, pushed_elemet, val)
        self.profile.calc_macro(pushed_element=pushed_elemet, val=val)
        print_macro(self)
        tt = { 'persents': { 'cano3_ca': 16.97,
                'cano3_no3': 11.86,
                'cano3_nh4': 0.0,
                'kno3_k': 38.67,
                'kno3_no3': 13.85,
                'nh4no3_nh4': 17.5,
                'nh4no3_no3': 17.5,
                'mgso4_mg': 9.86,
                'mgso4_s': 13.01,
                'kh2po4_k': 28.73,
                'kh2po4_p': 22.76,
                'k2so4_k': 44.87,
                'k2so4_s': 18.4,
                'mgno3_mg': 9.48,
                'mgno3_no3': 10.93,
                'cacl2_ca': 18.29,
                'cacl2_cl': 32.37},
  'n': 163.155,
  'no3': 148.323,
  'nh4': 14.832,
  'p': 40.0,
  'k': 183.549,
  'ca': 203.948,
  'mg': 50.986,
  's': 127.678,
  'cl': 10.0,
  'cano3': 11.685,
  'kno3': -0.368,
  'nh4no3': 0.848,
  'mgso4': 5.171,
  'kh2po4': 1.757,
  'k2so4': 3.283,
  'mgno3': 0,
  'cacl2': 0.309}
    
        for i in self.profile.macro:
            self.assertTrue(
                tt[i] == round(getattr(self.profile, i), 3)
            )
    
        for k, i in self.profile.salt_gramms.items():
            self.assertTrue(
                tt[k] == round(getattr(self.profile, i)(), 3)
            )
    def test_calc_ch_matrix_n_k(self):
        pushed_elemet = 'matrix-n-k'
        val = 1
       
        setattr(self.profile, pushed_elemet, val)
        self.profile.calc_macro(pushed_element=pushed_elemet, val=val)
        print_macro(self)
        tt = { 'persents': { 'cano3_ca': 16.97,
                'cano3_no3': 11.86,
                'cano3_nh4': 0.0,
                'kno3_k': 38.67,
                'kno3_no3': 13.85,
                'nh4no3_nh4': 17.5,
                'nh4no3_no3': 17.5,
                'mgso4_mg': 9.86,
                'mgso4_s': 13.01,
                'kh2po4_k': 28.73,
                'kh2po4_p': 22.76,
                'k2so4_k': 44.87,
                'k2so4_s': 18.4,
                'mgno3_mg': 9.48,
                'mgno3_no3': 10.93,
                'cacl2_ca': 18.29,
                'cacl2_cl': 32.37},
  'n': 182.35,
  'no3': 165.773,
  'nh4': 16.577,
  'p': 40.0,
  'k': 182.35,
  'ca': 202.616,
  'mg': 50.653,
  's': 107.704,
  'cl': 10.0,
  'cano3': 11.607,
  'kno3': 0.833,
  'nh4no3': 0.947,
  'mgso4': 5.137,
  'kh2po4': 1.757,
  'k2so4': 2.221,
  'mgno3': 0,
  'cacl2': 0.309}
    
        for i in self.profile.macro:
            self.assertTrue(
                tt[i] == round(getattr(self.profile, i), 3)
            )
    
        for k, i in self.profile.salt_gramms.items():
            self.assertTrue(
                tt[k] == round(getattr(self.profile, i)(), 3)
            )
    def test_calc_ch_matrix_n_ca(self):
        pushed_elemet = 'matrix-n-ca'
        val = 2.1
    
        setattr(self.profile, pushed_elemet, val)
        self.profile.calc_macro(pushed_element=pushed_elemet, val=val)
        print_macro(self)
        tt = { 'persents': { 'cano3_ca': 16.97,
                'cano3_no3': 11.86,
                'cano3_nh4': 0.0,
                'kno3_k': 38.67,
                'kno3_no3': 13.85,
                'nh4no3_nh4': 17.5,
                'nh4no3_no3': 17.5,
                'mgso4_mg': 9.86,
                'mgso4_s': 13.01,
                'kh2po4_k': 28.73,
                'kh2po4_p': 22.76,
                'k2so4_k': 44.87,
                'k2so4_s': 18.4,
                'mgno3_mg': 9.48,
                'mgno3_no3': 10.93,
                'cacl2_ca': 18.29,
                'cacl2_cl': 32.37},
  'n': 394.556,
  'no3': 358.688,
  'nh4': 35.869,
  'p': 40.0,
  'k': 169.092,
  'ca': 187.884,
  'mg': 46.97,
  's': -113.112,
  'cl': 10.0,
  'cano3': 10.739,
  'kno3': 14.108,
  'nh4no3': 2.05,
  'mgso4': 4.764,
  'kh2po4': 1.757,
  'k2so4': -9.516,
  'mgno3': 0,
  'cacl2': 0.309}
    
        for i in self.profile.macro:
            self.assertTrue(
                tt[i] == round(getattr(self.profile, i), 3)
            )
    
        for k, i in self.profile.salt_gramms.items():
            self.assertTrue(
                tt[k] == round(getattr(self.profile, i)(), 3)
            )
    def test_calc_ch_matrix_n_mg(self):
        pushed_elemet = 'matrix-n-mg'
        val = 1
    
        setattr(self.profile, pushed_elemet, val)
        self.profile.calc_macro(pushed_element=pushed_elemet, val=val)
        print_macro(self)
        tt = { 'persents': { 'cano3_ca': 16.97,
                'cano3_no3': 11.86,
                'cano3_nh4': 0.0,
                'kno3_k': 38.67,
                'kno3_no3': 13.85,
                'nh4no3_nh4': 17.5,
                'nh4no3_no3': 17.5,
                'mgso4_mg': 9.86,
                'mgso4_s': 13.01,
                'kh2po4_k': 28.73,
                'kh2po4_p': 22.76,
                'k2so4_k': 44.87,
                'k2so4_s': 18.4,
                'mgno3_mg': 9.48,
                'mgno3_no3': 10.93,
                'cacl2_ca': 18.29,
                'cacl2_cl': 32.37},
  'n': 52.899,
  'no3': 48.09,
  'nh4': 4.809,
  'p': 40.0,
  'k': 190.438,
  'ca': 211.602,
  'mg': 52.899,
  's': 242.407,
  'cl': 10.0,
  'cano3': 12.136,
  'kno3': -7.266,
  'nh4no3': 0.275,
  'mgso4': 5.365,
  'kh2po4': 1.757,
  'k2so4': 9.381,
  'mgno3': 0,
  'cacl2': 0.309}
    
        for i in self.profile.macro:
            self.assertTrue(
                tt[i] == round(getattr(self.profile, i), 3)
            )
    
        for k, i in self.profile.salt_gramms.items():
            self.assertTrue(
                tt[k] == round(getattr(self.profile, i)(), 3)
            )
    def test_calc_ch_matrix_n_s(self):
        pushed_elemet = 'matrix-n-s'
        val = 1
    
        setattr(self.profile, pushed_elemet, val)
        self.profile.calc_macro(pushed_element=pushed_elemet, val=val)
        print_macro(self)
        tt = {   'n': 133.965,
    'no3': 121.786,
    'nh4': 12.179,
    'p': 40.0,
    'k': 351.87,
    'ca': 44.377,
    'mg': 97.742,
    's': 158.052,
    'cl': 10.0,
    'cano3': 2.282,
    'kno3': 5.959,
    'nh4no3': 0.696,
    'mgso4': 9.913,
    'kh2po4': 1.757,
    'k2so4': 1.581,
    'mgno3': 0,
    'cacl2': 0.309}
    
        for i in self.profile.macro:
            self.assertTrue(
                tt[i] == round(getattr(self.profile, i), 3)
            )
    
        for k, i in self.profile.salt_gramms.items():
            self.assertTrue(
                tt[k] == round(getattr(self.profile, i)(), 3)
            )
    def test_calc_ch_matrix_p_n(self):
        pushed_elemet = 'matrix-p-n'
        val = 0.4
        # 0,4

        setattr(self.profile, pushed_elemet, val)
        self.profile.calc_macro(pushed_element=pushed_elemet, val=val)
        print_macro(self)
        tt = { 'persents': { 'cano3_ca': 16.97,
                'cano3_no3': 11.86,
                'cano3_nh4': 0.0,
                'kno3_k': 38.67,
                'kno3_no3': 13.85,
                'nh4no3_nh4': 17.5,
                'nh4no3_no3': 17.5,
                'mgso4_mg': 9.86,
                'mgso4_s': 13.01,
                'kh2po4_k': 28.73,
                'kh2po4_p': 22.76,
                'k2so4_k': 44.87,
                'k2so4_s': 18.4,
                'mgno3_mg': 9.48,
                'mgno3_no3': 10.93,
                'cacl2_ca': 18.29,
                'cacl2_cl': 32.37},
  'n': 219.998,
  'no3': 199.998,
  'nh4': 20.0,
  'p': 88.0,
  'k': 179.998,
  'ca': 200.002,
  'mg': 49.999,
  's': 43.683,
  'cl': 10.0,
  'cano3': 11.453,
  'kno3': 3.188,
  'nh4no3': 1.143,
  'mgso4': 5.071,
  'kh2po4': 3.866,
  'k2so4': -1.211,
  'mgno3': 0,
  'cacl2': 0.309}
    
        for i in self.profile.macro:
            self.assertTrue(
                tt[i] == round(getattr(self.profile, i), 3)
            )
    
        for k, i in self.profile.salt_gramms.items():
            self.assertTrue(
                tt[k] == round(getattr(self.profile, i)(), 3)
            )
    def test_calc_ch_matrix_p_k(self):
        pushed_elemet = 'matrix-p-k'
        val = 3
        # 0,4

        setattr(self.profile, pushed_elemet, val)
        self.profile.calc_macro(pushed_element=pushed_elemet, val=val)
        print_macro(self)
        tt = { 'persents': { 'cano3_ca': 16.97,
                'cano3_no3': 11.86,
                'cano3_nh4': 0.0,
                'kno3_k': 38.67,
                'kno3_no3': 13.85,
                'nh4no3_nh4': 17.5,
                'nh4no3_no3': 17.5,
                'mgso4_mg': 9.86,
                'mgso4_s': 13.01,
                'kh2po4_k': 28.73,
                'kh2po4_p': 22.76,
                'k2so4_k': 44.87,
                'k2so4_s': 18.4,
                'mgno3_mg': 9.48,
                'mgno3_no3': 10.93,
                'cacl2_ca': 18.29,
                'cacl2_cl': 32.37},
  'n': 219.998,
  'no3': 199.998,
  'nh4': 20.0,
  'p': 540.0,
  'k': 179.998,
  'ca': 200.002,
  'mg': 49.999,
  's': -190.279,
  'cl': 10.0,
  'cano3': 11.453,
  'kno3': 3.187,
  'nh4no3': 1.143,
  'mgso4': 5.071,
  'kh2po4': 23.726,
  'k2so4': -13.927,
  'mgno3': 0,
  'cacl2': 0.309}
    
        for i in self.profile.macro:
            self.assertTrue(
                tt[i] == round(getattr(self.profile, i), 3)
            )
    
        for k, i in self.profile.salt_gramms.items():
            self.assertTrue(
                tt[k] == round(getattr(self.profile, i)(), 3)
            )
    def test_calc_ch_matrix_p_ca(self):
        pushed_elemet = 'matrix-p-ca'
        val = 3
        # 0,4

        setattr(self.profile, pushed_elemet, val)
        self.profile.calc_macro(pushed_element=pushed_elemet, val=val)
        print_macro(self)
        tt =  { 'persents': { 'cano3_ca': 16.97,
                'cano3_no3': 11.86,
                'cano3_nh4': 0.0,
                'kno3_k': 38.67,
                'kno3_no3': 13.85,
                'nh4no3_nh4': 17.5,
                'nh4no3_no3': 17.5,
                'mgso4_mg': 9.86,
                'mgso4_s': 13.01,
                'kh2po4_k': 28.73,
                'kh2po4_p': 22.76,
                'k2so4_k': 44.87,
                'k2so4_s': 18.4,
                'mgno3_mg': 9.48,
                'mgno3_no3': 10.93,
                'cacl2_ca': 18.29,
                'cacl2_cl': 32.37},
  'n': 219.998,
  'no3': 199.998,
  'nh4': 20.0,
  'p': 600.013,
  'k': 179.998,
  'ca': 200.002,
  'mg': 49.999,
  's': -221.342,
  'cl': 10.0,
  'cano3': 11.453,
  'kno3': 3.187,
  'nh4no3': 1.143,
  'mgso4': 5.071,
  'kh2po4': 26.363,
  'k2so4': -15.615,
  'mgno3': 0,
  'cacl2': 0.309}
    
        for i in self.profile.macro:
            self.assertTrue(
                tt[i] == round(getattr(self.profile, i), 3)
            )
    
        for k, i in self.profile.salt_gramms.items():
            self.assertTrue(
                tt[k] == round(getattr(self.profile, i)(), 3)
            )
    def test_calc_ch_matrix_p_mg(self):
        pushed_elemet = 'matrix-p-mg'
        val = 2
        # 0,4

        setattr(self.profile, pushed_elemet, val)
        self.profile.calc_macro(pushed_element=pushed_elemet, val=val)
        print_macro(self)
        tt = { 'persents': { 'cano3_ca': 16.97,
                'cano3_no3': 11.86,
                'cano3_nh4': 0.0,
                'kno3_k': 38.67,
                'kno3_no3': 13.85,
                'nh4no3_nh4': 17.5,
                'nh4no3_no3': 17.5,
                'mgso4_mg': 9.86,
                'mgso4_s': 13.01,
                'kh2po4_k': 28.73,
                'kh2po4_p': 22.76,
                'k2so4_k': 44.87,
                'k2so4_s': 18.4,
                'mgno3_mg': 9.48,
                'mgno3_no3': 10.93,
                'cacl2_ca': 18.29,
                'cacl2_cl': 32.37},
  'n': 219.998,
  'no3': 199.998,
  'nh4': 20.0,
  'p': 100.0,
  'k': 179.998,
  'ca': 200.002,
  'mg': 49.999,
  's': 37.472,
  'cl': 10.0,
  'cano3': 11.453,
  'kno3': 3.188,
  'nh4no3': 1.143,
  'mgso4': 5.071,
  'kh2po4': 4.394,
  'k2so4': -1.549,
  'mgno3': 0,
  'cacl2': 0.309}
    
        for i in self.profile.macro:
            self.assertTrue(
                tt[i] == round(getattr(self.profile, i), 3)
            )
    
        for k, i in self.profile.salt_gramms.items():
            self.assertTrue(
                tt[k] == round(getattr(self.profile, i)(), 3)
            )
    def test_calc_ch_matrix_p_s(self):
        pushed_elemet = 'matrix-p-s'
        val = 2
        # 0,4

        setattr(self.profile, pushed_elemet, val)
        self.profile.calc_macro(pushed_element=pushed_elemet, val=val)
        print_macro(self)
        tt = { 'n': 190.36,
  'no3': 173.054,
  'nh4': 17.305,
  'p': 137.06,
  'k': 155.749,
  'ca': 227.392,
  'mg': 43.264,
  's': 49.13,
  'cl': 10.0,
  'cano3': 13.067,
  'kno3': 0.055,
  'nh4no3': 0.989,
  'mgso4': 4.388,
  'kh2po4': 6.022,
  'k2so4': -0.432,
  'mgno3': 0,
  'cacl2': 0.309}
    
        for i in self.profile.macro:
            self.assertTrue(
                tt[i] == round(getattr(self.profile, i), 3)
            )
    
        for k, i in self.profile.salt_gramms.items():
            self.assertTrue(
                tt[k] == round(getattr(self.profile, i)(), 3)
            )
    def test_calc_ch_matrix_k_n(self):
        pushed_elemet = 'matrix-k-n'
        val = 0.4
        # 0,4

        setattr(self.profile, pushed_elemet, val)
        self.profile.calc_macro(pushed_element=pushed_elemet, val=val)
        print_macro(self)
        tt ={ 'persents': { 'cano3_ca': 16.97,
                'cano3_no3': 11.86,
                'cano3_nh4': 0.0,
                'kno3_k': 38.67,
                'kno3_no3': 13.85,
                'nh4no3_nh4': 17.5,
                'nh4no3_no3': 17.5,
                'mgso4_mg': 9.86,
                'mgso4_s': 13.01,
                'kh2po4_k': 28.73,
                'kh2po4_p': 22.76,
                'k2so4_k': 44.87,
                'k2so4_s': 18.4,
                'mgno3_mg': 9.48,
                'mgno3_no3': 10.93,
                'cacl2_ca': 18.29,
                'cacl2_cl': 32.37},
  'n': 418.928,
  'no3': 380.844,
  'nh4': 38.084,
  'p': 40.0,
  'k': 167.571,
  'ca': 186.194,
  'mg': 46.548,
  's': -138.47,
  'cl': 10.0,
  'cano3': 10.639,
  'kno3': 15.633,
  'nh4no3': 2.176,
  'mgso4': 4.721,
  'kh2po4': 1.757,
  'k2so4': -10.863,
  'mgno3': 0,
  'cacl2': 0.309}
 
    
        for i in self.profile.macro:
            self.assertTrue(
                tt[i] == round(getattr(self.profile, i), 3)
            )
    
        for k, i in self.profile.salt_gramms.items():
            self.assertTrue(
                tt[k] == round(getattr(self.profile, i)(), 3)
            )
    def test_calc_ch_matrix_k_p(self):
        pushed_elemet = 'matrix-k-p'
        val = 5
        # 0,4

        setattr(self.profile, pushed_elemet, val)
        self.profile.calc_macro(pushed_element=pushed_elemet, val=val)
        print_macro(self)
        tt ={ 'persents': { 'cano3_ca': 16.97,
                'cano3_no3': 11.86,
                'cano3_nh4': 0.0,
                'kno3_k': 38.67,
                'kno3_no3': 13.85,
                'nh4no3_nh4': 17.5,
                'nh4no3_no3': 17.5,
                'mgso4_mg': 9.86,
                'mgso4_s': 13.01,
                'kh2po4_k': 28.73,
                'kh2po4_p': 22.76,
                'k2so4_k': 44.87,
                'k2so4_s': 18.4,
                'mgno3_mg': 9.48,
                'mgno3_no3': 10.93,
                'cacl2_ca': 18.29,
                'cacl2_cl': 32.37},
  'n': 214.545,
  'no3': 195.041,
  'nh4': 19.504,
  'p': 40.0,
  'k': 195.041,
  'ca': 195.045,
  'mg': 48.76,
  's': 74.203,
  'cl': 10.0,
  'cano3': 11.161,
  'kno3': 3.116,
  'nh4no3': 1.115,
  'mgso4': 4.945,
  'kh2po4': 1.757,
  'k2so4': 0.536,
  'mgno3': 0,
  'cacl2': 0.309}

 
    
        for i in self.profile.macro:
            self.assertTrue(
                tt[i] == round(getattr(self.profile, i), 3)
            )
    
        for k, i in self.profile.salt_gramms.items():
            self.assertTrue(
                tt[k] == round(getattr(self.profile, i)(), 3)
            )
    def test_calc_ch_matrix_k_ca(self):
        pushed_elemet = 'matrix-k-ca'
        val = 1
        # 0,4

        setattr(self.profile, pushed_elemet, val)
        self.profile.calc_macro(pushed_element=pushed_elemet, val=val)
        print_macro(self)
        tt = { 'persents': { 'cano3_ca': 16.97,
                'cano3_no3': 11.86,
                'cano3_nh4': 0.0,
                'kno3_k': 38.67,
                'kno3_no3': 13.85,
                'nh4no3_nh4': 17.5,
                'nh4no3_no3': 17.5,
                'mgso4_mg': 9.86,
                'mgso4_s': 13.01,
                'kh2po4_k': 28.73,
                'kh2po4_p': 22.76,
                'k2so4_k': 44.87,
                'k2so4_s': 18.4,
                'mgno3_mg': 9.48,
                'mgno3_no3': 10.93,
                'cacl2_ca': 18.29,
                'cacl2_cl': 32.37},
  'n': 231.481,
  'no3': 210.437,
  'nh4': 21.044,
  'p': 40.0,
  'k': 189.394,
  'ca': 189.394,
  'mg': 52.609,
  's': 56.583,
  'cl': 10.0,
  'cano3': 10.828,
  'kno3': 4.401,
  'nh4no3': 1.202,
  'mgso4': 5.336,
  'kh2po4': 1.757,
  'k2so4': -0.697,
  'mgno3': 0,
  'cacl2': 0.309}
    
        for i in self.profile.macro:
            self.assertTrue(
                tt[i] == round(getattr(self.profile, i), 3)
            )
    
        for k, i in self.profile.salt_gramms.items():
            self.assertTrue(
                tt[k] == round(getattr(self.profile, i)(), 3)
            )
    def test_calc_ch_matrix_k_mg(self):
        pushed_elemet = 'matrix-k-mg'
        val = 3
        # 0,4

        setattr(self.profile, pushed_elemet, val)
        self.profile.calc_macro(pushed_element=pushed_elemet, val=val)
        print_macro(self)
        tt = { 'persents': { 'cano3_ca': 16.97,
                'cano3_no3': 11.86,
                'cano3_nh4': 0.0,
                'kno3_k': 38.67,
                'kno3_no3': 13.85,
                'nh4no3_nh4': 17.5,
                'nh4no3_no3': 17.5,
                'mgso4_mg': 9.86,
                'mgso4_s': 13.01,
                'kh2po4_k': 28.73,
                'kh2po4_p': 22.76,
                'k2so4_k': 44.87,
                'k2so4_s': 18.4,
                'mgno3_mg': 9.48,
                'mgno3_no3': 10.93,
                'cacl2_ca': 18.29,
                'cacl2_cl': 32.37},
  'n': 211.359,
  'no3': 192.144,
  'nh4': 19.214,
  'p': 40.0,
  'k': 172.93,
  'ca': 192.148,
  'mg': 57.643,
  's': 77.522,
  'cl': 10.0,
  'cano3': 10.99,
  'kno3': 3.074,
  'nh4no3': 1.098,
  'mgso4': 5.846,
  'kh2po4': 1.757,
  'k2so4': 0.08,
  'mgno3': 0,
  'cacl2': 0.309}
 
    
        for i in self.profile.macro:
            self.assertTrue(
                tt[i] == round(getattr(self.profile, i), 3)
            )
    
        for k, i in self.profile.salt_gramms.items():
            self.assertTrue(
                tt[k] == round(getattr(self.profile, i)(), 3)
            )
    def test_calc_ch_matrix_k_s(self):
        pushed_elemet = 'matrix-k-s'
        val = 3
        # 0,4

        setattr(self.profile, pushed_elemet, val)
        self.profile.calc_macro(pushed_element=pushed_elemet, val=val)
        print_macro(self)
        tt = { 'n': 219.998,
  'no3': 199.998,
  'nh4': 20.0,
  'p': 40.0,
  'k': 205.588,
  'ca': 186.887,
  'mg': 49.999,
  's': 68.529,
  'cl': 10.0,
  'cano3': 10.68,
  'kno3': 3.85,
  'nh4no3': 1.143,
  'mgso4': 5.071,
  'kh2po4': 1.757,
  'k2so4': 0.139,
  'mgno3': 0,
  'cacl2': 0.309}
 
    
        for i in self.profile.macro:
            self.assertTrue(
                tt[i] == round(getattr(self.profile, i), 3)
            )
    
        for k, i in self.profile.salt_gramms.items():
            self.assertTrue(
                tt[k] == round(getattr(self.profile, i)(), 3)
            )
    def test_calc_ch_matrix_ca_n(self):
        pushed_elemet = 'matrix-ca-n'
        val = 1
        # 0,4

        setattr(self.profile, pushed_elemet, val)
        self.profile.calc_macro(pushed_element=pushed_elemet, val=val)
        print_macro(self)
        tt = { 'n': 209.606,
  'no3': 190.551,
  'nh4': 19.055,
  'p': 40.0,
  'k': 171.496,
  'ca': 209.606,
  'mg': 47.638,
  's': 79.342,
  'cl': 10.0,
  'cano3': 12.019,
  'kno3': 2.09,
  'nh4no3': 1.089,
  'mgso4': 4.831,
  'kh2po4': 1.757,
  'k2so4': 0.896,
  'mgno3': 0,
  'cacl2': 0.309}
 
    
        for i in self.profile.macro:
            self.assertTrue(
                tt[i] == round(getattr(self.profile, i), 3)
            )
    
        for k, i in self.profile.salt_gramms.items():
            self.assertTrue(
                tt[k] == round(getattr(self.profile, i)(), 3)
            )
    def test_calc_ch_matrix_ca_p(self):
        pushed_elemet = 'matrix-ca-p'
        val = 1
        # 0,4

        setattr(self.profile, pushed_elemet, val)
        self.profile.calc_macro(pushed_element=pushed_elemet, val=val)
        print_macro(self)
        tt = { 'n': 364.667,
  'no3': 331.516,
  'nh4': 33.152,
  'p': 40.0,
  'k': 298.364,
  'ca': 66.303,
  'mg': 82.879,
  's': -82.011,
  'cl': 10.0,
  'cano3': 3.574,
  'kno3': 18.478,
  'nh4no3': 1.894,
  'mgso4': 8.406,
  'kh2po4': 1.757,
  'k2so4': -10.4,
  'mgno3': 0,
  'cacl2': 0.309}

 
    
        for i in self.profile.macro:
            self.assertTrue(
                tt[i] == round(getattr(self.profile, i), 3)
            )
    
        for k, i in self.profile.salt_gramms.items():
            self.assertTrue(
                tt[k] == round(getattr(self.profile, i)(), 3)
            )
    def test_calc_ch_matrix_ca_k(self):
        pushed_elemet = 'matrix-ca-k'
        val = 1
        # 0,4

        setattr(self.profile, pushed_elemet, val)
        self.profile.calc_macro(pushed_element=pushed_elemet, val=val)
        print_macro(self)
        tt = { 'n': 231.479,
  'no3': 210.435,
  'nh4': 21.044,
  'p': 40.0,
  'k': 189.392,
  'ca': 189.392,
  'mg': 52.609,
  's': 56.582,
  'cl': 10.0,
  'cano3': 10.827,
  'kno3': 4.401,
  'nh4no3': 1.202,
  'mgso4': 5.336,
  'kh2po4': 1.757,
  'k2so4': -0.697,
  'mgno3': 0,
  'cacl2': 0.309}

 
    
        for i in self.profile.macro:
            self.assertTrue(
                tt[i] == round(getattr(self.profile, i), 3)
            )
    
        for k, i in self.profile.salt_gramms.items():
            self.assertTrue(
                tt[k] == round(getattr(self.profile, i)(), 3)
            )
    def test_calc_ch_matrix_ca_mg(self):
        # вопрос в чате
        
        pushed_elemet = 'matrix-ca-mg'
        val = 1
        setattr(self.profile, pushed_elemet, val)
        self.profile.calc_macro(pushed_element=pushed_elemet, val=val)
        print_macro(self)
        tt = { 'persents': { 'cano3_ca': 16.97,
                'cano3_no3': 11.86,
                'cano3_nh4': 0.0,
                'kno3_k': 38.67,
                'kno3_no3': 13.85,
                'nh4no3_nh4': 17.5,
                'nh4no3_no3': 17.5,
                'mgso4_mg': 9.86,
                'mgso4_s': 13.01,
                'kh2po4_k': 28.73,
                'kh2po4_p': 22.76,
                'k2so4_k': 44.87,
                'k2so4_s': 18.4,
                'mgno3_mg': 9.48,
                'mgno3_no3': 10.93,
                'cacl2_ca': 18.29,
                'cacl2_cl': 32.37},
  'n': 350.272,
  'no3': 318.429,
  'nh4': 31.843,
  'p': 40.0,
  'k': 286.586,
  'ca': 79.607,
  'mg': 79.607,
  's': -67.031,
  'cl': 10.0,
  'cano3': 4.358,
  'kno3': 16.956,
  'nh4no3': 1.82,
  'mgso4': 8.074,
  'kh2po4': 1.757,
  'k2so4': -9.352,
  'mgno3': 0,
  'cacl2': 0.309}

 
    
        for i in self.profile.macro:
            self.assertTrue(
                tt[i] == round(getattr(self.profile, i), 3)
            )
    
        for k, i in self.profile.salt_gramms.items():
            self.assertTrue(
                tt[k] == round(getattr(self.profile, i)(), 3)
            )
    def test_calc_ch_matrix_ca_s(self):
        pushed_elemet = 'matrix-ca-s'
        val = 1
        # 0,4

        setattr(self.profile, pushed_elemet, val)
        self.profile.calc_macro(pushed_element=pushed_elemet, val=val)
        print_macro(self)
        tt = { 'persents': { 'cano3_ca': 16.97,
                'cano3_no3': 11.86,
                'cano3_nh4': 0.0,
                'kno3_k': 38.67,
                'kno3_no3': 13.85,
                'nh4no3_nh4': 17.5,
                'nh4no3_no3': 17.5,
                'mgso4_mg': 9.86,
                'mgso4_s': 13.01,
                'kh2po4_k': 28.73,
                'kh2po4_p': 22.76,
                'k2so4_k': 44.87,
                'k2so4_s': 18.4,
                'mgno3_mg': 9.48,
                'mgno3_no3': 10.93,
                'cacl2_ca': 18.29,
                'cacl2_cl': 32.37},
  'n': 156.31,
  'no3': 142.1,
  'nh4': 14.21,
  'p': 40.0,
  'k': 127.89,
  'ca': 258.86,
  'mg': 35.525,
  's': 134.8,
  'cl': 10.0,
  'cano3': 14.921,
  'kno3': -3.543,
  'nh4no3': 0.812,
  'mgso4': 3.603,
  'kh2po4': 1.757,
  'k2so4': 4.779,
  'mgno3': 0,
  'cacl2': 0.309}
    
        for i in self.profile.macro:
            self.assertTrue(
                tt[i] == round(getattr(self.profile, i), 3)
            )
    
        for k, i in self.profile.salt_gramms.items():
            self.assertTrue(
                tt[k] == round(getattr(self.profile, i)(), 3)
            )
    def test_calc_ch_matrix_mg_n(self):
        pushed_elemet = 'matrix-mg-n'
        val = 0.4
        # 0,4

        setattr(self.profile, pushed_elemet, val)
        self.profile.calc_macro(pushed_element=pushed_elemet, val=val)
        print_macro(self)
        tt = { 'persents': { 'cano3_ca': 16.97,
                'cano3_no3': 11.86,
                'cano3_nh4': 0.0,
                'kno3_k': 38.67,
                'kno3_no3': 13.85,
                'nh4no3_nh4': 17.5,
                'nh4no3_no3': 17.5,
                'mgso4_mg': 9.86,
                'mgso4_s': 13.01,
                'kh2po4_k': 28.73,
                'kh2po4_p': 22.76,
                'k2so4_k': 44.87,
                'k2so4_s': 18.4,
                'mgno3_mg': 9.48,
                'mgno3_no3': 10.93,
                'cacl2_ca': 18.29,
                'cacl2_cl': 32.37},
  'n': 190.415,
  'no3': 173.104,
  'nh4': 17.31,
  'p': 40.0,
  'k': 155.794,
  'ca': 173.108,
  'mg': 76.166,
  's': 99.312,
  'cl': 10.0,
  'cano3': 9.868,
  'kno3': 2.798,
  'nh4no3': 0.989,
  'mgso4': 7.725,
  'kh2po4': 1.757,
  'k2so4': -0.064,
  'mgno3': 0,
  'cacl2': 0.309}


    
        for i in self.profile.macro:
            self.assertTrue(
                tt[i] == round(getattr(self.profile, i), 3)
            )
    
        for k, i in self.profile.salt_gramms.items():
            self.assertTrue(
                tt[k] == round(getattr(self.profile, i)(), 3)
            )
    def test_calc_ch_matrix_mg_p(self):
        pushed_elemet = 'matrix-mg-p'
        val = 1
        # 0,4

        setattr(self.profile, pushed_elemet, val)
        self.profile.calc_macro(pushed_element=pushed_elemet, val=val)
        print_macro(self)
        tt = { 'persents': { 'cano3_ca': 16.97,
                'cano3_no3': 11.86,
                'cano3_nh4': 0.0,
                'kno3_k': 38.67,
                'kno3_no3': 13.85,
                'nh4no3_nh4': 17.5,
                'nh4no3_no3': 17.5,
                'mgso4_mg': 9.86,
                'mgso4_s': 13.01,
                'kh2po4_k': 28.73,
                'kh2po4_p': 22.76,
                'k2so4_k': 44.87,
                'k2so4_s': 18.4,
                'mgno3_mg': 9.48,
                'mgno3_no3': 10.93,
                'cacl2_ca': 18.29,
                'cacl2_cl': 32.37},
  'n': 229.376,
  'no3': 208.523,
  'nh4': 20.852,
  'p': 40.0,
  'k': 187.671,
  'ca': 208.528,
  'mg': 41.705,
  's': 58.771,
  'cl': 10.0,
  'cano3': 11.955,
  'kno3': 3.311,
  'nh4no3': 1.192,
  'mgso4': 4.23,
  'kh2po4': 1.757,
  'k2so4': 0.203,
  'mgno3': 0,
  'cacl2': 0.309}


    
        for i in self.profile.macro:
            self.assertTrue(
                tt[i] == round(getattr(self.profile, i), 3)
            )
    
        for k, i in self.profile.salt_gramms.items():
            self.assertTrue(
                tt[k] == round(getattr(self.profile, i)(), 3)
            )
    def test_calc_ch_matrix_mg_k(self):
        pushed_elemet = 'matrix-mg-k'
        val = 1
        setattr(self.profile, pushed_elemet, val)
        self.profile.calc_macro(pushed_element=pushed_elemet, val=val)
        print_macro(self)
        tt = { 'persents': { 'cano3_ca': 16.97,
                'cano3_no3': 11.86,
                'cano3_nh4': 0.0,
                'kno3_k': 38.67,
                'kno3_no3': 13.85,
                'nh4no3_nh4': 17.5,
                'nh4no3_no3': 17.5,
                'mgso4_mg': 9.86,
                'mgso4_s': 13.01,
                'kh2po4_k': 28.73,
                'kh2po4_p': 22.76,
                'k2so4_k': 44.87,
                'k2so4_s': 18.4,
                'mgno3_mg': 9.48,
                'mgno3_no3': 10.93,
                'cacl2_ca': 18.29,
                'cacl2_cl': 32.37},
  'n': 143.649,
  'no3': 130.59,
  'nh4': 13.059,
  'p': 40.0,
  'k': 117.531,
  'ca': 130.592,
  'mg': 117.531,
  's': 147.976,
  'cl': 10.0,
  'cano3': 7.363,
  'kno3': 2.182,
  'nh4no3': 0.746,
  'mgso4': 11.92,
  'kh2po4': 1.757,
  'k2so4': -0.386,
  'mgno3': 0,
  'cacl2': 0.309}


    
        for i in self.profile.macro:
            self.assertTrue(
                tt[i] == round(getattr(self.profile, i), 3)
            )
    
        for k, i in self.profile.salt_gramms.items():
            self.assertTrue(
                tt[k] == round(getattr(self.profile, i)(), 3)
            )
    def test_calc_ch_matrix_mg_ca(self):
        pushed_elemet = 'matrix-mg-ca'
        val = 1
        setattr(self.profile, pushed_elemet, val)
        self.profile.calc_macro(pushed_element=pushed_elemet, val=val)
        print_macro(self)
        tt = { 'persents': { 'cano3_ca': 16.97,
                'cano3_no3': 11.86,
                'cano3_nh4': 0.0,
                'kno3_k': 38.67,
                'kno3_no3': 13.85,
                'nh4no3_nh4': 17.5,
                'nh4no3_no3': 17.5,
                'mgso4_mg': 9.86,
                'mgso4_s': 13.01,
                'kh2po4_k': 28.73,
                'kh2po4_p': 22.76,
                'k2so4_k': 44.87,
                'k2so4_s': 18.4,
                'mgno3_mg': 9.48,
                'mgno3_no3': 10.93,
                'cacl2_ca': 18.29,
                'cacl2_cl': 32.37},
  'n': 136.366,
  'no3': 123.969,
  'nh4': 12.397,
  'p': 40.0,
  'k': 111.572,
  'ca': 123.972,
  'mg': 123.972,
  's': 155.554,
  'cl': 10.0,
  'cano3': 6.972,
  'kno3': 2.086,
  'nh4no3': 0.708,
  'mgso4': 12.573,
  'kh2po4': 1.757,
  'k2so4': -0.436,
  'mgno3': 0,
  'cacl2': 0.309}


    
        for i in self.profile.macro:
            self.assertTrue(
                tt[i] == round(getattr(self.profile, i), 3)
            )
    
        for k, i in self.profile.salt_gramms.items():
            self.assertTrue(
                tt[k] == round(getattr(self.profile, i)(), 3)
            )
    def test_calc_ch_matrix_mg_s(self):
        pushed_elemet = 'matrix-mg-s'
        val = 1
        setattr(self.profile, pushed_elemet, val)
        self.profile.calc_macro(pushed_element=pushed_elemet, val=val)
        print_macro(self)
        tt = { 'n': 219.998,
  'no3': 199.998,
  'nh4': 20.0,
  'p': 40.0,
  'k': 179.998,
  'ca': 169.447,
  'mg': 68.529,
  's': 68.529,
  'cl': 10.0,
  'cano3': 9.652,
  'kno3': 4.73,
  'nh4no3': 1.143,
  'mgso4': 6.95,
  'kh2po4': 1.757,
  'k2so4': -1.19,
  'mgno3': 0,
  'cacl2': 0.309}
        for i in self.profile.macro:
            self.assertTrue(
                tt[i] == round(getattr(self.profile, i), 3)
            )
    
        for k, i in self.profile.salt_gramms.items():
            self.assertTrue(
                tt[k] == round(getattr(self.profile, i)(), 3)
            )
    def test_calc_ch_matrix_s_n(self):
        pushed_elemet = 'matrix-s-n'
        val = 0.4
        # 0,4
        setattr(self.profile, pushed_elemet, val)
        self.profile.calc_macro(pushed_element=pushed_elemet, val=val)
        print_macro(self)
        tt = { 'n': 207.479,
  'no3': 188.617,
  'nh4': 18.862,
  'p': 40.0,
  'k': 169.755,
  'ca': 211.572,
  'mg': 47.154,
  's': 81.556,
  'cl': 10.0,
  'cano3': 12.134,
  'kno3': 1.865,
  'nh4no3': 1.078,
  'mgso4': 4.782,
  'kh2po4': 1.757,
  'k2so4': 1.051,
  'mgno3': 0,
  'cacl2': 0.309}
        for i in self.profile.macro:
            self.assertTrue(
                tt[i] == round(getattr(self.profile, i), 3)
            )
    
        for k, i in self.profile.salt_gramms.items():
            self.assertTrue(
                tt[k] == round(getattr(self.profile, i)(), 3)
            )
    def test_calc_ch_matrix_s_p(self):
        pushed_elemet = 'matrix-s-p'
        val = 1
        # 0,4
        setattr(self.profile, pushed_elemet, val)
        self.profile.calc_macro(pushed_element=pushed_elemet, val=val)
        print_macro(self)
        tt = { 'n': 241.335,
  'no3': 219.396,
  'nh4': 21.94,
  'p': 40.0,
  'k': 197.456,
  'ca': 180.283,
  'mg': 54.849,
  's': 46.326,
  'cl': 10.0,
  'cano3': 10.291,
  'kno3': 5.443,
  'nh4no3': 1.254,
  'mgso4': 5.563,
  'kh2po4': 1.757,
  'k2so4': -1.416,
  'mgno3': 0,
  'cacl2': 0.309}
        for i in self.profile.macro:
            self.assertTrue(
                tt[i] == round(getattr(self.profile, i), 3)
            )
    
        for k, i in self.profile.salt_gramms.items():
            self.assertTrue(
                tt[k] == round(getattr(self.profile, i)(), 3)
            )
    def test_calc_ch_matrix_s_k(self):
        pushed_elemet = 'matrix-s-k'
        val = 1
        # 0,4
        setattr(self.profile, pushed_elemet, val)
        self.profile.calc_macro(pushed_element=pushed_elemet, val=val)
        print_macro(self)
        tt = { 'n': 163.513,
  'no3': 148.648,
  'nh4': 14.865,
  'p': 40.0,
  'k': 133.783,
  'ca': 252.204,
  'mg': 37.162,
  's': 127.306,
  'cl': 10.0,
  'cano3': 14.529,
  'kno3': -2.782,
  'nh4no3': 0.849,
  'mgso4': 3.769,
  'kh2po4': 1.757,
  'k2so4': 4.254,
  'mgno3': 0,
  'cacl2': 0.309}

        for i in self.profile.macro:
            self.assertTrue(
                tt[i] == round(getattr(self.profile, i), 3)
            )
    
        for k, i in self.profile.salt_gramms.items():
            self.assertTrue(
                tt[k] == round(getattr(self.profile, i)(), 3)
            )
    def test_calc_ch_matrix_s_ca(self):
        pushed_elemet = 'matrix-s-ca'
        val = 1
        # 0,4
        setattr(self.profile, pushed_elemet, val)
        self.profile.calc_macro(pushed_element=pushed_elemet, val=val)
        print_macro(self)
        tt = { 'persents': { 'cano3_ca': 16.97,
                'cano3_no3': 11.86,
                'cano3_nh4': 0.0,
                'kno3_k': 38.67,
                'kno3_no3': 13.85,
                'nh4no3_nh4': 17.5,
                'nh4no3_no3': 17.5,
                'mgso4_mg': 9.86,
                'mgso4_s': 13.01,
                'kh2po4_k': 28.73,
                'kh2po4_p': 22.76,
                'k2so4_k': 44.87,
                'k2so4_s': 18.4,
                'mgno3_mg': 9.48,
                'mgno3_no3': 10.93,
                'cacl2_ca': 18.29,
                'cacl2_cl': 32.37},
  'n': 156.31,
  'no3': 142.1,
  'nh4': 14.21,
  'p': 40.0,
  'k': 127.89,
  'ca': 258.86,
  'mg': 35.525,
  's': 134.8,
  'cl': 10.0,
  'cano3': 14.921,
  'kno3': -3.543,
  'nh4no3': 0.812,
  'mgso4': 3.603,
  'kh2po4': 1.757,
  'k2so4': 4.779,
  'mgno3': 0,
  'cacl2': 0.309}


        for i in self.profile.macro:
            self.assertTrue(
                tt[i] == round(getattr(self.profile, i), 3)
            )
    
        for k, i in self.profile.salt_gramms.items():
            self.assertTrue(
                tt[k] == round(getattr(self.profile, i)(), 3)
            )

    def test_calc_ch_matrix_s_mg(self):
        pushed_elemet = 'matrix-s-mg'
        val = 1
        # 0,4
        setattr(self.profile, pushed_elemet, val)
        self.profile.calc_macro(pushed_element=pushed_elemet, val=val)
        print_macro(self)
        tt = {'n': 233.401,
              'no3': 212.182,
              'nh4': 21.218,
              'p': 40.0,
              'k': 190.964,
              'ca': 187.616,
              'mg': 53.046,
              's': 54.582,
              'cl': 10.0,
              'cano3': 10.723,
              'kno3': 4.604,
              'nh4no3': 1.212,
              'mgso4': 5.38,
              'kh2po4': 1.757,
              'k2so4': -0.838,
              'mgno3': 0,
              'cacl2': 0.309}
    
        for i in self.profile.macro:
            self.assertTrue(
                tt[i] == round(getattr(self.profile, i), 3)
            )
    
        for k, i in self.profile.salt_gramms.items():
            self.assertTrue(
                tt[k] == round(getattr(self.profile, i)(), 3)
            )

    def test_calc_ch_cano3_ca(self):
        pushed_elemet = 'cano3_ca'
        val = 18
        # 0,4
        setattr(self.profile, pushed_elemet, val)
        self.profile.calc_macro(pushed_element=pushed_elemet, val=val)
        print_macro(self)
        tt = {'n': 220.0,
              'no3': 200.0,
              'nh4': 20.0,
              'p': 40.0,
              'k': 180.0,
              'ca': 200.004,
              'mg': 50.0,
              's': 68.53,
              'cl': 10.0,
              'cano3': 10.797,
              'kno3': 3.188,
              'nh4no3': 1.143,
              'mgso4': 5.071,
              'kh2po4': 1.757,
              'k2so4': 0.139,
              'mgno3': 0,
              'cacl2': 0.309}
    
        for i in self.profile.macro:
            self.assertTrue(
                tt[i] == round(getattr(self.profile, i), 3)
            )
    
        for k, i in self.profile.salt_gramms.items():
            self.assertTrue(
                tt[k] == round(getattr(self.profile, i)(), 3)
            )

    def test_calc_ch_cano3_no3(self):
        pushed_elemet = 'cano3_no3'
        val = 18
        # 0,4
        setattr(self.profile, pushed_elemet, val)
        self.profile.calc_macro(pushed_element=pushed_elemet, val=val)
        print_macro(self)
        tt = {'n': 220.0,
              'no3': 200.0,
              'nh4': 20.0,
              'p': 40.0,
              'k': 180.0,
              'ca': 200.004,
              'mg': 50.0,
              's': 68.53,
              'cl': 10.0,
              'cano3': 7.547,
              'kno3': 3.188,
              'nh4no3': 1.143,
              'mgso4': 5.071,
              'kh2po4': 1.757,
              'k2so4': 0.139,
              'mgno3': 0,
              'cacl2': 0.309}
    
        for i in self.profile.macro:
            self.assertTrue(
                tt[i] == round(getattr(self.profile, i), 3)
            )
    
        for k, i in self.profile.salt_gramms.items():
            self.assertTrue(
                tt[k] == round(getattr(self.profile, i)(), 3)
            )

    def test_calc_ch_cano3_nh4(self):
        pushed_elemet = 'cano3_nh4'
        val = 10
        # 0,4
        setattr(self.profile, pushed_elemet, val)
        self.profile.calc_macro(pushed_element=pushed_elemet, val=val)
        print_macro(self)
        tt = {'n': 220.0,
              'no3': 200.0,
              'nh4': 20.0,
              'p': 40.0,
              'k': 180.0,
              'ca': 200.004,
              'mg': 50.0,
              's': 68.53,
              'cl': 10.0,
              'cano3': 11.453,
              'kno3': 3.188,
              'nh4no3': -5.402,
              'mgso4': 5.071,
              'kh2po4': 1.757,
              'k2so4': 0.139,
              'mgno3': 0,
              'cacl2': 0.309}
    
        for i in self.profile.macro:
            self.assertTrue(
                tt[i] == round(getattr(self.profile, i), 3)
            )
    
        for k, i in self.profile.salt_gramms.items():
            self.assertTrue(
                tt[k] == round(getattr(self.profile, i)(), 3)
            )

    def test_calc_ch_kno3_k(self):
        pushed_elemet = 'kno3_k'
        val = 10
        # 0,4
        setattr(self.profile, pushed_elemet, val)
        self.profile.calc_macro(pushed_element=pushed_elemet, val=val)
        print_macro(self)
        tt = { 'persents': { 'cano3_ca': 16.97,
                'cano3_no3': 11.86,
                'cano3_nh4': 0.0,
                'kno3_k': 10,
                'kno3_no3': 3.582,
                'nh4no3_nh4': 17.5,
                'nh4no3_no3': 17.5,
                'mgso4_mg': 9.86,
                'mgso4_s': 13.01,
                'kh2po4_k': 28.73,
                'kh2po4_p': 22.76,
                'k2so4_k': 44.87,
                'k2so4_s': 18.4,
                'mgno3_mg': 9.48,
                'mgno3_no3': 10.93,
                'cacl2_ca': 18.29,
                'cacl2_cl': 32.37},
  'n': 220.0,
  'no3': 200.0,
  'nh4': 20.0,
  'p': 40.0,
  'k': 180.0,
  'ca': 200.004,
  'mg': 50.0,
  's': 68.53,
  'cl': 10.0,
  'cano3': 11.453,
  'kno3': 12.327,
  'nh4no3': 1.143,
  'mgso4': 5.071,
  'kh2po4': 1.757,
  'k2so4': 0.139,
  'mgno3': 0,
  'cacl2': 0.309}

    
        for i in self.profile.macro:
            self.assertTrue(
                tt[i] == round(getattr(self.profile, i), 3)
            )

        for k, i in self.profile.salt_gramms.items():
            self.assertTrue(
                tt[k] == round(getattr(self.profile, i)(), 3)
            )
        for i in self.profile.salt:
            self.assertTrue(
                tt['persents'][i] == round(getattr(self.profile, i), 3)
            )
    def test_calc_ch_kno3_no3(self):
        pushed_elemet = 'kno3_no3'
        val = 10
        # 0,4
        setattr(self.profile, pushed_elemet, val)
        self.profile.calc_macro(pushed_element=pushed_elemet, val=val)
        print_macro(self)
        tt = { 'persents':
                   { 'cano3_ca': 16.97,
                'cano3_no3': 11.86,
                'cano3_nh4': 0.0,
                'kno3_k': 27.914,
                'kno3_no3': 10.0,
                'nh4no3_nh4': 17.5,
                'nh4no3_no3': 17.5,
                'mgso4_mg': 9.86,
                'mgso4_s': 13.01,
                'kh2po4_k': 28.73,
                'kh2po4_p': 22.76,
                'k2so4_k': 44.87,
                'k2so4_s': 18.4,
                'mgno3_mg': 9.48,
                'mgno3_no3': 10.93,
                'cacl2_ca': 18.29,
                'cacl2_cl': 32.37},
                  'n': 220.0,
                  'no3': 200.0,
                  'nh4': 20.0,
                  'p': 40.0,
                  'k': 180.0,
                  'ca': 200.004,
                  'mg': 50.0,
                  's': 68.53,
                  'cl': 10.0,
                  'cano3': 11.453,
                  'kno3': 4.416,
                  'nh4no3': 1.143,
                  'mgso4': 5.071,
                  'kh2po4': 1.757,
                  'k2so4': 0.139,
                  'mgno3': 0,
                  'cacl2': 0.309}
        for i in self.profile.macro:
            self.assertTrue(
                tt[i] == round(getattr(self.profile, i), 3)
            )

        for k, i in self.profile.salt_gramms.items():
            self.assertTrue(
                tt[k] == round(getattr(self.profile, i)(), 3)
            )
        for i in self.profile.salt:
            self.assertTrue(
                tt['persents'][i] == round(getattr(self.profile, i), 3)
            )
    def test_calc_ch_nh4no3_nh4(self):
        pushed_elemet = 'nh4no3_nh4'
        val = 10
        # 0,4
        setattr(self.profile, pushed_elemet, val)
        self.profile.calc_macro(pushed_element=pushed_elemet, val=val)
        print_macro(self)
        tt = { 'persents': { 'cano3_ca': 16.97,
                'cano3_no3': 11.86,
                'cano3_nh4': 0.0,
                'kno3_k': 38.67,
                'kno3_no3': 13.85,
                'nh4no3_nh4': 10,
                'nh4no3_no3': 10,
                'mgso4_mg': 9.86,
                'mgso4_s': 13.01,
                'kh2po4_k': 28.73,
                'kh2po4_p': 22.76,
                'k2so4_k': 44.87,
                'k2so4_s': 18.4,
                'mgno3_mg': 9.48,
                'mgno3_no3': 10.93,
                'cacl2_ca': 18.29,
                'cacl2_cl': 32.37},
  'n': 220.0,
  'no3': 200.0,
  'nh4': 20.0,
  'p': 40.0,
  'k': 180.0,
  'ca': 200.004,
  'mg': 50.0,
  's': 68.53,
  'cl': 10.0,
  'cano3': 11.453,
  'kno3': 3.188,
  'nh4no3': 2.0,
  'mgso4': 5.071,
  'kh2po4': 1.757,
  'k2so4': 0.139,
  'mgno3': 0,
  'cacl2': 0.309}
        for i in self.profile.macro:
            self.assertTrue(
                tt[i] == round(getattr(self.profile, i), 3)
            )

        for k, i in self.profile.salt_gramms.items():
            self.assertTrue(
                tt[k] == round(getattr(self.profile, i)(), 3)
            )
        for i in self.profile.salt:
            self.assertTrue(
                tt['persents'][i] == round(getattr(self.profile, i), 3)
            )
    def test_calc_ch_kno3_no3(self):
        pushed_elemet = 'nh4no3_no3'
        val = 10
        # 0,4
        setattr(self.profile, pushed_elemet, val)
        self.profile.calc_macro(pushed_element=pushed_elemet, val=val)
        print_macro(self)
        tt = { 'persents': { 'cano3_ca': 16.97,
                'cano3_no3': 11.86,
                'cano3_nh4': 0.0,
                'kno3_k': 38.67,
                'kno3_no3': 13.85,
                'nh4no3_nh4': 10,
                'nh4no3_no3': 10,
                'mgso4_mg': 9.86,
                'mgso4_s': 13.01,
                'kh2po4_k': 28.73,
                'kh2po4_p': 22.76,
                'k2so4_k': 44.87,
                'k2so4_s': 18.4,
                'mgno3_mg': 9.48,
                'mgno3_no3': 10.93,
                'cacl2_ca': 18.29,
                'cacl2_cl': 32.37},
  'n': 220.0,
  'no3': 200.0,
  'nh4': 20.0,
  'p': 40.0,
  'k': 180.0,
  'ca': 200.004,
  'mg': 50.0,
  's': 68.53,
  'cl': 10.0,
  'cano3': 11.453,
  'kno3': 3.188,
  'nh4no3': 2.0,
  'mgso4': 5.071,
  'kh2po4': 1.757,
  'k2so4': 0.139,
  'mgno3': 0,
  'cacl2': 0.309}
        for i in self.profile.macro:
            self.assertTrue(
                tt[i] == round(getattr(self.profile, i), 3)
            )

        for k, i in self.profile.salt_gramms.items():
            self.assertTrue(
                tt[k] == round(getattr(self.profile, i)(), 3)
            )
        for i in self.profile.salt:
            self.assertTrue(
                tt['persents'][i] == round(getattr(self.profile, i), 3)
            )
    def test_calc_ch_mgso4_mg(self):
        pushed_elemet = 'mgso4_mg'
        val = 10
        # 0,4
        setattr(self.profile, pushed_elemet, val)
        self.profile.calc_macro(pushed_element=pushed_elemet, val=val)
        print_macro(self)
        tt = {
            'persents': { 'cano3_ca': 16.97,
                'cano3_no3': 11.86,
                'cano3_nh4': 0.0,
                'kno3_k': 38.67,
                'kno3_no3': 13.85,
                'nh4no3_nh4': 17.5,
                'nh4no3_no3': 17.5,
                'mgso4_mg': 10,
                'mgso4_s': 13.193,
                'kh2po4_k': 28.73,
                'kh2po4_p': 22.76,
                'k2so4_k': 44.87,
                'k2so4_s': 18.4,
                'mgno3_mg': 9.48,
                'mgno3_no3': 10.93,
                'cacl2_ca': 18.29,
                'cacl2_cl': 32.37},
                  'n': 220.0,
                  'no3': 200.0,
                  'nh4': 20.0,
                  'p': 40.0,
                  'k': 180.0,
                  'ca': 200.004,
                  'mg': 50.0,
                  's': 68.53,
                  'cl': 10.0,
                  'cano3': 11.453,
                  'kno3': 3.187,
                  'nh4no3': 1.143,
                  'mgso4': 5.0,
                  'kh2po4': 1.757,
                  'k2so4': 0.139,
                  'mgno3': 0,
                  'cacl2': 0.309
        }
        
        for i in self.profile.macro:
            self.assertTrue(
                tt[i] == round(getattr(self.profile, i), 3)
            )

        for k, i in self.profile.salt_gramms.items():
            self.assertTrue(
                tt[k] == round(getattr(self.profile, i)(), 3)
            )
        for i in self.profile.salt:
            self.assertTrue(
                tt['persents'][i] == round(getattr(self.profile, i), 3)
            )
    def test_calc_ch_mgso4_s(self):
        pushed_elemet = 'mgso4_s'
        val = 10
        # 0,4
        setattr(self.profile, pushed_elemet, val)
        self.profile.calc_macro(pushed_element=pushed_elemet, val=val)
        print_macro(self)
        tt = {
            'persents': { 'cano3_ca': 16.97,
                'cano3_no3': 11.86,
                'cano3_nh4': 0.0,
                'kno3_k': 38.67,
                'kno3_no3': 13.85,
                'nh4no3_nh4': 17.5,
                'nh4no3_no3': 17.5,
                'mgso4_mg': 7.58,
                'mgso4_s': 10,
                'kh2po4_k': 28.73,
                'kh2po4_p': 22.76,
                'k2so4_k': 44.87,
                'k2so4_s': 18.4,
                'mgno3_mg': 9.48,
                'mgno3_no3': 10.93,
                'cacl2_ca': 18.29,
                'cacl2_cl': 32.37},
  'n': 220.0,
  'no3': 200.0,
  'nh4': 20.0,
  'p': 40.0,
  'k': 180.0,
  'ca': 200.004,
  'mg': 50.0,
  's': 68.53,
  'cl': 10.0,
  'cano3': 11.453,
  'kno3': 3.187,
  'nh4no3': 1.143,
  'mgso4': 6.596,
  'kh2po4': 1.757,
  'k2so4': 0.139,
  'mgno3': 0,
  'cacl2': 0.309}
        
        for i in self.profile.macro:
            self.assertTrue(
                tt[i] == round(getattr(self.profile, i), 3)
            )

        for k, i in self.profile.salt_gramms.items():
            self.assertTrue(
                tt[k] == round(getattr(self.profile, i)(), 3)
            )
        for i in self.profile.salt:
            self.assertTrue(
                tt['persents'][i] == round(getattr(self.profile, i), 3)
            )
    def test_calc_ch_kh2po4_k(self):
        pushed_elemet = 'kh2po4_k'
        val = 10
        # 0,4
        setattr(self.profile, pushed_elemet, val)
        self.profile.calc_macro(pushed_element=pushed_elemet, val=val)
        print_macro(self)
        tt = {
            'persents': { 'cano3_ca': 16.97,
                'cano3_no3': 11.86,
                'cano3_nh4': 0.0,
                'kno3_k': 38.67,
                'kno3_no3': 13.85,
                'nh4no3_nh4': 17.5,
                'nh4no3_no3': 17.5,
                'mgso4_mg': 9.86,
                'mgso4_s': 13.01,
                'kh2po4_k': 10,
                'kh2po4_p': 7.922,
                'k2so4_k': 44.87,
                'k2so4_s': 18.4,
                'mgno3_mg': 9.48,
                'mgno3_no3': 10.93,
                'cacl2_ca': 18.29,
                'cacl2_cl': 32.37},
  'n': 220.0,
  'no3': 200.0,
  'nh4': 20.0,
  'p': 40.0,
  'k': 180.0,
  'ca': 200.004,
  'mg': 50.0,
  's': 68.53,
  'cl': 10.0,
  'cano3': 11.453,
  'kno3': 3.188,
  'nh4no3': 1.143,
  'mgso4': 5.071,
  'kh2po4': 5.049,
  'k2so4': 0.139,
  'mgno3': 0,
  'cacl2': 0.309}

        
        for i in self.profile.macro:
            self.assertTrue(
                tt[i] == round(getattr(self.profile, i), 3)
            )

        for k, i in self.profile.salt_gramms.items():
            self.assertTrue(
                tt[k] == round(getattr(self.profile, i)(), 3)
            )
        for i in self.profile.salt:
            self.assertTrue(
                tt['persents'][i] == round(getattr(self.profile, i), 3)
            )
    def test_calc_ch_kh2po4_p(self):
        pushed_elemet = 'kh2po4_p'
        val = 10
        # 0,4
        setattr(self.profile, pushed_elemet, val)
        self.profile.calc_macro(pushed_element=pushed_elemet, val=val)
        print_macro(self)
        tt = { 'persents': { 'cano3_ca': 16.97,
                'cano3_no3': 11.86,
                'cano3_nh4': 0.0,
                'kno3_k': 38.67,
                'kno3_no3': 13.85,
                'nh4no3_nh4': 17.5,
                'nh4no3_no3': 17.5,
                'mgso4_mg': 9.86,
                'mgso4_s': 13.01,
                'kh2po4_k': 12.623,
                'kh2po4_p': 10,
                'k2so4_k': 44.87,
                'k2so4_s': 18.4,
                'mgno3_mg': 9.48,
                'mgno3_no3': 10.93,
                'cacl2_ca': 18.29,
                'cacl2_cl': 32.37},
  'n': 220.0,
  'no3': 200.0,
  'nh4': 20.0,
  'p': 40.0,
  'k': 180.0,
  'ca': 200.004,
  'mg': 50.0,
  's': 68.53,
  'cl': 10.0,
  'cano3': 11.453,
  'kno3': 3.188,
  'nh4no3': 1.143,
  'mgso4': 5.071,
  'kh2po4': 4.0,
  'k2so4': 0.139,
  'mgno3': 0,
  'cacl2': 0.309}

        
        for i in self.profile.macro:
            self.assertTrue(
                tt[i] == round(getattr(self.profile, i), 3)
            )

        for k, i in self.profile.salt_gramms.items():
            self.assertTrue(
                tt[k] == round(getattr(self.profile, i)(), 3)
            )
        for i in self.profile.salt:
            self.assertTrue(
                tt['persents'][i] == round(getattr(self.profile, i), 3)
            )
    def test_calc_ch_k2so4_k(self):
        pushed_elemet = 'k2so4_k'
        val = 10
        # 0,4
        setattr(self.profile, pushed_elemet, val)
        self.profile.calc_macro(pushed_element=pushed_elemet, val=val)
        print_macro(self)
        tt = {
            'persents': { 'cano3_ca': 16.97,
                'cano3_no3': 11.86,
                'cano3_nh4': 0.0,
                'kno3_k': 38.67,
                'kno3_no3': 13.85,
                'nh4no3_nh4': 17.5,
                'nh4no3_no3': 17.5,
                'mgso4_mg': 9.86,
                'mgso4_s': 13.01,
                'kh2po4_k': 28.73,
                'kh2po4_p': 22.76,
                'k2so4_k': 10,
                'k2so4_s': 4.101,
                'mgno3_mg': 9.48,
                'mgno3_no3': 10.93,
                'cacl2_ca': 18.29,
                'cacl2_cl': 32.37},
              'n': 220.0,
              'no3': 200.0,
              'nh4': 20.0,
              'p': 40.0,
              'k': 180.0,
              'ca': 200.004,
              'mg': 50.0,
              's': 68.53,
              'cl': 10.0,
              'cano3': 11.453,
              'kno3': 3.188,
              'nh4no3': 1.143,
              'mgso4': 5.071,
              'kh2po4': 1.757,
              'k2so4': 0.623,
              'mgno3': 0,
              'cacl2': 0.309}

        
        for i in self.profile.macro:
            self.assertTrue(
                tt[i] == round(getattr(self.profile, i), 3)
            )

        for k, i in self.profile.salt_gramms.items():
            self.assertTrue(
                tt[k] == round(getattr(self.profile, i)(), 3)
            )
        for i in self.profile.salt:
            self.assertTrue(
                tt['persents'][i] == round(getattr(self.profile, i), 3)
            )
    def test_calc_ch_k2so4_s(self):
        pushed_elemet = 'k2so4_s'
        val = 10
        # 0,4
        setattr(self.profile, pushed_elemet, val)
        self.profile.calc_macro(pushed_element=pushed_elemet, val=val)
        print_macro(self)
        tt = { 'persents': { 'cano3_ca': 16.97,
                'cano3_no3': 11.86,
                'cano3_nh4': 0.0,
                'kno3_k': 38.67,
                'kno3_no3': 13.85,
                'nh4no3_nh4': 17.5,
                'nh4no3_no3': 17.5,
                'mgso4_mg': 9.86,
                'mgso4_s': 13.01,
                'kh2po4_k': 28.73,
                'kh2po4_p': 22.76,
                'k2so4_k': 24.387,
                'k2so4_s': 10,
                'mgno3_mg': 9.48,
                'mgno3_no3': 10.93,
                'cacl2_ca': 18.29,
                'cacl2_cl': 32.37},
  'n': 220.0,
  'no3': 200.0,
  'nh4': 20.0,
  'p': 40.0,
  'k': 180.0,
  'ca': 200.004,
  'mg': 50.0,
  's': 68.53,
  'cl': 10.0,
  'cano3': 11.453,
  'kno3': 3.188,
  'nh4no3': 1.143,
  'mgso4': 5.071,
  'kh2po4': 1.757,
  'k2so4': 0.256,
  'mgno3': 0,
  'cacl2': 0.309}

        
        for i in self.profile.macro:
            self.assertTrue(
                tt[i] == round(getattr(self.profile, i), 3)
            )

        for k, i in self.profile.salt_gramms.items():
            self.assertTrue(
                tt[k] == round(getattr(self.profile, i)(), 3)
            )
        for i in self.profile.salt:
            self.assertTrue(
                tt['persents'][i] == round(getattr(self.profile, i), 3)
            )

    def test_calc_ch_mgno3_mg(self):
        pushed_elemet = 'mgno3_mg'
        val = 10
        # 0,4
        setattr(self.profile, pushed_elemet, val)
        self.profile.calc_macro(pushed_element=pushed_elemet, val=val)
        print_macro(self)
        tt = {
            'persents': {'cano3_ca': 16.97,
                         'cano3_no3': 11.86,
                         'cano3_nh4': 0.0,
                         'kno3_k': 38.67,
                         'kno3_no3': 13.85,
                         'nh4no3_nh4': 17.5,
                         'nh4no3_no3': 17.5,
                         'mgso4_mg': 9.86,
                         'mgso4_s': 13.01,
                         'kh2po4_k': 28.73,
                         'kh2po4_p': 22.76,
                         'k2so4_k': 44.87,
                         'k2so4_s': 18.4,
                         'mgno3_mg': 10,
                         'mgno3_no3': 11.526,
                         'cacl2_ca': 18.29,
                         'cacl2_cl': 32.37},
                            'n': 220.0,
                            'no3': 200.0,
                            'nh4': 20.0,
                            'p': 40.0,
                            'k': 180.0,
                            'ca': 200.004,
                            'mg': 50.0,
                            's': 68.53,
                            'cl': 10.0,
                            'cano3': 11.453,
                            'kno3': 3.188,
                            'nh4no3': 1.143,
                            'mgso4': 5.071,
                            'kh2po4': 1.757,
                            'k2so4': 0.139,
                            'mgno3': 0,
                            'cacl2': 0.309}
    
        for i in self.profile.macro:
            self.assertTrue(
                tt[i] == round(getattr(self.profile, i), 3)
            )
    
        for k, i in self.profile.salt_gramms.items():
            self.assertTrue(
                tt[k] == round(getattr(self.profile, i)(), 3)
            )
        for i in self.profile.salt:
            self.assertTrue(
                tt['persents'][i] == round(getattr(self.profile, i), 3)
            )

    def test_calc_ch_mgno3_no3(self):
        pushed_elemet = 'mgno3_no3'
        val = 10
        # 0,4
        setattr(self.profile, pushed_elemet, val)
        self.profile.calc_macro(pushed_element=pushed_elemet, val=val)
        print_macro(self)
        tt = { 'persents': { 'cano3_ca': 16.97,
                'cano3_no3': 11.86,
                'cano3_nh4': 0.0,
                'kno3_k': 38.67,
                'kno3_no3': 13.85,
                'nh4no3_nh4': 17.5,
                'nh4no3_no3': 17.5,
                'mgso4_mg': 9.86,
                'mgso4_s': 13.01,
                'kh2po4_k': 28.73,
                'kh2po4_p': 22.76,
                'k2so4_k': 44.87,
                'k2so4_s': 18.4,
                'mgno3_mg': 8.676,
                'mgno3_no3': 10,
                'cacl2_ca': 18.29,
                'cacl2_cl': 32.37},
  'n': 220.0,
  'no3': 200.0,
  'nh4': 20.0,
  'p': 40.0,
  'k': 180.0,
  'ca': 200.004,
  'mg': 50.0,
  's': 68.53,
  'cl': 10.0,
  'cano3': 11.453,
  'kno3': 3.188,
  'nh4no3': 1.143,
  'mgso4': 5.071,
  'kh2po4': 1.757,
  'k2so4': 0.139,
  'mgno3': 0,
  'cacl2': 0.309}
    
        for i in self.profile.macro:
            self.assertTrue(
                tt[i] == round(getattr(self.profile, i), 3)
            )
    
        for k, i in self.profile.salt_gramms.items():
            self.assertTrue(
                tt[k] == round(getattr(self.profile, i)(), 3)
            )
        for i in self.profile.salt:
            self.assertTrue(
                tt['persents'][i] == round(getattr(self.profile, i), 3)
            )
    def test_calc_ch_cacl2_ca(self):
        pushed_elemet = 'cacl2_ca'
        val = 10
        # 0,4
        setattr(self.profile, pushed_elemet, val)
        self.profile.calc_macro(pushed_element=pushed_elemet, val=val)
        print_macro(self)
        tt ={ 'persents': { 'cano3_ca': 16.97,
                'cano3_no3': 11.86,
                'cano3_nh4': 0.0,
                'kno3_k': 38.67,
                'kno3_no3': 13.85,
                'nh4no3_nh4': 17.5,
                'nh4no3_no3': 17.5,
                'mgso4_mg': 9.86,
                'mgso4_s': 13.01,
                'kh2po4_k': 28.73,
                'kh2po4_p': 22.76,
                'k2so4_k': 44.87,
                'k2so4_s': 18.4,
                'mgno3_mg': 9.48,
                'mgno3_no3': 10.93,
                'cacl2_ca': 10,
                'cacl2_cl': 17.692},
  'n': 220.0,
  'no3': 200.0,
  'nh4': 20.0,
  'p': 40.0,
  'k': 180.0,
  'ca': 200.004,
  'mg': 50.0,
  's': 68.53,
  'cl': 10.0,
  'cano3': 11.453,
  'kno3': 3.188,
  'nh4no3': 1.143,
  'mgso4': 5.071,
  'kh2po4': 1.757,
  'k2so4': 0.139,
  'mgno3': 0,
  'cacl2': 0.565}

    
        for i in self.profile.macro:
            self.assertTrue(
                tt[i] == round(getattr(self.profile, i), 3)
            )
    
        for k, i in self.profile.salt_gramms.items():
            self.assertTrue(
                tt[k] == round(getattr(self.profile, i)(), 3)
            )
        for i in self.profile.salt:
            self.assertTrue(
                tt['persents'][i] == round(getattr(self.profile, i), 3)
            )
    def test_calc_ch_cacl2_cl(self):
        pushed_elemet = 'cacl2_cl'
        val = 10
        # 0,4
        setattr(self.profile, pushed_elemet, val)
        self.profile.calc_macro(pushed_element=pushed_elemet, val=val)
        print_macro(self)
        tt ={ 'persents': { 'cano3_ca': 16.97,
                'cano3_no3': 11.86,
                'cano3_nh4': 0.0,
                'kno3_k': 38.67,
                'kno3_no3': 13.85,
                'nh4no3_nh4': 17.5,
                'nh4no3_no3': 17.5,
                'mgso4_mg': 9.86,
                'mgso4_s': 13.01,
                'kh2po4_k': 28.73,
                'kh2po4_p': 22.76,
                'k2so4_k': 44.87,
                'k2so4_s': 18.4,
                'mgno3_mg': 9.48,
                'mgno3_no3': 10.93,
                'cacl2_ca': 5.652,
                'cacl2_cl': 10},
  'n': 220.0,
  'no3': 200.0,
  'nh4': 20.0,
  'p': 40.0,
  'k': 180.0,
  'ca': 200.004,
  'mg': 50.0,
  's': 68.53,
  'cl': 10.0,
  'cano3': 11.453,
  'kno3': 3.188,
  'nh4no3': 1.143,
  'mgso4': 5.071,
  'kh2po4': 1.757,
  'k2so4': 0.139,
  'mgno3': 0,
  'cacl2': 1.0}

    
        for i in self.profile.macro:
            self.assertTrue(
                tt[i] == round(getattr(self.profile, i), 3)
            )
    
        for k, i in self.profile.salt_gramms.items():
            self.assertTrue(
                tt[k] == round(getattr(self.profile, i)(), 3)
            )
        for i in self.profile.salt:
            self.assertTrue(
                tt['persents'][i] == round(getattr(self.profile, i), 3)
            )
    def test__change_cano3(self):
        pushed_elemet = 'cano3'
        val = 10
        # 0,4
        setattr(self.profile, pushed_elemet, val)
        self.profile.calc_macro(pushed_element=pushed_elemet, val=val)
        print_macro(self)
        tt ={ 'persents': { 'cano3_ca': 16.97,
                'cano3_no3': 11.86,
                'cano3_nh4': 0.0,
                'kno3_k': 38.67,
                'kno3_no3': 13.85,
                'nh4no3_nh4': 17.5,
                'nh4no3_no3': 17.5,
                'mgso4_mg': 9.86,
                'mgso4_s': 13.01,
                'kh2po4_k': 28.73,
                'kh2po4_p': 22.76,
                'k2so4_k': 44.87,
                'k2so4_s': 18.4,
                'mgno3_mg': 9.48,
                'mgno3_no3': 10.93,
                'cacl2_ca': 18.29,
                'cacl2_cl': 32.37},
          'n': 202.752,
          'no3': 182.752,
          'nh4': 20.0,
          'p': 40.0,
          'k': 180.0,
          'ca': 175.35,
          'mg': 50.0,
          's': 68.53,
          'cl': 10.0,
          'cano3': 10.0,
          'kno3': 3.188,
          'nh4no3': 1.143,
          'mgso4': 5.071,
          'kh2po4': 1.757,
          'k2so4': 0.139,
          'mgno3': 0,
          'cacl2': 0.309}

    
        for i in self.profile.macro:
            self.assertTrue(
                tt[i] == round(getattr(self.profile, i), 3)
            )
    
        for k, i in self.profile.salt_gramms.items():
            self.assertTrue(
                tt[k] == round(getattr(self.profile, i)(), 3)
            )
        for i in self.profile.salt:
            self.assertTrue(
                tt['persents'][i] == round(getattr(self.profile, i), 3)
            )
    def test__change_kno3(self):
        pushed_elemet = 'kno3'
        val = 10
        # 0,4
        setattr(self.profile, pushed_elemet, val)
        self.profile.calc_macro(pushed_element=pushed_elemet, val=val)
        print_macro(self)
        tt ={ 'persents': { 'cano3_ca': 16.97,
                'cano3_no3': 11.86,
                'cano3_nh4': 0.0,
                'kno3_k': 38.67,
                'kno3_no3': 13.85,
                'nh4no3_nh4': 17.5,
                'nh4no3_no3': 17.5,
                'mgso4_mg': 9.86,
                'mgso4_s': 13.01,
                'kh2po4_k': 28.73,
                'kh2po4_p': 22.76,
                'k2so4_k': 44.87,
                'k2so4_s': 18.4,
                'mgno3_mg': 9.48,
                'mgno3_no3': 10.93,
                'cacl2_ca': 18.29,
                'cacl2_cl': 32.37},
              'n': 314.33,
              'no3': 294.33,
              'nh4': 20.0,
              'p': 40.0,
              'k': 443.426,
              'ca': 200.004,
              'mg': 50.0,
              's': 68.53,
              'cl': 10.0,
              'cano3': 11.453,
              'kno3': 10.0,
              'nh4no3': 1.143,
              'mgso4': 5.071,
              'kh2po4': 1.757,
              'k2so4': 0.139,
              'mgno3': 0,
              'cacl2': 0.309}

    
        for i in self.profile.macro:
            self.assertTrue(
                tt[i] == round(getattr(self.profile, i), 3)
            )
    
        for k, i in self.profile.salt_gramms.items():
            self.assertTrue(
                tt[k] == round(getattr(self.profile, i)(), 3)
            )
        for i in self.profile.salt:
            self.assertTrue(
                tt['persents'][i] == round(getattr(self.profile, i), 3)
            )
    def test__change_nh4no3(self):
        pushed_elemet = 'nh4no3'
        val = 10
        # 0,4
        setattr(self.profile, pushed_elemet, val)
        self.profile.calc_macro(pushed_element=pushed_elemet, val=val)
        print_macro(self)
        tt = { 'persents': { 'cano3_ca': 16.97,
                'cano3_no3': 11.86,
                'cano3_nh4': 0.0,
                'kno3_k': 38.67,
                'kno3_no3': 13.85,
                'nh4no3_nh4': 17.5,
                'nh4no3_no3': 17.5,
                'mgso4_mg': 9.86,
                'mgso4_s': 13.01,
                'kh2po4_k': 28.73,
                'kh2po4_p': 22.76,
                'k2so4_k': 44.87,
                'k2so4_s': 18.4,
                'mgno3_mg': 9.48,
                'mgno3_no3': 10.93,
                'cacl2_ca': 18.29,
                'cacl2_cl': 32.37},
               'n': 529.982,
               'no3': 354.982,
               'nh4': 175.0,
               'p': 40.0,
               'k': 180.0,
               'ca': 200.004,
               'mg': 50.0,
               's': 68.53,
               'cl': 10.0,
               'cano3': 11.453,
               'kno3': 3.188,
               'nh4no3': 10.0,
               'mgso4': 5.071,
               'kh2po4': 1.757,
               'k2so4': 0.139,
               'mgno3': 0,
               'cacl2': 0.309}

    
        for i in self.profile.macro:
            self.assertTrue(
                tt[i] == round(getattr(self.profile, i), 3)
            )
    
        for k, i in self.profile.salt_gramms.items():
            self.assertTrue(
                tt[k] == round(getattr(self.profile, i)(), 3)
            )
        for i in self.profile.salt:
            self.assertTrue(
                tt['persents'][i] == round(getattr(self.profile, i), 3)
            )
    def test__change_mgso4(self):
        pushed_elemet = 'mgso4'
        val = 10
        # 0,4
        setattr(self.profile, pushed_elemet, val)
        self.profile.calc_macro(pushed_element=pushed_elemet, val=val)
        print_macro(self)
        tt = { 'persents': { 'cano3_ca': 16.97,
                'cano3_no3': 11.86,
                'cano3_nh4': 0.0,
                'kno3_k': 38.67,
                'kno3_no3': 13.85,
                'nh4no3_nh4': 17.5,
                'nh4no3_no3': 17.5,
                'mgso4_mg': 9.86,
                'mgso4_s': 13.01,
                'kh2po4_k': 28.73,
                'kh2po4_p': 22.76,
                'k2so4_k': 44.87,
                'k2so4_s': 18.4,
                'mgno3_mg': 9.48,
                'mgno3_no3': 10.93,
                'cacl2_ca': 18.29,
                'cacl2_cl': 32.37},
  'n': 219.982,
  'no3': 199.982,
  'nh4': 20.0,
  'p': 40.0,
  'k': 180.0,
  'ca': 200.004,
  'mg': 98.6,
  's': 132.668,
  'cl': 10.0,
  'cano3': 11.453,
  'kno3': 3.187,
  'nh4no3': 1.143,
  'mgso4': 10.0,
  'kh2po4': 1.757,
  'k2so4': 0.14,
  'mgno3': 0,
  'cacl2': 0.309}

    
        for i in self.profile.macro:
            self.assertTrue(
                tt[i] == round(getattr(self.profile, i), 3)
            )
    
        for k, i in self.profile.salt_gramms.items():
            self.assertTrue(
                tt[k] == round(getattr(self.profile, i)(), 3)
            )
        for i in self.profile.salt:
            self.assertTrue(
                tt['persents'][i] == round(getattr(self.profile, i), 3)
            )
    def test__change_kh2po4(self):
        pushed_elemet = 'kh2po4'
        val = 10
        # 0,4
        setattr(self.profile, pushed_elemet, val)
        self.profile.calc_macro(pushed_element=pushed_elemet, val=val)
        print_macro(self)
        tt = { 'persents': { 'cano3_ca': 16.97,
                'cano3_no3': 11.86,
                'cano3_nh4': 0.0,
                'kno3_k': 38.67,
                'kno3_no3': 13.85,
                'nh4no3_nh4': 17.5,
                'nh4no3_no3': 17.5,
                'mgso4_mg': 9.86,
                'mgso4_s': 13.01,
                'kh2po4_k': 28.73,
                'kh2po4_p': 22.76,
                'k2so4_k': 44.87,
                'k2so4_s': 18.4,
                'mgno3_mg': 9.48,
                'mgno3_no3': 10.93,
                'cacl2_ca': 18.29,
                'cacl2_cl': 32.37},
  'n': 219.982,
  'no3': 199.982,
  'nh4': 20.0,
  'p': 227.6,
  'k': 416.808,
  'ca': 200.004,
  'mg': 50.0,
  's': 68.53,
  'cl': 10.0,
  'cano3': 11.453,
  'kno3': 3.188,
  'nh4no3': 1.143,
  'mgso4': 5.071,
  'kh2po4': 10.0,
  'k2so4': 0.139,
  'mgno3': 0,
  'cacl2': 0.309}

    
        for i in self.profile.macro:
            self.assertTrue(
                tt[i] == round(getattr(self.profile, i), 3)
            )
    
        for k, i in self.profile.salt_gramms.items():
            self.assertTrue(
                tt[k] == round(getattr(self.profile, i)(), 3)
            )
        for i in self.profile.salt:
            self.assertTrue(
                tt['persents'][i] == round(getattr(self.profile, i), 3)
            )
    def test__change_mgno3(self):
        pushed_elemet = 'mgno3'
        val = 10
 
        setattr(self.profile, pushed_elemet, val)
        try:
            self.profile.calc_macro(pushed_element=pushed_elemet, val=val)
        except Exception as e:
            self.assertTrue(str(e) == "local variable 'n_nhno3' referenced before assignment")

    def test__change_cacl2(self):
        pushed_elemet = 'cacl2'
        val = 10
 
        setattr(self.profile, pushed_elemet, val)
        self.profile.calc_macro(pushed_element=pushed_elemet, val=val)
        print_macro(self)
        tt = { 'persents': { 'cano3_ca': 16.97,
                'cano3_no3': 11.86,
                'cano3_nh4': 0.0,
                'kno3_k': 38.67,
                'kno3_no3': 13.85,
                'nh4no3_nh4': 17.5,
                'nh4no3_no3': 17.5,
                'mgso4_mg': 9.86,
                'mgso4_s': 13.01,
                'kh2po4_k': 28.73,
                'kh2po4_p': 22.76,
                'k2so4_k': 44.87,
                'k2so4_s': 18.4,
                'mgno3_mg': 9.48,
                'mgno3_no3': 10.93,
                'cacl2_ca': 18.29,
                'cacl2_cl': 32.37},
  'n': 219.982,
  'no3': 199.982,
  'nh4': 20.0,
  'p': 40.0,
  'k': 180.0,
  'ca': 377.254,
  'mg': 50.0,
  's': 68.501,
  'cl': 323.7,
  'cano3': 11.453,
  'kno3': 3.19,
  'nh4no3': 1.143,
  'mgso4': 5.071,
  'kh2po4': 1.757,
  'k2so4': 0.137,
  'mgno3': 0,
  'cacl2': 10.0}
    
        for i in self.profile.macro:
            self.assertTrue(
                tt[i] == round(getattr(self.profile, i), 3)
            )
    
        for k, i in self.profile.salt_gramms.items():
            self.assertTrue(
                tt[k] == round(getattr(self.profile, i)(), 3)
            )
        for i in self.profile.salt:
            self.assertTrue(
                tt['persents'][i] == round(getattr(self.profile, i), 3)
            )

    def test__change_ec(self):
        pushed_elemet = 'ec'
        val = 2.5
        # 0,4
        setattr(self.profile, pushed_elemet, val)
        self.profile.calc_macro(pushed_element=pushed_elemet, val=val)
        print_macro(self)
        tt ={ 'persents': { 'cano3_ca': 16.97,
                'cano3_no3': 11.86,
                'cano3_nh4': 0.0,
                'kno3_k': 38.67,
                'kno3_no3': 13.85,
                'nh4no3_nh4': 17.5,
                'nh4no3_no3': 17.5,
                'mgso4_mg': 9.86,
                'mgso4_s': 13.01,
                'kh2po4_k': 28.73,
                'kh2po4_p': 22.76,
                'k2so4_k': 44.87,
                'k2so4_s': 18.4,
                'mgno3_mg': 9.48,
                'mgno3_no3': 10.93,
                'cacl2_ca': 18.29,
                'cacl2_cl': 32.37},
  'n': 265.789,
  'no3': 241.626,
  'nh4': 24.163,
  'p': 40.0,
  'k': 217.463,
  'ca': 241.631,
  'mg': 60.406,
  's': 88.044,
  'cl': 10.0,
  'cano3': 13.906,
  'kno3': 3.792,
  'nh4no3': 1.381,
  'mgso4': 6.126,
  'kh2po4': 1.757,
  'k2so4': 0.453,
  'mgno3': 0,
  'cacl2': 0.309}
    
        for i in self.profile.macro:
            self.assertTrue(
                tt[i] == round(getattr(self.profile, i), 3)
            )
    
        for k, i in self.profile.salt_gramms.items():
            self.assertTrue(
                tt[k] == round(getattr(self.profile, i)(), 3)
            )
        for i in self.profile.salt:
            self.assertTrue(
                tt['persents'][i] == round(getattr(self.profile, i), 3)
            )
    def test__change_litres(self):
        pushed_elemet = 'litres'
        val = 50
        setattr(self.profile, pushed_elemet, val)
        self.profile.calc_macro(pushed_element=pushed_elemet, val=val)
        print_macro(self)
        tt ={ 'persents': { 'cano3_ca': 16.97,
                'cano3_no3': 11.86,
                'cano3_nh4': 0.0,
                'kno3_k': 38.67,
                'kno3_no3': 13.85,
                'nh4no3_nh4': 17.5,
                'nh4no3_no3': 17.5,
                'mgso4_mg': 9.86,
                'mgso4_s': 13.01,
                'kh2po4_k': 28.73,
                'kh2po4_p': 22.76,
                'k2so4_k': 44.87,
                'k2so4_s': 18.4,
                'mgno3_mg': 9.48,
                'mgno3_no3': 10.93,
                'cacl2_ca': 18.29,
                'cacl2_cl': 32.37},
  'n': 220.0,
  'no3': 200.0,
  'nh4': 20.0,
  'p': 40.0,
  'k': 180.0,
  'ca': 200.004,
  'mg': 50.0,
  's': 68.53,
  'cl': 10.0,
  'cano3': 57.264,
  'kno3': 15.939,
  'nh4no3': 5.714,
  'mgso4': 25.355,
  'kh2po4': 8.787,
  'k2so4': 0.695,
  'mgno3': 0,
  'cacl2': 1.545}

    
        for i in self.profile.macro:
            self.assertTrue(
                tt[i] == round(getattr(self.profile, i), 3)
            )
    
        for k, i in self.profile.salt_gramms.items():
            self.assertTrue(
                tt[k] == round(getattr(self.profile, i)(), 3)
            )
        for i in self.profile.salt:
            self.assertTrue(
                tt['persents'][i] == round(getattr(self.profile, i), 3)
            )
    def test__change_micro_fe(self):
        pushed_elemet = 'fe'
        val = 7000
        setattr(self.profile, pushed_elemet, val)
        self.profile.calc_micro(pushed_element=pushed_elemet, val=val)
        print_micro(self)
        tt ={ 'persents': { 'dfe': 11.0,
                'dmn': 32.5,
                'db': 17.5,
                'dzn': 22.7,
                'dcu': 25.5,
                'dmo': 54.3,
                'dco': 13.0,
                'dsi': 7.0},
  'fe': 7000,
  'mn': 550.0,
  'b': 500.0,
  'zn': 60.0,
  'cu': 60.0,
  'mo': 60.0,
  'co': 50.0,
  'si': 0.0,
  'gfe': 0.636,
  'gmn': 0.017,
  'gb': 0.029,
  'gzn': 0.003,
  'gcu': 0.002,
  'gmo': 0.001,
  'gco': 0.004,
  'gsi': 0.0}

        for i in self.profile.micro:
            self.assertTrue(tt[i] == round(getattr(self.profile, i), 3))

        for i in self.profile.salt_micro_gramm:
            self.assertTrue(tt[i] == round(getattr(self.profile, i), 3))
            
        for i in self.profile.salt_micro_persent:
            self.assertTrue(tt['persents'][i] == round(getattr(self.profile, i), 3))
    def test__change_micro_mn(self):
        pushed_elemet = 'mn'
        val = 800
        setattr(self.profile, pushed_elemet, val)
        self.profile.calc_micro(pushed_element=pushed_elemet, val=val)
        print_micro(self)
        tt ={ 'persents': { 'dfe': 11.0,
                'dmn': 32.5,
                'db': 17.5,
                'dzn': 22.7,
                'dcu': 25.5,
                'dmo': 54.3,
                'dco': 13.0,
                'dsi': 7.0},
  'fe': 6000.0,
  'mn': 800,
  'b': 500.0,
  'zn': 60.0,
  'cu': 60.0,
  'mo': 60.0,
  'co': 50.0,
  'si': 0.0,
  'gfe': 0.545,
  'gmn': 0.025,
  'gb': 0.029,
  'gzn': 0.003,
  'gcu': 0.002,
  'gmo': 0.001,
  'gco': 0.004,
  'gsi': 0.0}

        for i in self.profile.micro:
            self.assertTrue(tt[i] == round(getattr(self.profile, i), 3))

        for i in self.profile.salt_micro_gramm:
            self.assertTrue(tt[i] == round(getattr(self.profile, i), 3))
            
        for i in self.profile.salt_micro_persent:
            self.assertTrue(tt['persents'][i] == round(getattr(self.profile, i), 3))
    def test__change_micro_b(self):
        pushed_elemet = 'b'
        val = 800
        setattr(self.profile, pushed_elemet, val)
        self.profile.calc_micro(pushed_element=pushed_elemet, val=val)
        print_micro(self)
        tt ={ 'persents': { 'dfe': 11.0,
                'dmn': 32.5,
                'db': 17.5,
                'dzn': 22.7,
                'dcu': 25.5,
                'dmo': 54.3,
                'dco': 13.0,
                'dsi': 7.0},
  'fe': 6000.0,
  'mn': 550.0,
  'b': 800,
  'zn': 60.0,
  'cu': 60.0,
  'mo': 60.0,
  'co': 50.0,
  'si': 0.0,
  'gfe': 0.545,
  'gmn': 0.017,
  'gb': 0.046,
  'gzn': 0.003,
  'gcu': 0.002,
  'gmo': 0.001,
  'gco': 0.004,
  'gsi': 0.0}

        for i in self.profile.micro:
            self.assertTrue(tt[i] == round(getattr(self.profile, i), 3))

        for i in self.profile.salt_micro_gramm:
            self.assertTrue(tt[i] == round(getattr(self.profile, i), 3))
            
        for i in self.profile.salt_micro_persent:
            self.assertTrue(tt['persents'][i] == round(getattr(self.profile, i), 3))
    def test__change_micro_zn(self):
        pushed_elemet = 'zn'
        val = 80
        setattr(self.profile, pushed_elemet, val)
        self.profile.calc_micro(pushed_element=pushed_elemet, val=val)
        print_micro(self)
        tt ={ 'persents': { 'dfe': 11.0,
                'dmn': 32.5,
                'db': 17.5,
                'dzn': 22.7,
                'dcu': 25.5,
                'dmo': 54.3,
                'dco': 13.0,
                'dsi': 7.0},
  'fe': 6000.0,
  'mn': 550.0,
  'b': 500.0,
  'zn': 80,
  'cu': 60.0,
  'mo': 60.0,
  'co': 50.0,
  'si': 0.0,
  'gfe': 0.545,
  'gmn': 0.017,
  'gb': 0.029,
  'gzn': 0.004,
  'gcu': 0.002,
  'gmo': 0.001,
  'gco': 0.004,
  'gsi': 0.0}

        for i in self.profile.micro:
            self.assertTrue(tt[i] == round(getattr(self.profile, i), 3))

        for i in self.profile.salt_micro_gramm:
            self.assertTrue(tt[i] == round(getattr(self.profile, i), 3))
            
        for i in self.profile.salt_micro_persent:
            self.assertTrue(tt['persents'][i] == round(getattr(self.profile, i), 3))
    def test__change_micro_cu(self):
        pushed_elemet = 'cu'
        val = 80
        setattr(self.profile, pushed_elemet, val)
        self.profile.calc_micro(pushed_element=pushed_elemet, val=val)
        print_micro(self)
        tt ={ 'persents': { 'dfe': 11.0,
                'dmn': 32.5,
                'db': 17.5,
                'dzn': 22.7,
                'dcu': 25.5,
                'dmo': 54.3,
                'dco': 13.0,
                'dsi': 7.0},
  'fe': 6000.0,
  'mn': 550.0,
  'b': 500.0,
  'zn': 60.0,
  'cu': 80,
  'mo': 60.0,
  'co': 50.0,
  'si': 0.0,
  'gfe': 0.545,
  'gmn': 0.017,
  'gb': 0.029,
  'gzn': 0.003,
  'gcu': 0.003,
  'gmo': 0.001,
  'gco': 0.004,
  'gsi': 0.0}

        for i in self.profile.micro:
            self.assertTrue(tt[i] == round(getattr(self.profile, i), 3))

        for i in self.profile.salt_micro_gramm:
            self.assertTrue(tt[i] == round(getattr(self.profile, i), 3))
            
        for i in self.profile.salt_micro_persent:
            self.assertTrue(tt['persents'][i] == round(getattr(self.profile, i), 3))
    def test__change_micro_mo(self):
        pushed_elemet = 'mo'
        val = 180
        setattr(self.profile, pushed_elemet, val)
        self.profile.calc_micro(pushed_element=pushed_elemet, val=val)
        print_micro(self)
        tt ={ 'persents': { 'dfe': 11.0,
                'dmn': 32.5,
                'db': 17.5,
                'dzn': 22.7,
                'dcu': 25.5,
                'dmo': 54.3,
                'dco': 13.0,
                'dsi': 7.0},
  'fe': 6000.0,
  'mn': 550.0,
  'b': 500.0,
  'zn': 60.0,
  'cu': 60.0,
  'mo': 180,
  'co': 50.0,
  'si': 0.0,
  'gfe': 0.545,
  'gmn': 0.017,
  'gb': 0.029,
  'gzn': 0.003,
  'gcu': 0.002,
  'gmo': 0.003,
  'gco': 0.004,
  'gsi': 0.0}

        for i in self.profile.micro:
            self.assertTrue(tt[i] == round(getattr(self.profile, i), 3))

        for i in self.profile.salt_micro_gramm:
            self.assertTrue(tt[i] == round(getattr(self.profile, i), 3))
            
        for i in self.profile.salt_micro_persent:
            self.assertTrue(tt['persents'][i] == round(getattr(self.profile, i), 3))
    def test__change_micro_co(self):
        pushed_elemet = 'co'
        val = 180
        setattr(self.profile, pushed_elemet, val)
        self.profile.calc_micro(pushed_element=pushed_elemet, val=val)
        print_micro(self)
        tt ={ 'persents': { 'dfe': 11.0,
                'dmn': 32.5,
                'db': 17.5,
                'dzn': 22.7,
                'dcu': 25.5,
                'dmo': 54.3,
                'dco': 13.0,
                'dsi': 7.0},
  'fe': 6000.0,
  'mn': 550.0,
  'b': 500.0,
  'zn': 60.0,
  'cu': 60.0,
  'mo': 60.0,
  'co': 180,
  'si': 0.0,
  'gfe': 0.545,
  'gmn': 0.017,
  'gb': 0.029,
  'gzn': 0.003,
  'gcu': 0.002,
  'gmo': 0.001,
  'gco': 0.014,
  'gsi': 0.0}

        for i in self.profile.micro:
            self.assertTrue(tt[i] == round(getattr(self.profile, i), 3))

        for i in self.profile.salt_micro_gramm:
            self.assertTrue(tt[i] == round(getattr(self.profile, i), 3))
            
        for i in self.profile.salt_micro_persent:
            self.assertTrue(tt['persents'][i] == round(getattr(self.profile, i), 3))
    def test__change_micro_zn(self):
        pushed_elemet = 'si'
        val = 180
        setattr(self.profile, pushed_elemet, val)
        self.profile.calc_micro(pushed_element=pushed_elemet, val=val)
        print_micro(self)
        tt = { 'persents': { 'dfe': 11.0,
                'dmn': 32.5,
                'db': 17.5,
                'dzn': 22.7,
                'dcu': 25.5,
                'dmo': 54.3,
                'dco': 13.0,
                'dsi': 7.0},
              'fe': 6000.0,
              'mn': 550.0,
              'b': 500.0,
              'zn': 60.0,
              'cu': 60.0,
              'mo': 60.0,
              'co': 50.0,
              'si': 180,
              'gfe': 0.545,
              'gmn': 0.017,
              'gb': 0.029,
              'gzn': 0.003,
              'gcu': 0.002,
              'gmo': 0.001,
              'gco': 0.004,
              'gsi': 0.026}

        for i in self.profile.micro:
            self.assertTrue(tt[i] == round(getattr(self.profile, i), 3))

        for i in self.profile.salt_micro_gramm:
            self.assertTrue(tt[i] == round(getattr(self.profile, i), 3))
            
        for i in self.profile.salt_micro_persent:
            self.assertTrue(tt['persents'][i] == round(getattr(self.profile, i), 3))
    def test__change_micro_d_fe(self):
        pushed_elemet = 'dfe'
        val = 15
        setattr(self.profile, pushed_elemet, val)
        self.profile.calc_micro(pushed_element=pushed_elemet, val=val)
        print_micro(self)
        tt = { 'persents': { 'dfe': 15,
                'dmn': 32.5,
                'db': 17.5,
                'dzn': 22.7,
                'dcu': 25.5,
                'dmo': 54.3,
                'dco': 13.0,
                'dsi': 7.0},
              'fe': 6000.0,
              'mn': 550.0,
              'b': 500.0,
              'zn': 60.0,
              'cu': 60.0,
              'mo': 60.0,
              'co': 50.0,
              'si': 0.0,
              'gfe': 0.4,
              'gmn': 0.017,
              'gb': 0.029,
              'gzn': 0.003,
              'gcu': 0.002,
              'gmo': 0.001,
              'gco': 0.004,
              'gsi': 0.0}


        for i in self.profile.micro:
            self.assertTrue(tt[i] == round(getattr(self.profile, i), 3))

        for i in self.profile.salt_micro_gramm:
            self.assertTrue(tt[i] == round(getattr(self.profile, i), 3))
            
        for i in self.profile.salt_micro_persent:
            self.assertTrue(tt['persents'][i] == round(getattr(self.profile, i), 3))
    def test__change_micro_d_mn(self):
        pushed_elemet = 'dmn'
        val = 15
        setattr(self.profile, pushed_elemet, val)
        self.profile.calc_micro(pushed_element=pushed_elemet, val=val)
        print_micro(self)
        tt = { 'persents': { 'dfe': 11.0,
                'dmn': 15,
                'db': 17.5,
                'dzn': 22.7,
                'dcu': 25.5,
                'dmo': 54.3,
                'dco': 13.0,
                'dsi': 7.0},
  'fe': 6000.0,
  'mn': 550.0,
  'b': 500.0,
  'zn': 60.0,
  'cu': 60.0,
  'mo': 60.0,
  'co': 50.0,
  'si': 0.0,
  'gfe': 0.545,
  'gmn': 0.037,
  'gb': 0.029,
  'gzn': 0.003,
  'gcu': 0.002,
  'gmo': 0.001,
  'gco': 0.004,
  'gsi': 0.0}


        for i in self.profile.micro:
            self.assertTrue(tt[i] == round(getattr(self.profile, i), 3))

        for i in self.profile.salt_micro_gramm:
            self.assertTrue(tt[i] == round(getattr(self.profile, i), 3))
            
        for i in self.profile.salt_micro_persent:
            self.assertTrue(tt['persents'][i] == round(getattr(self.profile, i), 3))
    def test__change_micro_d_b(self):
        pushed_elemet = 'db'
        val = 15
        setattr(self.profile, pushed_elemet, val)
        self.profile.calc_micro(pushed_element=pushed_elemet, val=val)
        print_micro(self)
        tt = { 'persents': { 'dfe': 11.0,
                'dmn': 32.5,
                'db': 15,
                'dzn': 22.7,
                'dcu': 25.5,
                'dmo': 54.3,
                'dco': 13.0,
                'dsi': 7.0},
  'fe': 6000.0,
  'mn': 550.0,
  'b': 500.0,
  'zn': 60.0,
  'cu': 60.0,
  'mo': 60.0,
  'co': 50.0,
  'si': 0.0,
  'gfe': 0.545,
  'gmn': 0.017,
  'gb': 0.033,
  'gzn': 0.003,
  'gcu': 0.002,
  'gmo': 0.001,
  'gco': 0.004,
  'gsi': 0.0}


        for i in self.profile.micro:
            self.assertTrue(tt[i] == round(getattr(self.profile, i), 3))

        for i in self.profile.salt_micro_gramm:
            self.assertTrue(tt[i] == round(getattr(self.profile, i), 3))
            
        for i in self.profile.salt_micro_persent:
            self.assertTrue(tt['persents'][i] == round(getattr(self.profile, i), 3))
    def test__change_micro_d_zn(self):
        pushed_elemet = 'dzn'
        val = 15
        setattr(self.profile, pushed_elemet, val)
        self.profile.calc_micro(pushed_element=pushed_elemet, val=val)
        print_micro(self)
        tt = { 'persents': { 'dfe': 11.0,
                'dmn': 32.5,
                'db': 17.5,
                'dzn': 15,
                'dcu': 25.5,
                'dmo': 54.3,
                'dco': 13.0,
                'dsi': 7.0},
  'fe': 6000.0,
  'mn': 550.0,
  'b': 500.0,
  'zn': 60.0,
  'cu': 60.0,
  'mo': 60.0,
  'co': 50.0,
  'si': 0.0,
  'gfe': 0.545,
  'gmn': 0.017,
  'gb': 0.029,
  'gzn': 0.004,
  'gcu': 0.002,
  'gmo': 0.001,
  'gco': 0.004,
  'gsi': 0.0}

        for i in self.profile.micro:
            self.assertTrue(tt[i] == round(getattr(self.profile, i), 3))

        for i in self.profile.salt_micro_gramm:
            self.assertTrue(tt[i] == round(getattr(self.profile, i), 3))
            
        for i in self.profile.salt_micro_persent:
            self.assertTrue(tt['persents'][i] == round(getattr(self.profile, i), 3))
    def test__change_micro_d_cu(self):
        pushed_elemet = 'dcu'
        val = 15
        setattr(self.profile, pushed_elemet, val)
        self.profile.calc_micro(pushed_element=pushed_elemet, val=val)
        print_micro(self)
        tt = { 'persents': { 'dfe': 11.0,
                'dmn': 32.5,
                'db': 17.5,
                'dzn': 22.7,
                'dcu': 15,
                'dmo': 54.3,
                'dco': 13.0,
                'dsi': 7.0},
  'fe': 6000.0,
  'mn': 550.0,
  'b': 500.0,
  'zn': 60.0,
  'cu': 60.0,
  'mo': 60.0,
  'co': 50.0,
  'si': 0.0,
  'gfe': 0.545,
  'gmn': 0.017,
  'gb': 0.029,
  'gzn': 0.003,
  'gcu': 0.004,
  'gmo': 0.001,
  'gco': 0.004,
  'gsi': 0.0}


        for i in self.profile.micro:
            self.assertTrue(tt[i] == round(getattr(self.profile, i), 3))

        for i in self.profile.salt_micro_gramm:
            self.assertTrue(tt[i] == round(getattr(self.profile, i), 3))
            
        for i in self.profile.salt_micro_persent:
            self.assertTrue(tt['persents'][i] == round(getattr(self.profile, i), 3))
    def test__change_micro_d_mo(self):
        pushed_elemet = 'dmo'
        val = 15
        setattr(self.profile, pushed_elemet, val)
        self.profile.calc_micro(pushed_element=pushed_elemet, val=val)
        print_micro(self)
        tt = { 'persents': { 'dfe': 11.0,
                'dmn': 32.5,
                'db': 17.5,
                'dzn': 22.7,
                'dcu': 25.5,
                'dmo': 15,
                'dco': 13.0,
                'dsi': 7.0},
  'fe': 6000.0,
  'mn': 550.0,
  'b': 500.0,
  'zn': 60.0,
  'cu': 60.0,
  'mo': 60.0,
  'co': 50.0,
  'si': 0.0,
  'gfe': 0.545,
  'gmn': 0.017,
  'gb': 0.029,
  'gzn': 0.003,
  'gcu': 0.002,
  'gmo': 0.004,
  'gco': 0.004,
  'gsi': 0.0}


        for i in self.profile.micro:
            self.assertTrue(tt[i] == round(getattr(self.profile, i), 3))

        for i in self.profile.salt_micro_gramm:
            self.assertTrue(tt[i] == round(getattr(self.profile, i), 3))
            
        for i in self.profile.salt_micro_persent:
            self.assertTrue(tt['persents'][i] == round(getattr(self.profile, i), 3))
    def test__change_micro_d_co(self):
        pushed_elemet = 'dco'
        val = 15
        setattr(self.profile, pushed_elemet, val)
        self.profile.calc_micro(pushed_element=pushed_elemet, val=val)
        print_micro(self)
        tt = { 'persents': { 'dfe': 11.0,
                'dmn': 32.5,
                'db': 17.5,
                'dzn': 22.7,
                'dcu': 25.5,
                'dmo': 54.3,
                'dco': 15,
                'dsi': 7.0},
  'fe': 6000.0,
  'mn': 550.0,
  'b': 500.0,
  'zn': 60.0,
  'cu': 60.0,
  'mo': 60.0,
  'co': 50.0,
  'si': 0.0,
  'gfe': 0.545,
  'gmn': 0.017,
  'gb': 0.029,
  'gzn': 0.003,
  'gcu': 0.002,
  'gmo': 0.001,
  'gco': 0.003,
  'gsi': 0.0}


        for i in self.profile.micro:
            self.assertTrue(tt[i] == round(getattr(self.profile, i), 3))

        for i in self.profile.salt_micro_gramm:
            self.assertTrue(tt[i] == round(getattr(self.profile, i), 3))
            
        for i in self.profile.salt_micro_persent:
            self.assertTrue(tt['persents'][i] == round(getattr(self.profile, i), 3))
    def test__change_micro_d_si(self):
        pushed_elemet = 'dsi'
        val = 15
        setattr(self.profile, pushed_elemet, val)
        self.profile.calc_micro(pushed_element=pushed_elemet, val=val)
        print_micro(self)
        tt = { 'persents': { 'dfe': 11.0,
                'dmn': 32.5,
                'db': 17.5,
                'dzn': 22.7,
                'dcu': 25.5,
                'dmo': 54.3,
                'dco': 13.0,
                'dsi': 15},
  'fe': 6000.0,
  'mn': 550.0,
  'b': 500.0,
  'zn': 60.0,
  'cu': 60.0,
  'mo': 60.0,
  'co': 50.0,
  'si': 0.0,
  'gfe': 0.545,
  'gmn': 0.017,
  'gb': 0.029,
  'gzn': 0.003,
  'gcu': 0.002,
  'gmo': 0.001,
  'gco': 0.004,
  'gsi': 0.0}

        for i in self.profile.micro:
            self.assertTrue(tt[i] == round(getattr(self.profile, i), 3))

        for i in self.profile.salt_micro_gramm:
            self.assertTrue(tt[i] == round(getattr(self.profile, i), 3))
            
        for i in self.profile.salt_micro_persent:
            self.assertTrue(tt['persents'][i] == round(getattr(self.profile, i), 3))
    def test__change_micro_g_fe(self):
        pushed_elemet = 'gfe'
        val = 0.9
        setattr(self.profile, pushed_elemet, val)
        self.profile.calc_micro(pushed_element=pushed_elemet, val=val)
        print_micro(self)
        tt = { 'persents': { 'dfe': 11.0,
                'dmn': 32.5,
                'db': 17.5,
                'dzn': 22.7,
                'dcu': 25.5,
                'dmo': 54.3,
                'dco': 13.0,
                'dsi': 7.0},
  'fe': 9900.0,
  'mn': 550.0,
  'b': 500.0,
  'zn': 60.0,
  'cu': 60.0,
  'mo': 60.0,
  'co': 50.0,
  'si': 0.0,
  'gfe': 0.9,
  'gmn': 0.017,
  'gb': 0.029,
  'gzn': 0.003,
  'gcu': 0.002,
  'gmo': 0.001,
  'gco': 0.004,
  'gsi': 0.0}

        for i in self.profile.micro:
            self.assertTrue(tt[i] == round(getattr(self.profile, i), 3))

        for i in self.profile.salt_micro_gramm:
            self.assertTrue(tt[i] == round(getattr(self.profile, i), 3))
            
        for i in self.profile.salt_micro_persent:
            self.assertTrue(tt['persents'][i] == round(getattr(self.profile, i), 3))
    def test__change_micro_g_mn(self):
        pushed_elemet = 'gmn'
        val = 0.9
        setattr(self.profile, pushed_elemet, val)
        self.profile.calc_micro(pushed_element=pushed_elemet, val=val)
        print_micro(self)
        tt ={ 'persents': { 'dfe': 11.0,
                'dmn': 32.5,
                'db': 17.5,
                'dzn': 22.7,
                'dcu': 25.5,
                'dmo': 54.3,
                'dco': 13.0,
                'dsi': 7.0},
  'fe': 6000.0,
  'mn': 29250.0,
  'b': 500.0,
  'zn': 60.0,
  'cu': 60.0,
  'mo': 60.0,
  'co': 50.0,
  'si': 0.0,
  'gfe': 0.545,
  'gmn': 0.9,
  'gb': 0.029,
  'gzn': 0.003,
  'gcu': 0.002,
  'gmo': 0.001,
  'gco': 0.004,
  'gsi': 0.0}


        for i in self.profile.micro:
            self.assertTrue(tt[i] == round(getattr(self.profile, i), 3))

        for i in self.profile.salt_micro_gramm:
            self.assertTrue(tt[i] == round(getattr(self.profile, i), 3))
            
        for i in self.profile.salt_micro_persent:
            self.assertTrue(tt['persents'][i] == round(getattr(self.profile, i), 3))
    def test__change_micro_g_b(self):
        pushed_elemet = 'gb'
        val = 0.9
        setattr(self.profile, pushed_elemet, val)
        self.profile.calc_micro(pushed_element=pushed_elemet, val=val)
        print_micro(self)
        tt = { 'persents': { 'dfe': 11.0,
                'dmn': 32.5,
                'db': 17.5,
                'dzn': 22.7,
                'dcu': 25.5,
                'dmo': 54.3,
                'dco': 13.0,
                'dsi': 7.0},
  'fe': 6000.0,
  'mn': 550.0,
  'b': 15750.0,
  'zn': 60.0,
  'cu': 60.0,
  'mo': 60.0,
  'co': 50.0,
  'si': 0.0,
  'gfe': 0.545,
  'gmn': 0.017,
  'gb': 0.9,
  'gzn': 0.003,
  'gcu': 0.002,
  'gmo': 0.001,
  'gco': 0.004,
  'gsi': 0.0}


        for i in self.profile.micro:
            self.assertTrue(tt[i] == round(getattr(self.profile, i), 3))

        for i in self.profile.salt_micro_gramm:
            self.assertTrue(tt[i] == round(getattr(self.profile, i), 3))
            
        for i in self.profile.salt_micro_persent:
            self.assertTrue(tt['persents'][i] == round(getattr(self.profile, i), 3))
    def test__change_micro_g_zn(self):
        pushed_elemet = 'gzn'
        val = 0.9
        setattr(self.profile, pushed_elemet, val)
        self.profile.calc_micro(pushed_element=pushed_elemet, val=val)
        print_micro(self)
        tt = { 'persents': { 'dfe': 11.0,
                'dmn': 32.5,
                'db': 17.5,
                'dzn': 22.7,
                'dcu': 25.5,
                'dmo': 54.3,
                'dco': 13.0,
                'dsi': 7.0},
  'fe': 6000.0,
  'mn': 550.0,
  'b': 500.0,
  'zn': 20430.0,
  'cu': 60.0,
  'mo': 60.0,
  'co': 50.0,
  'si': 0.0,
  'gfe': 0.545,
  'gmn': 0.017,
  'gb': 0.029,
  'gzn': 0.9,
  'gcu': 0.002,
  'gmo': 0.001,
  'gco': 0.004,
  'gsi': 0.0}

 

        for i in self.profile.micro:
            self.assertTrue(tt[i] == round(getattr(self.profile, i), 3))

        for i in self.profile.salt_micro_gramm:
            self.assertTrue(tt[i] == round(getattr(self.profile, i), 3))
            
        for i in self.profile.salt_micro_persent:
            self.assertTrue(tt['persents'][i] == round(getattr(self.profile, i), 3))
    def test__change_micro_g_cu(self):
        pushed_elemet = 'gcu'
        val = 0.9
        setattr(self.profile, pushed_elemet, val)
        self.profile.calc_micro(pushed_element=pushed_elemet, val=val)
        print_micro(self)
        tt ={ 'persents': { 'dfe': 11.0,
                'dmn': 32.5,
                'db': 17.5,
                'dzn': 22.7,
                'dcu': 25.5,
                'dmo': 54.3,
                'dco': 13.0,
                'dsi': 7.0},
  'fe': 6000.0,
  'mn': 550.0,
  'b': 500.0,
  'zn': 60.0,
  'cu': 22950.0,
  'mo': 60.0,
  'co': 50.0,
  'si': 0.0,
  'gfe': 0.545,
  'gmn': 0.017,
  'gb': 0.029,
  'gzn': 0.003,
  'gcu': 0.9,
  'gmo': 0.001,
  'gco': 0.004,
  'gsi': 0.0}

        for i in self.profile.micro:
            self.assertTrue(tt[i] == round(getattr(self.profile, i), 3))

        for i in self.profile.salt_micro_gramm:
            self.assertTrue(tt[i] == round(getattr(self.profile, i), 3))
            
        for i in self.profile.salt_micro_persent:
            self.assertTrue(tt['persents'][i] == round(getattr(self.profile, i), 3))
    def test__change_micro_g_mo(self):
        pushed_elemet = 'gmo'
        val = 0.9
        setattr(self.profile, pushed_elemet, val)
        self.profile.calc_micro(pushed_element=pushed_elemet, val=val)
        print_micro(self)
        tt ={ 'persents': { 'dfe': 11.0,
                'dmn': 32.5,
                'db': 17.5,
                'dzn': 22.7,
                'dcu': 25.5,
                'dmo': 54.3,
                'dco': 13.0,
                'dsi': 7.0},
  'fe': 6000.0,
  'mn': 550.0,
  'b': 500.0,
  'zn': 60.0,
  'cu': 60.0,
  'mo': 48870.0,
  'co': 50.0,
  'si': 0.0,
  'gfe': 0.545,
  'gmn': 0.017,
  'gb': 0.029,
  'gzn': 0.003,
  'gcu': 0.002,
  'gmo': 0.9,
  'gco': 0.004,
  'gsi': 0.0}

        for i in self.profile.micro:
            self.assertTrue(tt[i] == round(getattr(self.profile, i), 3))

        for i in self.profile.salt_micro_gramm:
            self.assertTrue(tt[i] == round(getattr(self.profile, i), 3))
            
        for i in self.profile.salt_micro_persent:
            self.assertTrue(tt['persents'][i] == round(getattr(self.profile, i), 3))
    def test__change_micro_g_co(self):
        pushed_elemet = 'gco'
        val = 0.9
        setattr(self.profile, pushed_elemet, val)
        self.profile.calc_micro(pushed_element=pushed_elemet, val=val)
        print_micro(self)
        tt = { 'persents': { 'dfe': 11.0,
                'dmn': 32.5,
                'db': 17.5,
                'dzn': 22.7,
                'dcu': 25.5,
                'dmo': 54.3,
                'dco': 13.0,
                'dsi': 7.0},
  'fe': 6000.0,
  'mn': 550.0,
  'b': 500.0,
  'zn': 60.0,
  'cu': 60.0,
  'mo': 60.0,
  'co': 11700.0,
  'si': 0.0,
  'gfe': 0.545,
  'gmn': 0.017,
  'gb': 0.029,
  'gzn': 0.003,
  'gcu': 0.002,
  'gmo': 0.001,
  'gco': 0.9,
  'gsi': 0.0}


        for i in self.profile.micro:
            self.assertTrue(tt[i] == round(getattr(self.profile, i), 3))

        for i in self.profile.salt_micro_gramm:
            self.assertTrue(tt[i] == round(getattr(self.profile, i), 3))
            
        for i in self.profile.salt_micro_persent:
            self.assertTrue(tt['persents'][i] == round(getattr(self.profile, i), 3))
    def test__change_micro_g_si(self):
        pushed_elemet = 'gsi'
        val = 0.9
        setattr(self.profile, pushed_elemet, val)
        self.profile.calc_micro(pushed_element=pushed_elemet, val=val)
        print_micro(self)
        tt = { 'persents': { 'dfe': 11.0,
                'dmn': 32.5,
                'db': 17.5,
                'dzn': 22.7,
                'dcu': 25.5,
                'dmo': 54.3,
                'dco': 13.0,
                'dsi': 7.0},
  'fe': 6000.0,
  'mn': 550.0,
  'b': 500.0,
  'zn': 60.0,
  'cu': 60.0,
  'mo': 60.0,
  'co': 50.0,
  'si': 6300.0,
  'gfe': 0.545,
  'gmn': 0.017,
  'gb': 0.029,
  'gzn': 0.003,
  'gcu': 0.002,
  'gmo': 0.001,
  'gco': 0.004,
  'gsi': 0.9}


        for i in self.profile.micro:
            self.assertTrue(tt[i] == round(getattr(self.profile, i), 3))

        for i in self.profile.salt_micro_gramm:
            self.assertTrue(tt[i] == round(getattr(self.profile, i), 3))
            
        for i in self.profile.salt_micro_persent:
            self.assertTrue(tt['persents'][i] == round(getattr(self.profile, i), 3))
    def test__change_micro_BOR_gb(self):
        
        pushed_elemet = 'weight_micro'
        val = 2
        setattr(self.profile, pushed_elemet, val)

        self.profile.micro_calc_mode = self.profile.CalcMicroMode.B
        self.profile.switch_micro_to_bor()
        self.profile.gmsum=None
        self.profile.calc_micro(pushed_element=pushed_elemet, val=val)
        print_micro(self)
        tt = { 'persents': { 'dfe': 9.985,
                'dmn': 0.915,
                'db': 0.832,
                'dzn': 0.1,
                'dcu': 0.1,
                'dmo': 0.1,
                'dco': 0.083,
                'dsi': 0},
              'fe': 19970.168,
              'mn': 1830.599,
              'b': 1664.181,
              'zn': 199.702,
              'cu': 199.702,
              'mo': 199.702,
              'co': 166.418,
              'si': 0.0,
              'gfe': 0.545,
              'gmn': 0.017,
              'gb': 0.029,
              'gzn': 0.003,
              'gcu': 0.002,
              'gmo': 0.001,
              'gco': 0.004,
              'gsi': 0.0}

        for i in self.profile.micro:
            self.assertTrue(tt[i] == round(getattr(self.profile, i), 3))

        for i in self.profile.salt_micro_gramm:
            self.assertTrue(tt[i] == round(getattr(self.profile, i), 3))
            
        for i in self.profile.salt_micro_persent:
            self.assertTrue(tt['persents'][i] == round(getattr(self.profile, i), 3))
    def test__change_micro_BOR_to_NORMAL(self):
        
        pushed_elemet = 'weight_micro'
        val = 2
        setattr(self.profile, pushed_elemet, val)

        self.profile.micro_calc_mode = self.profile.CalcMicroMode.B
        self.profile.switch_micro_to_bor()
        self.profile.gmsum=None
        self.profile.calc_micro(pushed_element=pushed_elemet, val=val)
        print_micro(self)
        tt = { 'persents': { 'dfe': 9.985,
                'dmn': 0.915,
                'db': 0.832,
                'dzn': 0.1,
                'dcu': 0.1,
                'dmo': 0.1,
                'dco': 0.083,
                'dsi': 0},
              'fe': 19970.168,
              'mn': 1830.599,
              'b': 1664.181,
              'zn': 199.702,
              'cu': 199.702,
              'mo': 199.702,
              'co': 166.418,
              'si': 0.0,
              'gfe': 0.545,
              'gmn': 0.017,
              'gb': 0.029,
              'gzn': 0.003,
              'gcu': 0.002,
              'gmo': 0.001,
              'gco': 0.004,
              'gsi': 0.0}

        for i in self.profile.micro:
            self.assertTrue(tt[i] == round(getattr(self.profile, i), 3))

        for i in self.profile.salt_micro_gramm:
            self.assertTrue(tt[i] == round(getattr(self.profile, i), 3))
            
        for i in self.profile.salt_micro_persent:
            self.assertTrue(tt['persents'][i] == round(getattr(self.profile, i), 3))

        self.profile.micro_calc_mode = self.profile.CalcMicroMode.U
        self.profile.switch_micro_to_all()
        self.profile.gmsum = None
        self.profile.calc_micro(pushed_element='b', val=tt['b'])
        print_micro(self)
        tt = { 'persents': { 'dfe': 11.0,
                'dmn': 32.5,
                'db': 17.5,
                'dzn': 22.7,
                'dcu': 25.5,
                'dmo': 54.3,
                'dco': 13.0,
                'dsi': 7.0},
  'fe': 19970.168,
  'mn': 1830.599,
  'b': 1664.181,
  'zn': 199.702,
  'cu': 199.702,
  'mo': 199.702,
  'co': 166.418,
  'si': 0.0,
  'gfe': 1.815,
  'gmn': 0.056,
  'gb': 0.095,
  'gzn': 0.009,
  'gcu': 0.008,
  'gmo': 0.004,
  'gco': 0.013,
  'gsi': 0.0}
        for i in self.profile.micro:
            self.assertTrue(tt[i] == round(getattr(self.profile, i), 3))

        for i in self.profile.salt_micro_gramm:
            self.assertTrue(tt[i] == round(getattr(self.profile, i), 3))

        for i in self.profile.salt_micro_persent:
            self.assertTrue(tt['persents'][i] == round(getattr(self.profile, i), 3))

    def test__change_micro_text(self):
    
        pushed_elemet = 'weight_micro'
        val = 2
        setattr(self.profile, pushed_elemet, val)
    
        self.profile.micro_calc_mode = self.profile.CalcMicroMode.B
        self.profile.switch_micro_to_bor()
        self.profile.gmsum = None
        self.profile.calc_micro(pushed_element=pushed_elemet, val=val)
        print_micro(self)
        tt = {'persents': {'dfe': 9.985,
                           'dmn': 0.915,
                           'db': 0.832,
                           'dzn': 0.1,
                           'dcu': 0.1,
                           'dmo': 0.1,
                           'dco': 0.083,
                           'dsi': 0},
              'fe': 19970.168,
              'mn': 1830.599,
              'b': 1664.181,
              'zn': 199.702,
              'cu': 199.702,
              'mo': 199.702,
              'co': 166.418,
              'si': 0.0,
              'gfe': 0.545,
              'gmn': 0.017,
              'gb': 0.029,
              'gzn': 0.003,
              'gcu': 0.002,
              'gmo': 0.001,
              'gco': 0.004,
              'gsi': 0.0}
    
        for i in self.profile.micro:
            self.assertTrue(tt[i] == round(getattr(self.profile, i), 3))
    
        for i in self.profile.salt_micro_gramm:
            self.assertTrue(tt[i] == round(getattr(self.profile, i), 3))
    
        for i in self.profile.salt_micro_persent:
            self.assertTrue(tt['persents'][i] == round(getattr(self.profile, i), 3))

        setattr(self.profile, 'v_micro', 1000)
        self.profile.calc_micro(pushed_element='v_micro', val=1000)
        # self.profile.micro_text
        print(self.profile.micro_text)
        self.assertTrue(self.profile.micro_text == "Концентрация: 2.0 г/л,Кратность: 10:1,Расход: 100.0 мл/л раствора")
        self.profile.micro_calc_mode = self.profile.CalcMicroMode.U
        self.profile.switch_micro_to_all()
        self.profile.calc_micro(pushed_element='v_micro', val=1000)
        self.assertTrue(self.profile.micro_text == "Концентрация: 2.0 г/л,Кратность: 10:1,Расход: 100.0 мл/л раствора")
        print('self.profile.micro_sostav', self.profile.micro_sostav)
        self.assertTrue(self.profile.micro_sostav == "Состав: Fe=9.985% Mn=0.915% B=0.832% Zn=0.1% Cu=0.1% Mo=0.1% Co=0.083% Si=0.0%")

        
            
            
            
    
            
   
    
 
        
        

      


class TestWithMg(TestCase):
    
    def setUp(self):
     
        self.user = User.objects.create_user(username='test_user', password='12345')
        # login = self.client.login(username='testuser', password='12345')
        fields =  {'name': 'for_test.hpg', 'n': '220.00', 'nh4': '20.00', 'no3': '200.00', 'p': '40.00', 'k': '180.00', 'ca': '200.00', 'mg': '50.00', 's': '68.53', 'cl': '10.00', 'cano3_ca': '16.97', 'cano3_no3': '11.86', 'cano3_nh4': '0.00', 'kno3_k': '38.67', 'kno3_no3': '13.85', 'nh4no3_nh4': '17.50', 'nh4no3_no3': '17.50', 'mgso4_mg': '9.86', 'mgso4_s': '13.01', 'kh2po4_k': '28.73', 'kh2po4_p': '22.76', 'k2so4_k': '44.87', 'k2so4_s': '18.40', 'mgno3_mg': '9.48', 'mgno3_no3': '10.93', 'cacl2_ca': '18.29', 'cacl2_cl': '32.37', 'fe': '6000.00', 'mn': '550.00', 'b': '500.00', 'zn': '60.00', 'cu': '60.00', 'mo': '60.00', 'co': '50.00', 'si': '0.00', 'dfe': '11.00', 'dmn': '32.50', 'db': '17.50', 'dzn': '22.70', 'dcu': '25.50', 'dmo': '54.30', 'dco': '13.00', 'dsi': '7.00', 'gl_cano3': '600.00', 'gl_kno3': '250.00', 'gl_nh4no3': '100.00', 'gl_mgno3': '500.00', 'gl_mgso4': '600.00', 'gl_k2so4': '100.00', 'gl_kh2po4': '150.00', 'gl_cacl2': '100.00', 'gl_cmplx': '10.00', 'gl_fe': '10.00', 'gl_mn': '10.00', 'gl_b': '10.00', 'gl_zn': '10.00', 'gl_cu': '10.00', 'gl_mo': '10.00', 'gl_co': '10.00', 'gl_si': '10.00', 'gml_cano3': '1.28', 'gml_kno3': '1.00', 'gml_nh4no3': '1.00', 'gml_mgno3': '1.00', 'gml_mgso4': '1.00', 'gml_k2so4': '1.00', 'gml_kh2po4': '1.00', 'gml_cacl2': '1.00', 'gml_cmplx': '1.00', 'gml_fe': '1.00', 'gml_mn': '1.00', 'gml_b': '1.00', 'gml_zn': '1.00', 'gml_cu': '1.00', 'gml_mo': '1.00', 'gml_co': '1.00', 'gml_si': '1.00', 'micro_calc_mode': 'u', 'calc_mode': 'Mg', 'litres': '10.00', 'taml': '1000.00', 'tbml': '1000.00', 'ec': 0, 'ppm': 0, 'user_id': 1}
        pp = PlantProfile(**fields)
        pp.save()
        self.profile = PlantProfile.objects.get(pk=pp.pk)
    
    def tearDown(self):
        # Очистка после каждого метода
        pass
    
    def test_calc_s(self):
        print(self.profile.calc_s())
        
    def test_kh2po4(self):
        t = round(self.profile.calc_kh2po4(), 5)
        self.assertTrue( t ==  1.75747)
    
    def test_kno3(self):
        t = round(self.profile.calc_kno3(), 5)
        self.assertTrue(t == 3.34905)
    
    def test_salt_cano3(self):
        t = round(self.profile.calc_cano3(), 5)
        self.assertTrue( t ==  11.4528 )
    
    def test_mgso4(self):
        t = round(self.profile.calc_mgso4(), 5)
        self.assertTrue(t ==  5.26749 )
    
    def test_nh4no3(self):
        t = round(self.profile.calc_nh4no3(), 5)
        self.assertTrue(t  == 1.14286  )
    
    def test_cacl2(self):
        t = round(self.profile.calc_cacl2(), 5)
        self.assertTrue(t == 0.30893 )
    
    def test_mgno3(self):
        t = round(self.profile.calc_mgno3(), 5)
        self.assertTrue( t ==  -0.20437 )


class TestMatrix(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='12345')
        # login = self.client.login(username='testuser', password='12345')
        fields =  {'name': 'for_test.hpg', 'n': '220.00', 'nh4': '20.00', 'no3': '200.00', 'p': '40.00', 'k': '180.00', 'ca': '200.00', 'mg': '50.00', 's': '68.53', 'cl': '10.00', 'cano3_ca': '16.97', 'cano3_no3': '11.86', 'cano3_nh4': '0.00', 'kno3_k': '38.67', 'kno3_no3': '13.85', 'nh4no3_nh4': '17.50', 'nh4no3_no3': '17.50', 'mgso4_mg': '9.86', 'mgso4_s': '13.01', 'kh2po4_k': '28.73', 'kh2po4_p': '22.76', 'k2so4_k': '44.87', 'k2so4_s': '18.40', 'mgno3_mg': '9.48', 'mgno3_no3': '10.93', 'cacl2_ca': '18.29', 'cacl2_cl': '32.37', 'fe': '6000.00', 'mn': '550.00', 'b': '500.00', 'zn': '60.00', 'cu': '60.00', 'mo': '60.00', 'co': '50.00', 'si': '0.00', 'dfe': '11.00', 'dmn': '32.50', 'db': '17.50', 'dzn': '22.70', 'dcu': '25.50', 'dmo': '54.30', 'dco': '13.00', 'dsi': '7.00', 'gl_cano3': '600.00', 'gl_kno3': '250.00', 'gl_nh4no3': '100.00', 'gl_mgno3': '500.00', 'gl_mgso4': '600.00', 'gl_k2so4': '100.00', 'gl_kh2po4': '150.00', 'gl_cacl2': '100.00', 'gl_cmplx': '10.00', 'gl_fe': '10.00', 'gl_mn': '10.00', 'gl_b': '10.00', 'gl_zn': '10.00', 'gl_cu': '10.00', 'gl_mo': '10.00', 'gl_co': '10.00', 'gl_si': '10.00', 'gml_cano3': '1.28', 'gml_kno3': '1.00', 'gml_nh4no3': '1.00', 'gml_mgno3': '1.00', 'gml_mgso4': '1.00', 'gml_k2so4': '1.00', 'gml_kh2po4': '1.00', 'gml_cacl2': '1.00', 'gml_cmplx': '1.00', 'gml_fe': '1.00', 'gml_mn': '1.00', 'gml_b': '1.00', 'gml_zn': '1.00', 'gml_cu': '1.00', 'gml_mo': '1.00', 'gml_co': '1.00', 'gml_si': '1.00', 'micro_calc_mode': 'u', 'calc_mode': 'Mg', 'litres': '10.00', 'taml': '1000.00', 'tbml': '1000.00', 'ec': 0, 'ppm': 0, 'user_id': 1}
        pp = PlantProfile(**fields)
        pp.save()
        self.profile = PlantProfile.objects.get(pk=pp.pk)
    
    def tearDown(self):
        # Очистка после каждого метода
        pass
    
    def test_calc_s(self):
        pushed_element = 'matrix-n-p'
        a = float(self.profile.n)
        b = float(self.profile.p)
        t_old = a / b
        t_new = 6
        c = a / t_new
    

 