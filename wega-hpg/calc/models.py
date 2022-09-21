import math
import uuid

import simplejson
from django.contrib.auth.models import User
from django.core.cache import cache
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html

from calc.decorators import float_exception


class MM:
    N = 14.0067
    P = 30.973762
    K = 39.0983
    Ca = 40.078
    Mg = 24.305
    S = 32.065
    Cl = 35.453
    O = 15.999
    H = 1.00784


# Create your models here.
class PlantProfile(models.Model):
    class CalcMode(models.TextChoices):
        K = 'K', _('Калий сернокислый K2SO4 ')
        Mg = 'Mg', _('Магний азотнокислый Mg(NO3)2*6H2O')
    
    class CalcMicroMode(models.TextChoices):
        U = 'u', _('Все микро соли')
        B = 'b', _('Комплекс по бору')
    
    def __str__(self):
        return f'{self.name} by {self.user}'

   
    macro = ['n', 'no3', 'nh4', 'p', 'k', 'ca', 'mg', 's', 'cl', ]
    macro_matrix = ['n', 'p', 'k', 'ca', 'mg', 's', ]
    micro = ['fe', 'mn', 'b', 'zn', 'cu', 'mo', 'co', 'si', ]
    salt_micro_gramm = ['gfe', 'gmn', 'gb', 'gzn', 'gcu', 'gmo', 'gco', 'gsi', ]
    salt_micro_persent = ['dfe', 'dmn', 'db', 'dzn', 'dcu', 'dmo', 'dco', 'dsi', ]
    salt_micro_persent_bor = ['agfe', 'agmn', 'agdb', 'agdzn', 'agdcu', 'agdmo', 'agdco', 'agdsi', ]
    salt_micro_dict = {
        'fe': {'name': "Железо", 'd': 'dfe', 'g': 'gfe'},
        'mn': {'name': "Марганец", 'd': 'dmn', 'g': 'gmn'},
        'b': {'name': "Бор", 'd': 'db', 'g': 'gb'},
        'zn': {'name': "Цинк", 'd': 'dzn', 'g': 'gzn'},
        'cu': {'name': "Медь", 'd': 'dcu', 'g': 'gcu'},
        'mo': {'name': "Молибден", 'd': 'dmo', 'g': 'gmo'},
        'co': {'name': "Кобальт", 'd': 'dco', 'g': 'gco'},
        'si': {'name': "Кремний", 'd': 'dsi', 'g': 'gsi'},
    }
    salt = ['cano3_ca', 'cano3_no3', 'cano3_nh4', 'kno3_k', 'kno3_no3', 'nh4no3_nh4', 'nh4no3_no3', 'mgso4_mg',
            'mgso4_s', 'kh2po4_k', 'kh2po4_p', 'k2so4_k', 'k2so4_s', 'mgno3_mg', 'mgno3_no3', 'cacl2_ca', 'cacl2_cl', ]
    salt_default = {'cano3_ca':16.972,
                    'cano3_no3':11.863,
                    'cano3_nh4':0.000,
                    'kno3_k':38.672,
                    'kno3_no3':13.853,
                    'nh4no3_nh4':17.5,
                    'nh4no3_no3':17.5,
                    'mgso4_mg':9.861,
                    'mgso4_s':13.011,
                    'kh2po4_k':28.731,
                    'kh2po4_p':22.761,
                    'k2so4_k':44.874,
                    'k2so4_s':18.401,
                    'mgno3_mg':9.483,
                    'mgno3_no3':10.930,
                    'cacl2_ca':18.294,
                    'cacl2_cl':32.366, }
    salt_gramms = {'cano3':'calc_cano3',
                   'kno3':'calc_kno3',
                   'nh4no3':'calc_nh4no3',
                   'mgso4':'calc_mgso4',
                   'kh2po4':'calc_kh2po4',
                   'k2so4':'calc_k2so4',
                   'mgno3':'calc_mgno3',
                   'cacl2':'calc_cacl2', }
    concentrate_dict_a = {
        'cano3':  {'name':'cano3', 'data':  ['gl_cano3', 'gml_cano3', ], 'calc_data': ['ml_cano3', 'gg_cano3']},
        'kno3':   {'name':'kno3', 'data':   ['gl_kno3', 'gml_kno3', ], 'calc_data': ['ml_kno3', 'gg_kno3']},
        'nh4no3': {'name':'nh4no3', 'data': ['gl_nh4no3', 'gml_nh4no3', ], 'calc_data': ['ml_nh4no3', 'gg_nh4no3']},
        'mgno3':  {'name':'mgno3', 'data':  ['gl_mgno3', 'gml_mgno3', ], 'calc_data': ['ml_mgno3', 'gg_mgno3']},
        'cacl2':  {'name':'cacl2', 'data':  ['gl_cacl2', 'gml_cacl2', ], 'calc_data': ['ml_cacl2', 'gg_cacl2']},
        
 
    }
    concentrate_fields = ['taml', 'tbml', 'gml_fe', 'gml_mn', 'gml_b', 'gml_zn', 'gml_cu', 'gml_mo', 'gml_co',
                          'gml_si', 'gml_cano3', 'gml_kno3', 'gml_nh4no3', 'gml_mgno3', 'gml_mgso4', 'gml_k2so4',
                          'gml_kh2po4', 'gml_cacl2', 'gml_cmplx', 'gl_fe', 'gl_mn', 'gl_b', 'gl_zn',
                          'gl_cu', 'gl_mo', 'gl_co', 'gl_si', 'gl_cano3', 'gl_kno3', 'gl_nh4no3', 'gl_mgno3',
                          'gl_mgso4', 'gl_k2so4', 'gl_kh2po4', 'gl_cacl2', 'gl_cmplx', 'ml_cano3', 'gg_cano3',
                          'ml_kno3', 'gg_kno3', 'ml_nh4no3', 'gg_nh4no3', 'ml_mgno3', 'gg_mgno3', 'ml_cacl2',
                          'gg_cacl2', 'ml_mgso4', 'ml_kh2po4', 'ml_k2so4', 'ml_fe', 'ml_mn', 'ml_b', 'ml_zn',
                          'ml_cu', 'ml_mo', 'ml_co', 'ml_si', 'ml_cmplx', 'gg_mgso4', 'gg_kh2po4', 'gg_k2so4',
                          'gg_fe', 'gg_mn', 'gg_b', 'gg_zn', 'gg_cu', 'gg_mo','gg_co', 'gg_si', 'gg_cmplx',

                          ]
    model_create_fields = macro + micro + salt_micro_gramm + salt_micro_persent + salt_micro_persent_bor + salt + concentrate_fields
    model_change_fields = macro + micro + salt_micro_gramm + salt_micro_persent + salt + concentrate_fields
    price_fields = [ 'p_cano3','p_kno3','p_nh4no3','p_mgso4','p_kh2po4','p_k2so4','p_mgno3','p_cacl2','p_fe',
                     'p_mn','p_b','p_zn','p_cu','p_mo','p_co','p_si','p_cmplx',]
    mkorr = ''
    corrections_macro = [
        'N', 'NO3', 'NH4',  'P', 'K', 'Ca', 'Mg', 'S', 'Cl', 'EC',
    ]
    correction_fields = {
        '0':['n_0','no3_0', 'nh4_0', 'p_0', 'k_0', 'ca_0','mg_0', 's_0','cl_0', 'ec_0',],
        '1':['n_1','no3_1', 'nh4_1', 'p_1', 'k_1', 'ca_1','mg_1', 's_1','cl_1', 'ec_1',],
        '2':['n_2','no3_2', 'nh4_2', 'p_2', 'k_2', 'ca_2','mg_2', 's_2','cl_2', 'ec_2',],
        'k':['n_k','no3_k', 'nh4_k', 'p_k', 'k_k', 'ca_k','mg_k', 's_k','cl_k', 'ec_k',],
    }
    correction_fields_all = [
        'ca_0', 'cl_0', 'ec_0', 'k_0', 'mg_0', 'n_0', 'nh4_0', 'no3_0', 'p_0', 's_0', 'v_0',
        'ca_1', 'cl_1', 'ec_1', 'k_1', 'mg_1', 'n_1', 'nh4_1', 'no3_1', 'p_1', 's_1', 'v_1',
        'ca_2', 'cl_2', 'ec_2', 'k_2', 'mg_2', 'n_2', 'nh4_2', 'no3_2', 'p_2', 's_2', 'v_2',
        'ca_k', 'cl_k', 'ec_k', 'k_k', 'mg_k', 'n_k', 'nh4_k', 'no3_k', 'p_k', 's_k', 'v_k'
    ]
    def concentrate_dict_b(self):
        concentrate_dict_b = {
            'mgso4': {'name': 'mgso4', 'data': ['gl_mgso4', 'gml_mgso4', ], 'calc_data': ['ml_mgso4', 'gg_mgso4']},
            'kh2po4': {'name': 'kh2po4', 'data': ['gl_kh2po4', 'gml_kh2po4', ], 'calc_data': ['ml_kh2po4', 'gg_kh2po4']},
            'k2so4': {'name': 'k2so4', 'data': ['gl_k2so4', 'gml_k2so4', ], 'calc_data': ['ml_k2so4', 'gg_k2so4']},
            'fe': {'name': 'fe', 'data': ['gl_fe', 'gml_fe', ], 'calc_data': ['ml_fe', 'gg_fe']},
            'mn': {'name': 'mn', 'data': ['gl_mn', 'gml_mn', ], 'calc_data': ['ml_mn', 'gg_mn']},
            'b': {'name': 'b', 'data': ['gl_b', 'gml_b', ], 'calc_data': ['ml_b', 'gg_b']},
            'zn': {'name': 'zn', 'data': ['gl_zn', 'gml_zn', ], 'calc_data': ['ml_zn', 'gg_zn']},
            'cu': {'name': 'cu', 'data': ['gl_cu', 'gml_cu', ], 'calc_data': ['ml_cu', 'gg_cu']},
            'mo': {'name': 'mo', 'data': ['gl_mo', 'gml_mo', ], 'calc_data': ['ml_mo', 'gg_mo']},
            'co': {'name': 'co', 'data': ['gl_co', 'gml_co', ], 'calc_data': ['ml_co', 'gg_co']},
            'si': {'name': 'si', 'data': ['gl_si', 'gml_si', ], 'calc_data': ['ml_si', 'gg_si']},
            'cmplx': {'name': 'cmplx', 'data': ['gl_cmplx', 'gml_cmplx', ], 'calc_data': ['ml_cmplx', 'gg_cmplx']},
        }
        return concentrate_dict_b
      
    mixer_dict={
        'cano3': {'calc':'calc_cano3', 'mixer': 'm_cano3', 'gram': 'gg_cano3', 'gl': 'gl_cano3', 'gml': 'gml_cano3', 'd': 'dcano3','p': 'p_cano3', 'calc_p': 'calc_p_cano3'},
        'kno3': {'calc':'calc_kno3', 'mixer': 'm_kno3', 'gram': 'gg_kno3', 'gl': 'gl_kno3', 'gml': 'gml_kno3', 'd': 'dkno3','p': 'p_kno3', 'calc_p': 'calc_p_kno3'},
        'nh4no3': {'calc':'calc_nh4no3', 'mixer': 'm_nh4no3', 'gram': 'gg_nh4no3', 'gl': 'gl_nh4no3', 'gml': 'gml_nh4no3', 'd': 'dnh4no3', 'p': 'p_nh4no3', 'calc_p': 'calc_p_nh4no3'},
        'mgso4': {'calc':'calc_mgso4', 'mixer': 'm_mgso4', 'gram': 'gg_mgso4', 'gl': 'gl_mgso4', 'gml': 'gml_mgso4', 'd': 'dmgso4', 'p': 'p_mgso4', 'calc_p': 'calc_p_mgso4'},
        'kh2po4': {'calc':'calc_kh2po4', 'mixer': 'm_kh2po4', 'gram': 'gg_kh2po4', 'gl': 'gl_kh2po4', 'gml': 'gml_kh2po4', 'd': 'dkh2po4', 'p': 'p_kh2po4', 'calc_p': 'calc_p_kh2po4'},
        'k2so4': {'calc':'calc_k2so4', 'mixer': 'm_k2so4', 'gram': 'gg_k2so4', 'gl': 'gl_k2so4', 'gml': 'gml_k2so4', 'd': 'dk2so4',  'p': 'p_k2so4', 'calc_p': 'calc_p_k2so4'},
        'mgno3': {'calc':'calc_mgno3', 'mixer': 'm_mgno3', 'gram': 'gg_mgno3', 'gl': 'gl_mgno3', 'gml': 'gml_mgno3', 'd': 'dmgno3', 'p': 'p_mgno3', 'calc_p': 'calc_p_mgno3'},
        'cacl2': {'calc':'calc_cacl2', 'mixer': 'm_cacl2', 'gram': 'gg_cacl2', 'gl': 'gl_cacl2', 'gml': 'gml_cacl2', 'd': 'dcacl2', 'p': 'p_cacl2', 'calc_p': 'calc_p_cacl2'},
        'fe': {'calc':'fe', 'mixer': 'm_fe', 'gram': 'gg_fe', 'gl': 'gl_fe', 'gml': 'gml_fe', 'd': 'dfe', 'p': 'p_fe', 'calc_p': 'calc_p_fe'},
        'mn': {'calc':'mn', 'mixer': 'm_mn', 'gram': 'gg_mn', 'gl': 'gl_mn', 'gml': 'gml_mn', 'd': 'dmn', 'p': 'p_mn', 'calc_p': 'calc_p_mn'},
        'b': {'calc':'b', 'mixer': 'm_b', 'gram': 'gg_b', 'gl': 'gl_b', 'gml': 'gml_b', 'd': 'db', 'p': 'p_b', 'calc_p': 'calc_p_b'},
        'zn': {'calc':'zn', 'mixer': 'm_zn', 'gram': 'gg_zn', 'gl': 'gl_zn', 'gml': 'gml_zn', 'd': 'dzn', 'p': 'p_zn', 'calc_p': 'calc_p_zn'},
        'cu': {'calc':'cu', 'mixer': 'm_cu', 'gram': 'gg_cu', 'gl': 'gl_cu', 'gml': 'gml_cu', 'd': 'dcu', 'p': 'p_cu', 'calc_p': 'calc_p_cu'},
        'mo': {'calc':'mo', 'mixer': 'm_mo', 'gram': 'gg_mo', 'gl': 'gl_mo', 'gml': 'gml_mo', 'd': 'dmo', 'p': 'p_mo', 'calc_p': 'calc_p_mo'},
        'co': {'calc':'co', 'mixer': 'm_co', 'gram': 'gg_co', 'gl': 'gl_co', 'gml': 'gml_co', 'd': 'dco', 'p': 'p_co', 'calc_p': 'calc_p_co'},
        'si': {'calc':'si', 'mixer': 'm_si', 'gram': 'gg_si', 'gl': 'gl_si', 'gml': 'gml_si', 'd': 'dsi', 'p': 'p_si', 'calc_p': 'calc_p_si'},
        'cmplx': {'calc':'cmplx', 'mixer': 'm_cmplx', 'gram': 'gg_cmplx', 'gl': 'gl_cmplx', 'gml': 'gml_cmplx', 'p': 'p_cmplx', 'calc_p': 'calc_p_cmplx'},
    }
    
    salt_dict = {
        'cano3':  { 'calc':'calc_cano3', 'salt': ['cano3_ca', 'cano3_no3', 'cano3_nh4', ], 'name': 'Кальций азотнокислый', 'formula': 'Са(NО3)2*4H2O'},
        'kno3':    { 'calc':'calc_kno3', 'salt': ['kno3_k', 'kno3_no3', ], 'name': 'Калий азотнокислый', 'formula': 'KNO3'},
        'nh4no3': { 'calc':'calc_nh4no3', 'salt': ['nh4no3_nh4', 'nh4no3_no3', ], 'name': 'Аммоний азотнокислый', 'formula': 'NH4NO3'},
        'mgso4':  { 'calc':'calc_mgso4', 'salt': ['mgso4_mg', 'mgso4_s', ], 'name': 'Магний сернокислый', 'formula': 'MgSO4*7H2O'},
        'kh2po4': { 'calc':'calc_kh2po4', 'salt': ['kh2po4_k', 'kh2po4_p', ], 'name': 'Калий фосфорнокислый', 'formula': 'KH2PO4'},
        'k2so4':  { 'calc':'calc_k2so4', 'salt': ['k2so4_k', 'k2so4_s', ], 'name': 'Калий сернокислый ', 'formula': 'K2SO4'},
        'mgno3':  { 'calc':'calc_mgno3', 'salt': ['mgno3_mg', 'mgno3_no3', ], 'name': 'Магний азотнокислый', 'formula': 'Mg(NO3)2*6H2O'},
        'cacl2':  { 'calc':'calc_cacl2', 'salt': ['cacl2_ca', 'cacl2_cl', ], 'name': 'Хлорид кальция 6-водный', 'formula': 'CaCl2*6H2O'},
    }

    def __init__(self, *args, **kwargs):
        super(PlantProfile, self).__init__(*args, **kwargs)
        if self.pk:
            self.saved_ec = self.calc_ec()
            if not self.ec:
                self.ec = self.calc_ec()
        
            self.recalc()
            for k, ii in self.correction_fields.items():
                for i in ii:
                    setattr(self, i , getattr(self, i.replace('_'+k, '')) )
            self.v_2 = self.litres + 20
            self.v_1 = self.litres
            self.v_k = self.litres + 10
            
            self.ec_2 = self.saved_ec
            self.ec_1 = self.saved_ec
            self.ec_k = self.saved_ec
    
    def save(self, *args, **kwargs):
        for i in self.salt:
            if not getattr(self,i) or (getattr(self,i) and float(getattr(self,i))<=0):
                setattr(self, i, self.salt_default.get(i))
        super(PlantProfile, self).save(args,kwargs)
    
    
    name = models.CharField(max_length=1024, verbose_name='Имя профиля')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ec = models.FloatField(default=0, verbose_name='Ec')
    ppm = models.FloatField(default=0, verbose_name='PPM')
    litres = models.FloatField(default=10, verbose_name='Литры')
    mixer_ip =   models.CharField(max_length=1024, default='mixer.local', verbose_name='Адрес/порт миксера')
    mixer_system_number = models.FloatField(default=1, null=True, blank=True, verbose_name='Номер системы куда нальется раствор')
    
    template = models.ForeignKey('PlantTemplate', on_delete=models.SET_NULL, null=True, blank=True)
    from_template = models.ForeignKey('PlantTemplate', on_delete=models.SET_NULL, null=True, blank=True,
                                      related_name='profile_from_template')
    calc_mode = models.CharField(max_length=2, choices=CalcMode.choices, default=CalcMode.K, )
    
    n = models.FloatField(default=0, verbose_name='N')
    no3 = models.FloatField(default=0, verbose_name='NO3')
    nh4 = models.FloatField(default=0, verbose_name='NH4')
    
    p = models.FloatField(default=0, verbose_name='P')
    k = models.FloatField(default=0, verbose_name='K')
    ca = models.FloatField(default=0, verbose_name='Ca')
    mg = models.FloatField(default=0, verbose_name='Mg')
    s = models.FloatField(default=0, verbose_name='S')
    cl = models.FloatField(default=0, verbose_name='Cl')
    
    fe = models.FloatField(default=0, verbose_name='Fe')
    mn = models.FloatField(default=0, verbose_name='Mn')
    b = models.FloatField(default=0, verbose_name='B')
    zn = models.FloatField(default=0, verbose_name='Zn')
    cu = models.FloatField(default=0, verbose_name='Cu')
    mo = models.FloatField(default=0, verbose_name='Mo')
    co = models.FloatField(default=0, verbose_name='Co')
    si = models.FloatField(default=0, verbose_name='Si')

    cano3 = models.FloatField(default=0, verbose_name='CaNO3')
    kno3 = models.FloatField(default=0, verbose_name='KNO3')
    nh4no3 = models.FloatField(default=0, verbose_name='Nh4NO3')
    mgso4 = models.FloatField(default=0, verbose_name='MgSO4')
    kh2po4 = models.FloatField(default=0, verbose_name='KH2PO4')
    k2so4 = models.FloatField(default=0, verbose_name='K2SO4')
    mgno3 = models.FloatField(default=0, verbose_name='MgNO3')
    cacl2 = models.FloatField(default=0, verbose_name='CaCl2')
    
    
    dfe = models.FloatField(default=0, verbose_name='Fe')
    dmn = models.FloatField(default=0, verbose_name='Mn')
    db = models.FloatField(default=0, verbose_name='B')
    dzn = models.FloatField(default=0, verbose_name='Zn')
    dcu = models.FloatField(default=0, verbose_name='Cu')
    dmo = models.FloatField(default=0, verbose_name='Mo')
    dco = models.FloatField(default=0, verbose_name='Co')
    dsi = models.FloatField(default=0, verbose_name='Si')
    
    gfe = models.FloatField(default=0, verbose_name='Fe')
    gmn = models.FloatField(default=0, verbose_name='Mn')
    gb = models.FloatField(default=0, verbose_name='B')
    gzn = models.FloatField(default=0, verbose_name='Zn')
    gcu = models.FloatField(default=0, verbose_name='Cu')
    gmo = models.FloatField(default=0, verbose_name='Mo')
    gco = models.FloatField(default=0, verbose_name='Co')
    gsi = models.FloatField(default=0, verbose_name='Si')
    
    cano3_ca = models.FloatField(default=0, verbose_name='CaNO3_Ca')
    cano3_no3 = models.FloatField(default=0, verbose_name='CaNO3_NO3')
    cano3_nh4 = models.FloatField(default=0, verbose_name='CaNO3_NH4')
    
    kno3_k = models.FloatField(default=0, verbose_name='KNO3_K')
    kno3_no3 = models.FloatField(default=0, verbose_name='KNO3_NO3')
    nh4no3_nh4 = models.FloatField(default=0, verbose_name='NH4NO3_NH4')
    nh4no3_no3 = models.FloatField(default=0, verbose_name='NH4NO3_NO3')
    mgso4_mg = models.FloatField(default=0, verbose_name='MgSO4_Mg')
    mgso4_s = models.FloatField(default=0, verbose_name='MgSO4_S')
    kh2po4_k = models.FloatField(default=0, verbose_name='KH2PO4_K')
    kh2po4_p = models.FloatField(default=0, verbose_name='KH2PO4_P')
    k2so4_k = models.FloatField(default=0, verbose_name='K2SO4_K')
    k2so4_s = models.FloatField(default=0, verbose_name='K2SO4_S')
    mgno3_mg = models.FloatField(default=0, verbose_name='MgNO3_Mg')
    mgno3_no3 = models.FloatField(default=0, verbose_name='MgNO3_NO3')
    cacl2_ca = models.FloatField(default=0, verbose_name='CaCl2_Ca')
    cacl2_cl = models.FloatField(default=0, verbose_name='CaCl2_Cl')
    
    nh4_nh3_ratio = models.FloatField(default=0.1, verbose_name='NH4:NH3')
    
    micro_calc_mode = models.CharField(max_length=2, choices=CalcMicroMode.choices, default=CalcMicroMode.U,
                                       verbose_name='Микро метод расчета')
    
    v_micro = models.FloatField(default=500, verbose_name='Объем микро')

    gl_cano3 = models.FloatField(default=600 )
    gl_kno3 = models.FloatField(default=250)
    gl_nh4no3 = models.FloatField(default=100)
    gl_mgno3  = models.FloatField(default=500)
    gl_mgso4 = models.FloatField(default=600)
    gl_k2so4 = models.FloatField(default=100)
    gl_kh2po4 = models.FloatField(default=150)
    gl_cacl2  = models.FloatField(default=100)
    gl_cmplx  = models.FloatField(default=10)
    
    gl_fe = models.FloatField(default=10)
    gl_mn = models.FloatField(default=10)
    gl_b = models.FloatField(default=10)
    gl_zn = models.FloatField(default=10)
    gl_cu = models.FloatField(default=10)
    gl_mo = models.FloatField(default=10)
    gl_co = models.FloatField(default=10)
    gl_si = models.FloatField(default=10)
    
    gml_cano3  = models.FloatField(default=1.2845)
    gml_kno3  = models.FloatField(default=1)
    gml_nh4no3  = models.FloatField(default=1)
    gml_mgno3  = models.FloatField(default=1)
    gml_mgso4  = models.FloatField(default=1)
    gml_k2so4  = models.FloatField(default=1)
    gml_kh2po4  = models.FloatField(default=1)
    gml_cacl2  = models.FloatField(default=1)
    gml_cmplx  = models.FloatField(default=1)
    
    gml_fe = models.FloatField(default=1)
    gml_mn = models.FloatField(default=1)
    gml_b  = models.FloatField(default=1)
    gml_zn = models.FloatField(default=1)
    gml_cu = models.FloatField(default=1)
    gml_mo = models.FloatField(default=1)
    gml_co = models.FloatField(default=1)
    gml_si = models.FloatField(default=1)

    taml = models.FloatField(default=1)
    tbml = models.FloatField(default=1)
    
    
    # mixer
    m_cano3 = models.CharField(max_length=10, blank=True, null=True, default='p1')
    m_kno3 = models.CharField(max_length=10, blank=True, null=True, default='p2')
    m_nh4no3 = models.CharField(max_length=10, blank=True, null=True, default='p3')
    m_mgso4 = models.CharField(max_length=10, blank=True, null=True, default='p4')
    m_kh2po4 = models.CharField(max_length=10, blank=True, null=True, default='p5')
    m_k2so4 = models.CharField(max_length=10, blank=True, null=True, default='p6')
    m_mgno3 = models.CharField(max_length=10, blank=True, null=True)
    m_cacl2 = models.CharField(max_length=10, blank=True, null=True)
    m_fe = models.CharField(max_length=10, blank=True, null=True)
    m_mn = models.CharField(max_length=10, blank=True, null=True)
    m_b = models.CharField(max_length=10, blank=True, null=True)
    m_zn = models.CharField(max_length=10, blank=True, null=True)
    m_cu = models.CharField(max_length=10, blank=True, null=True)
    m_mo = models.CharField(max_length=10, blank=True, null=True)
    m_co = models.CharField(max_length=10, blank=True, null=True)
    m_si = models.CharField(max_length=10, blank=True, null=True)
    m_cmplx = models.CharField(max_length=10, blank=True, null=True, default='p7')


    p_cano3 = models.FloatField(default=0.4000, blank=True, null=True)
    p_kno3 = models.FloatField(default=0.3500, blank=True, null=True)
    p_nh4no3 = models.FloatField(default=0.2500, blank=True, null=True)
    p_mgso4 = models.FloatField(default=0.3500, blank=True, null=True)
    p_kh2po4 = models.FloatField(default=0.1200, blank=True, null=True)
    p_k2so4 = models.FloatField(default=0.4000, blank=True, null=True)
    p_mgno3 = models.FloatField(default=0.3200, blank=True, null=True)
    p_cacl2 = models.FloatField(default=0.7700, blank=True, null=True)
    p_fe = models.FloatField(default=0.0500, blank=True, null=True)
    p_mn = models.FloatField(default=3.000, blank=True, null=True)
    p_b = models.FloatField(default=0.3000, blank=True, null=True)
    p_zn = models.FloatField(default=0.4000, blank=True, null=True)
    p_cu = models.FloatField(default=0.1500, blank=True, null=True)
    p_mo = models.FloatField(default=0.4000, blank=True, null=True)
    p_co = models.FloatField(default=3.0000, blank=True, null=True)
    p_si = models.FloatField(default=2.3000, blank=True, null=True)
    p_cmplx = models.FloatField(default=0.2700, blank=True, null=True)

    @float_exception
    def calcs(self, no3, nh4, p, k, ca, mg, cl):

      m = MM
      a = nh4 * m.Ca * m.Mg * m.K * m.P * m.Cl
      b = 2 * ca * m.N * m.Mg * m.K * m.P * m.Cl
      c = 2 * mg * m.N * m.Ca * m.K * m.P * m.Cl
      d = k * m.N * m.Ca * m.Mg * m.P * m.Cl
      e = no3 * m.Ca * m.Mg * m.K * m.P * m.Cl
      f = p * m.N * m.Ca * m.Mg * m.K * m.Cl
      g = cl * m.N * m.Ca * m.Mg * m.K * m.P
      h = 2 * m.N * m.Ca * m.Mg * m.K * m.P * m.Cl
      total = -m.S * (-a - b - c - d + e + f + g) / (h)
      return total

    @float_exception
    def calcec(self, nh4, k, ca, mg):
        m = MM()
        a = nh4 * m.Ca * m.Mg * m.K
        b = ca * m.N * m.Mg * m.K
        c = mg * m.N * m.Ca * m.K
        d = k * m.N * m.Ca * m.Mg
        e = m.N * m.Ca * m.Mg * m.K
        f = m.N * m.Ca * m.Mg * m.K
        ec = 0.095 * (a + 2 * b + 2 * c + d + 2 * e) / f
        return ec

    @float_exception
    def calc_correction(self, pushed_element=None, val=None):
        if pushed_element in self.correction_fields['0'] or pushed_element in self.correction_fields['2'] or pushed_element in ['v_1','v_2']:
            kec = None
            # // исходный
            if self.v_1 >= self.v_2:
                self.v_2 = self.v_1+self.v_k
    
            self.s_0 = self.calcs(self.no3_0,self.nh4_0,self.p_0,self.k_0,self.ca_0,self.mg_0,self.cl_0)
            self.ec_0 = self.calcec(self.nh4_0, self.k_0, self.ca_0, self.mg_0)
            self.n_0 = self.no3_0 + self.nh4_0;
    
            # // текущий
            
            if self.ec_0 != 0: kec = self.ec_1 / self.ec_0
            
            self.no3_1 = self.no3_0 * kec
            self.nh4_1 = self.nh4_0 * kec
            self.p_1 = self.p_0 * kec
            self.k_1 = self.k_0 * kec
            self.ca_1 = self.ca_0 * kec
            self.mg_1 = self.mg_0 * kec
            self.s_1 = self.s_0 * kec
            self.cl_1 = self.cl_0 * kec
            self.n_1 = self.no3_1 + self.nh4_1
            
            # // корректирующий
            self.v_k = self.v_2 - self.v_1
            self.no3_k = (self.no3_2 * self.v_2 - self.no3_1 * self.v_1) / self.v_k
            self.nh4_k = (self.nh4_2 * self.v_2 - self.nh4_1 * self.v_1) / self.v_k
            self.p_k = (self.p_2 * self.v_2 - self.p_1 * self.v_1) / self.v_k
            self.k_k = (self.k_2 * self.v_2 - self.k_1 * self.v_1) / self.v_k
            self.ca_k = (self.ca_2 * self.v_2 - self.ca_1 * self.v_1) / self.v_k
            self.mg_k = (self.mg_2 * self.v_2 - self.mg_1 * self.v_1) / self.v_k
            self.cl_k = (self.cl_2 * self.v_2 - self.cl_1 * self.v_1) / self.v_k
            
            self.s_k = self.calcs(self.no3_k,self.nh4_k,self.p_k,self.k_k,self.ca_k,self.mg_k,self.cl_k)
            
            # // self.ec_k = (self.ec_2 * self.v_2 - self.ec_1 * self.v_1) / self.v_k;
            
            self.ec_k = self.calcec(self.nh4_k,self.k_k,self.ca_k,self.mg_k)
            self.n_k = self.no3_k + self.nh4_k;
            # // итоговый
            
            self.s_2 = self.calcs(self.no3_2,self.nh4_2,self.p_2,self.k_2,self.ca_2,self.mg_2,self.cl_2)
            
            self.ec_2 = self.calcec(self.nh4_2,self.k_2,self.ca_2,self.mg_2)
            
            self.n_2 = self.no3_2 + self.nh4_2
            
            self.mkorr = f'основное:\n' \
                         f'изменение объема на: {round((self.v_2 - self.v_1) / self.v_1 * 100)}%\n' \
                         f'доля старого расвтора: {round((self.v_1 / self.v_2) * 100)}%\n' \
                         f'изменение ec на {round((self.ec_2 - self.ec_1) / self.ec_1 * 100)}%\n' \
                         f'изменение n общий на: {round((self.n_2 - self.n_1) / self.n_1 * 100)}%\n\n' \
                         f'профиль:' \
                         f'коррекция no3 на: {round((self.no3_2 - self.no3_1) / self.no3_1 * 100)}%\n' \
                         f'коррекция nh4 на: {round((self.nh4_2 - self.nh4_1) / self.nh4_1 * 100)}%\n' \
                         f'коррекция p на: {round((self.p_2 - self.p_1) / self.p_1 * 100)}%\n' \
                         f'коррекция k на: {round((self.k_2 - self.k_1) / self.k_1 * 100)}%\n' \
                         f'коррекция ca на: {round((self.ca_2 - self.ca_1) / self.ca_1 * 100)}%\n' \
                         f'коррекция mg на: {round((self.mg_2 - self.mg_1) / self.mg_1 * 100)}%\n' \
                         f'коррекция s на: {round((self.s_2 - self.s_1))}ppm\n' \
                         f'коррекция cl на: {round((self.cl_2 - self.cl_1))}ppm\n\n' \
                         f'соотношения:\n' \
                         f'nh4:no3 до {round(self.nh4_1 / self.no3_1 * 1000) / 1000} после {round(self.nh4_2 / self.no3_2 * 1000) / 1000}\n' \
                         f'k:n до {round(self.k_1 / self.n_1 * 1000) / 1000} после {round(self.k_2 / self.n_2 * 1000) / 1000}\n' \
                         f'k:ca до {round(self.k_1 / self.ca_1 * 1000) / 1000} после {round(self.k_2 / self.ca_2 * 1000) / 1000}\n' \
                         f'k:mg до {round(self.k_1 / self.mg_1 * 1000) / 1000} после {round(self.k_2 / self.mg_2 * 1000) / 1000}\n'

    @float_exception
    def calc_uncorrection(self, pushed_element=None, val=None):
    
        if pushed_element in self.correction_fields['2'] or  pushed_element in self.correction_fields['k']  or pushed_element in ['v_1','v_2']:
            if self.v_2 != 0: self.no3_2=  (self.no3_k * self.v_k + self.no3_1 * self.v_1) / self.v_2
            if self.v_2 != 0: self.nh4_2=  (self.nh4_k * self.v_k + self.nh4_1 * self.v_1) / self.v_2
    
            self.n_k = self.no3_k + self.nh4_k
            self.n_2 = self.no3_2 + self.nh4_2
    
            if self.v_2 != 0: self.p_2=  (self.p_k * self.v_k + self.p_1 * self.v_1) / self.v_2
            if self.v_2 != 0: self.k_2=  (self.k_k * self.v_k + self.k_1 * self.v_1) / self.v_2
            if self.v_2 != 0: self.ca_2=  (self.ca_k * self.v_k + self.ca_1 * self.v_1) / self.v_2
            if self.v_2 != 0: self.mg_2=  (self.mg_k * self.v_k + self.mg_1 * self.v_1) / self.v_2
            if self.v_2 != 0: self.cl_2=  (self.cl_k * self.v_k + self.cl_1 * self.v_1) / self.v_2
            self.s_k = self.calcs(self.no3_k,self.nh4_k,self.p_k,self.k_k,self.ca_k,self.mg_k,self.cl_k)
            self.ec_k = self.calcec(self.nh4_k,self.k_k,self.ca_k,self.mg_k)
            self.s_2 = self.calcs(self.no3_2,self.nh4_2,self.p_2,self.k_2,self.ca_2,self.mg_2,self.cl_2)
            self.ec_2 = self.calcec(self.nh4_2,self.k_2,self.ca_2,self.mg_2)

    @float_exception
    def calc_p_cano3(self):
        return self.p_cano3 * self.calc_cano3()

    @float_exception
    def calc_p_kno3(self):
        return self.p_kno3 * self.calc_kno3()

    @float_exception
    def calc_p_nh4no3(self):
        return self.p_nh4no3 * self.calc_nh4no3()

    @float_exception
    def calc_p_mgso4(self):
        return self.p_mgso4 * self.calc_mgso4()

    @float_exception
    def calc_p_kh2po4(self):
        return self.p_kh2po4 * self.calc_kh2po4()

    @float_exception
    def calc_p_k2so4(self):
        return self.p_k2so4 * self.calc_k2so4()

    @float_exception
    def calc_p_mgno3(self):
        return self.p_mgno3 * self.calc_mgno3()

    @float_exception
    def calc_p_cacl2(self):
        return self.p_cacl2 * self.calc_cacl2()

    @float_exception
    def calc_p_fe(self):
        return self.p_fe * self.gfe

    @float_exception
    def calc_p_mn(self):
        return self.p_mn * self.gmn

    @float_exception
    def calc_p_b(self):
        return self.p_b * self.gb

    @float_exception
    def calc_p_zn(self):
        return self.p_zn * self.gzn

    @float_exception
    def calc_p_cu(self):
        return self.p_cu * self.gcu

    @float_exception
    def calc_p_mo(self):
        return self.p_mo * self.gmo

    @float_exception
    def calc_p_co(self):
        return self.p_co * self.gco

    @float_exception
    def calc_p_si(self):
        return self.p_si * self.gsi

    @float_exception
    def calc_p_cmplx(self):
        return self.p_cmplx * self.cmplx()
    
    
    
    micro_text = None
    micro_sostav = None

    gmsum= None
    agfe= None
    agmn= None
    agb= None
    agzn= None
    agcu= None
    agmo= None
    agco= None
    agsi= None

    ml_cano3 = None
    gg_cano3 = None
    ml_kno3 = None
    gg_kno3 = None
    ml_nh4no3 = None
    gg_nh4no3 = None
    ml_mgno3 = None
    gg_mgno3 = None
    ml_cacl2 = None
    gg_cacl2 = None

    gg_mgso4  = None
    gg_kh2po4  = None
    gg_k2so4  = None
    gg_fe  = None
    gg_mn  = None
    gg_b  = None
    gg_zn  = None
    gg_cu  = None
    gg_mo  = None
    gg_co  = None
    gg_si  = None
    gg_cmplx   = None

    ml_mgso4= None
    ml_kh2po4= None
    ml_k2so4= None
    ml_fe= None
    ml_mn= None
    ml_b= None
    ml_zn= None
    ml_cu= None
    ml_mo= None
    ml_co= None
    ml_si= None
    ml_cmplx= None

    suma = ''
    lvola = ''
    sumb = ''
    lvolb = ''

    gmlcano3_error = False
    gmlkno3_error = False
    gmlnh4no3_error = False
    gmlmgno3_error = False
    gmlmgso4_error = False
    gmlkh2po4_error = False
    gmlk2so4_error = False
    gmlcacl2_error = False
    
    errors = {}

    @float_exception
    def get_mixer_link(self):
        params = {}
        adr = f'http://{str(self.mixer_ip)}'
        
        params['s'] =  int(self.mixer_system_number or 1)
        if self.m_cano3:  params[self.m_cano3] = round(self.gg_cano3,2)
        if self.m_kno3:   params[self.m_kno3] = round(self.gg_kno3,2)
        if self.m_nh4no3:  params[self.m_nh4no3] = round(self.gg_nh4no3,2)
        if self.m_mgno3:  params[self.m_mgno3] = round(self.gg_mgno3,2)
        if self.m_cacl2:  params[self.m_cacl2] = round(self.gg_cacl2,2)
        if self.m_mgso4:  params[self.m_mgso4] = round(self.gg_mgso4,2)
        if self.m_kh2po4:  params[self.m_kh2po4] = round(self.gg_kh2po4,2)
        if self.m_k2so4:  params[self.m_k2so4] = round(self.gg_k2so4,2)
        

        if self.micro_calc_mode==self.CalcMicroMode.B:
        
            params[self.m_cmplx] = round(self.gg_cmplx,2)
    
        else:
        
            if self.m_fe:  params[self.m_fe]  = round(self.gg_fe,2)
            if self.m_mn:  params[self.m_mn]  = round(self.gg_mn,2)
            if self.m_b:  params[self.m_b]  = round(self.gg_b,2)
            if self.m_zn:  params[self.m_zn]  = round(self.gg_zn,2)
            if self.m_cu:  params[self.m_cu]  = round(self.gg_cu,2)
            if self.m_mo:  params[self.m_mo]  = round(self.gg_mo,2)
            if self.m_co:  params[self.m_co]  = round(self.gg_co,2)
            if self.m_si:  params[self.m_si]  = round(self.gg_si,2)
        from urllib.parse import urlencode
        return f"{adr}?{urlencode(params)}"

    @float_exception
    def calc_micro_vars(self):
        self.agfe =  (self.fe * self.litres) / (self.gmsum * 10000)   if self.fe > 0 else 0
        self.agmn =  (self.mn * self.litres) / (self.gmsum * 10000)   if self.mn > 0 else 0
        self.agb  =  (self.b * self.litres)  / (self.gmsum * 10000)   if self.b  > 0 else 0
        self.agzn =  (self.zn * self.litres) / (self.gmsum * 10000)   if self.zn > 0 else 0
        self.agcu =  (self.cu * self.litres) / (self.gmsum * 10000)   if self.cu > 0 else 0
        self.agmo =  (self.mo * self.litres) / (self.gmsum * 10000)   if self.mo > 0 else 0
        self.agco =  (self.co * self.litres) / (self.gmsum * 10000)   if self.co > 0 else 0
        self.agsi =  (self.si * self.litres) / (self.gmsum * 10000)   if self.si > 0 else 0

    @float_exception
    def weight_to_micro(self):
        self.fe = 10000 * self.gfe * (self.dfe / self.litres)
        self.mn = 10000 * self.gmn * (self.dmn / self.litres)
        self.b  = 10000 * self.gb * (self.db /   self.litres)
        self.zn = 10000 * self.gzn * (self.dzn / self.litres)
        self.cu = 10000 * self.gcu * (self.dcu / self.litres)
        self.mo = 10000 * self.gmo * (self.dmo / self.litres)
        self.co = 10000 * self.gco * (self.dco / self.litres)
        self.si = 10000 * self.gsi * (self.dsi / self.litres)

    @float_exception
    def micro_to_weight(self, recalc_gmsum=True):
        
        if self.micro_calc_mode == self.CalcMicroMode.U:
            if recalc_gmsum:
                pass
            else:
                for i in self.salt_micro_persent:
                    cache_str = f"pp-{self.pk}-{i}"
                    ii = cache.get(cache_str)
                    if ii:
                        # print(' i, ii',  i, ii)
                        setattr(self, i, ii)


            self.gfe = self.fe / self.dfe * self.litres / 10000 if self.dfe > 0 else 0
            self.gmn = self.mn / self.dmn * self.litres / 10000 if self.dmn > 0 else 0
            self.gb  = self.b  / self.db  * self.litres / 10000 if self.db > 0 else 0
            self.gzn = self.zn / self.dzn * self.litres / 10000 if self.dzn > 0 else 0
            self.gcu = self.cu / self.dcu * self.litres / 10000 if self.dcu > 0 else 0
            self.gmo = self.mo / self.dmo * self.litres / 10000 if self.dmo > 0 else 0
            self.gco = self.co / self.dco * self.litres / 10000 if self.dco > 0 else 0
            self.gsi = self.si / self.dsi * self.litres / 10000 if self.dsi > 0 else 0

            if not self.gmsum:
                self.gmsum = self.gfe + self.gmn + self.gb + self.gzn + self.gcu + self.gmo + self.gco + self.gsi
                self.calc_micro_vars()
            
        else:
            
            if recalc_gmsum    :
                self.gmsum = self.b / self.db * self.litres / 10000
                self.calc_micro_vars(  )
            else:
                if not self.gmsum:
                    self.gmsum = self.b / self.db * self.litres / 10000
                    self.calc_micro_vars(   )
                for i in self.salt_micro_persent:
                    cache_str = f"pp-{self.pk}-{i}"
                    cache.set(cache_str, getattr(self, i))
                
                if self.agfe:
                    self.dfe = self.agfe
                    self.dmn = self.agmn
                    self.dzn = self.agzn
                    self.db  = self.agb
                    self.dcu = self.agcu
                    self.dmo = self.agmo
                    self.dco = self.agco
                    self.dsi = self.agsi

            self.fe = 10000 * self.gmsum * (self.dfe / self.litres)
            self.mn = 10000 * self.gmsum * (self.dmn / self.litres)
            self.zn = 10000 * self.gmsum * (self.dzn / self.litres)
            self.cu = 10000 * self.gmsum * (self.dcu / self.litres)
            self.mo = 10000 * self.gmsum * (self.dmo / self.litres)
            self.co = 10000 * self.gmsum * (self.dco / self.litres)
            self.si = 10000 * self.gmsum * (self.dsi / self.litres)

    @float_exception
    def switch_micro_to_bor(self):
        if not any([self.gfe + self.gmn + self.gb + self.gzn + self.gcu + self.gmo + self.gco + self.gsi]):
            self.micro_to_weight(recalc_gmsum=False)
        self.gmsum = self.gfe + self.gmn + self.gb + self.gzn + self.gcu + self.gmo + self.gco + self.gsi
        self.calc_micro_vars()
        self.micro_to_weight(recalc_gmsum=False)

    @float_exception
    def switch_micro_to_all(self):
        self.gmsum = self.gfe + self.gmn + self.gb + self.gzn + self.gcu + self.gmo + self.gco + self.gsi
        if not any([self.gfe + self.gmn + self.gb + self.gzn + self.gcu + self.gmo + self.gco + self.gsi]):
            self.micro_to_weight(recalc_gmsum=False)
        self.calc_micro_vars()
        self.micro_to_weight(recalc_gmsum=False)
        
    def get_profile_str(self):
         return f"N={int(self.n)} NO3={int(self.no3)} NH4={int(self.nh4)} P={int(self.p)} K={int(self.k)} " \
                f"Ca={int(self.ca)} Mg={int(self.mg)} " \
                f"S={int(self.s)} Cl={int(self.cl)} Fe={int(self.fe)/1000} Mn={int(self.mn)/1000} " \
                f"B={int(self.b)/1000} Zn={int(self.zn)/1000} " \
                f"Cu={int(self.cu)/1000} Mo={int(self.mo)} Co={int(self.co)} Si={int(self.si)} "
    @float_exception
    def calc_micro(self, pushed_element=None, val=None):
        
        if pushed_element and pushed_element == 'micro_calc_mode' and val=='b':
            self.micro_calc_mode = self.CalcMicroMode.B
            self.switch_micro_to_bor()
            return
        
        if pushed_element and pushed_element == 'micro_calc_mode' and val=='u':
            self.micro_calc_mode = self.CalcMicroMode.U
            self.switch_micro_to_all()
            return
        
        
        if pushed_element in self.micro or pushed_element in self.salt_micro_gramm \
                or pushed_element in self.salt_micro_persent or pushed_element in [ 'weight_micro', 'v_micro', 'litres', None]:
            
         
            recalc_gmsum= True
            
            if not any([self.gfe + self.gmn + self.gb + self.gzn + self.gcu + self.gmo + self.gco + self.gsi]):
                self.micro_to_weight(recalc_gmsum=False)
                
          
            if not self.gmsum:
                if self.micro_calc_mode==self.CalcMicroMode.U:
                    self.gmsum = self.gfe + self.gmn + self.gb + self.gzn + self.gcu + self.gmo + self.gco + self.gsi
                else:
                    self.gmsum = self.b / self.db * self.litres / 10000
            
            self.calc_micro_vars()
            if pushed_element in self.salt_micro_gramm:
                if self.micro_calc_mode==self.CalcMicroMode.U:
                    self.weight_to_micro()
            else:
                if pushed_element!='weight_micro':
                    self.micro_to_weight(recalc_gmsum=recalc_gmsum)
                    
           
                
            if pushed_element == 'weight_micro' and self.micro_calc_mode==self.CalcMicroMode.B:
                self.gmsum = float(val)
                self.b = 10000 * self.gmsum * (self.db / self.litres)
                self.micro_to_weight(recalc_gmsum=True)

        if self.micro_calc_mode == self.CalcMicroMode.U:
            if not any([self.gfe + self.gmn + self.gb + self.gzn + self.gcu + self.gmo + self.gco + self.gsi]):
                self.micro_to_weight(recalc_gmsum=False)
    
            
            self.gmsum = self.gfe + self.gmn + self.gb + self.gzn + self.gcu + self.gmo + self.gco + self.gsi
            self.calc_micro_vars()
            self.micro_sostav = f'Состав: Fe={round(self.agfe * 1000) / 1000}%' \
                                f' Mn={(round(self.agmn * 1000) / 1000)}%' \
                                f' B={round(self.agb * 1000) / 1000}%' \
                                f' Zn={round(self.agzn * 1000) / 1000}%' \
                                f' Cu={round(self.agcu * 1000) / 1000}%' \
                                f' Mo={round(self.agmo * 1000) / 1000}%' \
                                f' Co={round(self.agco * 1000) / 1000}%' \
                                f' Si={round(self.agsi * 1000) / 1000}%'
      
        if self.v_micro > 0:
            if self.micro_calc_mode==self.CalcMicroMode.U:
                self.gmsum = self.gfe + self.gmn + self.gb + self.gzn + self.gcu + self.gmo + self.gco + self.gsi
            else:
                self.gmsum = self.b / self.db * self.litres / 10000
            self.micro_text = f'Концентрация: {round(self.gmsum * 1000 / self.v_micro * 100) / 100} г/л,' \
                              f'Кратность: {round(self.litres / self.v_micro * 1000)}:1,' \
                              f'Расход: {round(self.v_micro / self.litres * 10) / 10} мл/л раствора'
                        
    @float_exception
    def cmplx(self):
        return self.weight_micro()

    @float_exception
    def weight_micro(self):
        if self.micro_calc_mode == self.CalcMicroMode.B:
            return self.calc_bor_complex()
        else:
            return self.gfe + self.gmn + self.gzn + self.gcu + self.gmo + self.gco + self.gsi

    @float_exception
    def calc_bor_complex(self):
        print( ' self.micro_calc_mode ', self.micro_calc_mode , self.micro_calc_mode == self.CalcMicroMode.B)
        if self.b > 0 and self.micro_calc_mode == self.CalcMicroMode.B:
            bor_complex = self.b / self.db * self.litres / 10000
        else:
            bor_complex = 0
        return bor_complex

    @float_exception
    def k_mg(self):
        return  self.k / self.mg

    @float_exception
    def k_ca(self):
        return  self.k / self.ca

    @float_exception
    def k_n(self):
        return  self.k / self.n

    @float_exception
    def get_npk(self):
        t = self.get_matrix()[0]

    @float_exception
    def get_profile(self):
        return f"N={round(self.n)} " \
               f"NO3={round(self.no3 * 100) / 100} " \
               f"NH4={round(self.nh4 * 100) / 100} " \
               f"P={round(self.p * 100) / 100} " \
               f"K={round(self.k * 100) / 100} " \
               f"Ca={round(self.ca * 100) / 100} " \
               f"Mg={round(self.mg * 100) / 100} " \
               f"S={round(self.s * 100) / 100} " \
               f"Cl={round(self.cl * 100) / 100} " \
               f"Fe={round(self.fe / 1000, 2)} " \
               f"Mn={round(self.mn / 1000, 2)} " \
               f"B={round(self.b / 1000, 2)} " \
               f"Zn={round(self.zn / 1000, 2)} " \
               f"Cu={round(self.cu / 1000, 2)} " \
               f"Mo={round(self.mo / 1000, 2)} " \
               f"Co={round(self.co / 1000, 2)} " \
               f"Si={round(self.si / 1000, 2)}"
    
    @float_exception
    def calc_npk_formula(self):
        a = f"{math.ceil(self.n / self.n * 100) / 100} : " \
            f"{math.ceil(self.p / self.n * 100) / 100} : " \
            f"{math.ceil(self.k / self.n * 100) / 100} : " \
            f"{math.ceil(self.ca / self.n * 100) / 100} : " \
            f"{math.ceil(self.mg / self.n * 100) / 100} : " \
            f"{math.ceil(self.s / self.n * 100) / 100} : " \
            f"{math.ceil(self.cl / self.n * 100) / 100} sPPM={self.calc_ppm()}"
        return a

    @float_exception
    def get_npk_magazine(self):
        a = f"NPK: {math.ceil(self.n / 10)}-{math.ceil(self.p / 0.436421 / 10)}-{math.ceil(self.k / 0.830148 / 10)} " \
            f"CaO={(math.ceil(self.ca / 0.714691 / 10) * 10 / 10)}% MgO={math.ceil(self.mg / 0.603036 / 10 * 10) / 10}%" \
            f"SO3={math.ceil(self.s / 0.400496 / 10 * 10) / 10}"
        return a

    @float_exception
    def get_matrix(self, as_dict=False):
        pp = self
        matrix = []
        matrix_dict = {}
        element_row = self.macro_matrix.copy()
        matix_length = len(self.macro_matrix)
        ii = 0
        
        while ii != matix_length:
            cur_element = element_row[0]
            row = {}
            cur_cal = getattr(pp, cur_element.lower()) or 0
            for i in self.macro_matrix:
                val = getattr(pp, i.lower()) or 0
                if val is None or cur_cal is None or cur_cal == 0:
                    row[i] = None
                    matrix_dict[f"{i}-{cur_element}"] = None
                else:
                    
                    try:
                        t = round(val / cur_cal, 2)
                    except ZeroDivisionError as e:
                        t = 0
                    row[i] = t
                    matrix_dict[f"{i}-{cur_element}"] = t
            
            del element_row[0]
            element_row.append(cur_element)
            matrix.append(row)
            ii += 1
        if as_dict:
            return matrix_dict
        return matrix

    @float_exception
    def calc_ec_to_val(self, k_n=None, k_ca=None, k_mg=None):
        
        m = MM()
        if not k_mg: k_mg = self.k_mg()
        if not k_ca: k_ca = self.k_ca()
        if not k_n: k_n = self.k_n()
        r_n = (k_mg * k_ca) / \
              (k_ca * k_n + k_mg * k_n + k_mg * k_ca + k_mg * k_ca * k_n)
        r_k = (k_n * k_mg * k_ca) / (
                k_ca * k_n + k_mg * k_n + k_mg * k_ca + k_mg * k_ca * k_n)
        r_ca = (k_mg * k_n) / (
                k_ca * k_n + k_mg * k_n + k_mg * k_ca + k_mg * k_ca * k_n)
        r_mg = (k_ca * k_n) / (
                k_ca * k_n + k_mg * k_n + k_mg * k_ca + k_mg * k_ca * k_n)
        r_nh4 = (r_n * self.nh4_nh3_ratio) / (1 + self.nh4_nh3_ratio)
    
    
        r = (0.10526315789473684211 * m.N * m.Ca * m.Mg * m.K * (100 * self.ec - 19)) / \
            ( r_nh4 * m.Ca * m.Mg * m.K +
                    2 * r_ca * m.N * m.Mg * m.K +
                    2 * r_mg * m.N * m.Ca * m.K +
                    r_k * m.N * m.Ca * m.Mg)
    
        self.n = r_n * r
        self.k = r_k * r
        self.ca = r_ca * r
        self.mg = r_mg * r
        self.nh4 = r_nh4 * r
        self.no3 = self.n - self.nh4
        
        self.s = self.calc_s()

    @float_exception
    def calc_ratio(self):
        self.nh4 = self.n * (self.nh4_nh3_ratio / (self.nh4_nh3_ratio + 1))
        self.no3 = self.n / (self.nh4_nh3_ratio + 1)

    @float_exception
    def calc_macro(self, pushed_element=None, val=None):
        m = MM()
    
        if pushed_element == 'nh4_nh3_ratio':
            self.calc_ratio()
    
        if pushed_element and 'matrix' in pushed_element:
            k_n=None
            k_ca=None
            k_mg=None
            
            t, a, b, = pushed_element.split('-')

            if pushed_element == 'matrix-k-n':
                k_ca = self.k_ca()
                k_mg = self.k_mg()
                
            if pushed_element == 'matrix-k-ca':
                k_n = self.k_n()
                k_mg= self.k_mg()
                
            if pushed_element == 'matrix-k-mg':
                k_n = self.k_n()
                k_ca = self.k_ca()
            
            if pushed_element == 'matrix-ca-s':
                self.s = self.ca/ val
                print('*****', 's', self.ca/ val )
                
            if a=='s':
                self.s = getattr(self, b) * val
                print('*****', 's', self.n * val)
                
            else:
                v = getattr(self, b) * val
                setattr(self, a, v)
                print('*****', a, v)
        
            self.calc_ratio()
            if b=='s' or a=='s':
                self.ca = self.calc_ca()
            if pushed_element not in ['matrix-k-mg', 'matrix-k-ca', 'matrix-k-n']:
                print('changing ec')
                self.ec = self.saved_ec
            print(f'ec now/old {self.ec} /{self.saved_ec}',)
            self.calc_ec_to_val(k_n=k_n, k_ca=k_ca, k_mg=k_mg)

        if pushed_element in  ['ec', 'nh4_nh3_ratio']:
            self.calc_ec_to_val()
            
        if pushed_element=='nh4_nh3_ratio':
            self.s = self.calc_s()
     
            
        if pushed_element in self.salt_gramms:
            val = float(val)
            
            if pushed_element == 'cano3' :
                n_no3 = (val * self.cano3_no3 + self.nh4no3_no3 * self.calc_nh4no3() + self.calc_kno3() * self.kno3_no3 +
                         self.calc_mgno3() * self.mgno3_no3) / (0.1 * self.litres)
                n_nh4 = (val * self.cano3_nh4 + self.calc_nh4no3() * self.nh4no3_nh4) / (0.1 * self.litres)
                n_n = n_no3 + n_nh4
                n_p = (self.calc_kh2po4() * self.kh2po4_p) / (0.1 * self.litres)
                n_k = (self.calc_kno3() * self.kno3_k + self.calc_kh2po4() * self.kh2po4_k + self.calc_k2so4() * self.k2so4_k) / (
                            0.1 * self.litres)
                n_ca = (val * self.cano3_ca + self.calc_cacl2() * self.cacl2_ca) / (0.1 * self.litres)
                n_mg = (self.calc_mgso4() * self.mgso4_mg + self.calc_mgno3() * self.mgno3_mg) / (0.1 * self.litres)
                n_nhno3 = n_nh4 / n_no3
                n_cl = (self.calc_cacl2() * self.cacl2_cl) / (0.1 * self.litres)
        
            if pushed_element == 'kno3' :
                n_no3 = (self.calc_cano3() * self.cano3_no3 + self.nh4no3_no3 * self.calc_nh4no3() + val * self.kno3_no3 +
                         self.calc_mgno3() * self.mgno3_no3) / (0.1 * self.litres)
                n_nh4 = (self.calc_cano3() * self.cano3_nh4 + self.calc_nh4no3() * self.nh4no3_nh4) / (0.1 * self.litres)
                n_n = n_no3 + n_nh4
                n_p = (self.calc_kh2po4() * self.kh2po4_p) / (0.1 * self.litres)
                n_k = (val * self.kno3_k + self.calc_kh2po4() * self.kh2po4_k + self.calc_k2so4() * self.k2so4_k) / (
                            0.1 * self.litres)
                n_ca = (self.calc_cano3() * self.cano3_ca + self.calc_cacl2() * self.cacl2_ca) / (0.1 * self.litres)
                n_mg = (self.calc_mgso4() * self.mgso4_mg + self.calc_mgno3() * self.mgno3_mg) / (0.1 * self.litres)
                n_nhno3 = n_nh4 / n_no3
                n_cl = (self.calc_cacl2() * self.cacl2_cl) / (0.1 * self.litres)
        
            if pushed_element == 'nh4no3':
                n_no3 = (self.calc_cano3() * self.cano3_no3 + self.nh4no3_no3 * val + self.calc_kno3() * self.kno3_no3 +
                         self.calc_mgno3() * self.mgno3_no3) / (0.1 * self.litres)
                n_nh4 = (self.calc_cano3() * self.cano3_nh4 + val * self.nh4no3_nh4) / (0.1 * self.litres)
                n_n = n_no3 + n_nh4
                n_p = (self.calc_kh2po4() * self.kh2po4_p) / (0.1 * self.litres)
                n_k = (self.calc_kno3() * self.kno3_k + self.calc_kh2po4() * self.kh2po4_k + self.calc_k2so4() * self.k2so4_k) / (
                            0.1 * self.litres)
                n_ca = (self.calc_cano3() * self.cano3_ca + self.calc_cacl2() * self.cacl2_ca) / (0.1 * self.litres)
                n_mg = (self.calc_mgso4() * self.mgso4_mg + self.calc_mgno3() * self.mgno3_mg) / (0.1 * self.litres)
                n_nhno3 = n_nh4 / n_no3
                n_cl = (self.calc_cacl2() * self.cacl2_cl) / (0.1 * self.litres)
    
            if pushed_element == 'mgso4' :
                n_no3 = (self.calc_cano3() * self.cano3_no3 + self.nh4no3_no3 * self.calc_nh4no3() + self.calc_kno3() * self.kno3_no3 +
                         self.calc_mgno3() * self.mgno3_no3) / (0.1 * self.litres)
                n_nh4 = (self.calc_cano3() * self.cano3_nh4 + self.calc_nh4no3() * self.nh4no3_nh4) / (0.1 * self.litres)
                n_n = n_no3 + n_nh4
                n_p = (self.calc_kh2po4() * self.kh2po4_p) / (0.1 * self.litres)
                n_k = (self.calc_kno3() * self.kno3_k + self.calc_kh2po4() * self.kh2po4_k + self.calc_k2so4() * self.k2so4_k) / (
                            0.1 * self.litres)
                n_ca = (self.calc_cano3() * self.cano3_ca + self.calc_cacl2() * self.cacl2_ca) / (0.1 * self.litres)
                n_mg = (val * self.mgso4_mg + self.calc_mgno3() * self.mgno3_mg) / (0.1 * self.litres)
                n_nhno3 = n_nh4 / n_no3
                n_cl = (self.calc_cacl2() * self.cacl2_cl) / (0.1 * self.litres)
        
            if pushed_element == 'kh2po4' :
                n_no3 = (self.calc_cano3() * self.cano3_no3 + self.nh4no3_no3 * self.calc_nh4no3() + self.calc_kno3() * self.kno3_no3 +
                         self.calc_mgno3() * self.mgno3_no3) / (0.1 * self.litres)
                n_nh4 = (self.calc_cano3() * self.cano3_nh4 + self.calc_nh4no3() * self.nh4no3_nh4) / (0.1 * self.litres)
                n_n = n_no3 + n_nh4
            
                n_p = (val * self.kh2po4_p) / (0.1 * self.litres)
                n_k = (self.calc_kno3() * self.kno3_k + val * self.kh2po4_k + self.calc_k2so4() * self.k2so4_k) / (
                            0.1 * self.litres)
                n_ca = (self.calc_cano3() * self.cano3_ca + self.calc_cacl2() * self.cacl2_ca) / (0.1 * self.litres)
                n_mg = (self.calc_mgso4() * self.mgso4_mg + self.calc_mgno3() * self.mgno3_mg) / (0.1 * self.litres)
                n_nhno3 = n_nh4 / n_no3
                n_cl = (self.calc_cacl2() * self.cacl2_cl) / (0.1 * self.litres)
        
            if pushed_element == 'k2so4' :
                n_no3 = (self.calc_cano3() * self.cano3_no3 + self.nh4no3_no3 * self.calc_nh4no3() + self.calc_kno3() * self.kno3_no3 +
                         self.calc_mgno3() * self.mgno3_no3) / (0.1 * self.litres)
                n_nh4 = (self.calc_cano3() * self.cano3_nh4 + self.calc_nh4no3() * self.nh4no3_nh4) / (0.1 * self.litres)
                n_n = n_no3 + n_nh4
                n_p = (self.calc_kh2po4() * self.kh2po4_p) / (0.1 * self.litres)
                n_k = (self.calc_kno3() * self.kno3_k + self.calc_kh2po4() * self.kh2po4_k + val * self.k2so4_k) / (
                            0.1 * self.litres)
                n_ca = (self.calc_cano3() * self.cano3_ca + self.calc_cacl2() * self.cacl2_ca) / (0.1 * self.litres)
                n_mg = (self.calc_mgso4() * self.mgso4_mg + self.calc_mgno3() * self.mgno3_mg) / (0.1 * self.litres)
                n_nhno3 = n_nh4 / n_no3
                n_cl = (self.calc_cacl2() * self.cacl2_cl) / (0.1 * self.litres)
        
            if pushed_element == 'mgno3'  :
                if self.calc_mode == self.CalcMode.Mg:
                    n_no3 = (self.calc_cano3() * self.cano3_no3 + self.nh4no3_no3 * self.calc_nh4no3() + self.calc_kno3() * self.kno3_no3 +
                             val * self.mgno3_no3) / (0.1 * self.litres)
                    n_nh4 = (self.calc_cano3() * self.cano3_nh4 + self.calc_nh4no3() * self.nh4no3_nh4) / (0.1 * self.litres)
                    n_n = n_no3 + n_nh4
                    n_p = (self.calc_kh2po4() * self.kh2po4_p) / (0.1 * self.litres)
                    n_k = (self.calc_kno3() * self.kno3_k + self.calc_kh2po4() * self.kh2po4_k + self.calc_k2so4() * self.k2so4_k) / (
                                0.1 * self.litres)
                    n_ca = (self.calc_cano3() * self.cano3_ca + self.calc_cacl2() * self.cacl2_ca) / (0.1 * self.litres)
                    n_mg = (self.calc_mgso4() * self.mgso4_mg + val * self.mgno3_mg) / (0.1 * self.litres)
                    n_nhno3 = n_nh4 / n_no3
                    n_cl = (self.calc_cacl2() * self.cacl2_cl) / (0.1 * self.litres)
             
        
            if pushed_element == 'cacl2' :
                n_no3 = (self.calc_cano3() * self.cano3_no3 + self.nh4no3_no3 * self.calc_nh4no3() + self.calc_kno3() * self.kno3_no3 +
                         self.calc_mgno3() * self.mgno3_no3) / (0.1 * self.litres)
                n_nh4 = (self.calc_cano3() * self.cano3_nh4 + self.calc_nh4no3() * self.nh4no3_nh4) / (0.1 * self.litres)
                n_n = n_no3 + n_nh4
                n_p = (self.calc_kh2po4() * self.kh2po4_p) / (0.1 * self.litres)
                n_k = (self.calc_kno3() * self.kno3_k + self.calc_kh2po4() * self.kh2po4_k + self.calc_k2so4() * self.k2so4_k) / (
                            0.1 * self.litres)
                n_ca = (self.calc_cano3() * self.cano3_ca + val * self.cacl2_ca) / (0.1 * self.litres)
                n_mg = (self.calc_mgso4() * self.mgso4_mg + self.calc_mgno3() * self.mgno3_mg) / (0.1 * self.litres)
                n_nhno3 = n_nh4 / n_no3
                n_cl = (val * self.cacl2_cl) / (0.1 * self.litres)
        
            self.nh4_nh3_ratio = n_nhno3
            self.n = n_n
            self.no3 = n_no3
            self.nh4 = n_nh4
            self.p = n_p
            self.k = n_k
            self.ca = n_ca
            self.mg = n_mg
            self.cl = n_cl
        
            if pushed_element in ['mgso4', 'k2so4']:
                self.s = self.calc_s()
        
            if pushed_element in ['cacl2']:
                self.s = self.calc_s()
                self.ca = self.calc_ca()

        if pushed_element == 'nh4':
            t = self.n - self.nh4
            self.no3 = t
            self.n = self.no3 + self.nh4

        if pushed_element == 'no3':
            t = self.n - self.no3
            self.nh4 = t
            self.n = self.no3 + self.nh4

        if pushed_element == 'n':
            self.no3 = self.n / (self.nh4_nh3_ratio + 1)
            self.nh4 = self.nh4_nh3_ratio * self.n / (self.nh4_nh3_ratio + 1)
            self.s = self.calc_s()
            
        if pushed_element == 's':
            self.ca = self.calc_ca()

        if pushed_element not in self.salt_gramms and pushed_element not in [ 'litres' ]:
            if pushed_element not in self.macro:
                self.ca = self.calc_ca()
            self.s = self.calc_s()

        if pushed_element == 'cano3_ca':
            self.cano3_no3 = (2 * self.cano3_ca * m.N + self.cano3_nh4 * m.Ca) / m.Ca

        if pushed_element == 'cano3_nh4':
            self.cano3_no3 = (2 * self.cano3_ca * m.N + self.cano3_nh4 * m.Ca) / m.Ca;
            self.cano3_ca = -m.Ca * (self.cano3_nh4 - self.cano3_no3) / (2 * m.N);

        if pushed_element == 'kno3_k':
            self.kno3_no3 = (self.kno3_k * m.N) / m.K

        if pushed_element == 'kno3_no3':
            self.kno3_k = (self.kno3_no3 * m.K) / m.N
            self.kno3_no3 = (self.kno3_k * m.N) / m.K

        if pushed_element == 'nh4no3_no3':
            self.nh4no3_nh4 = self.nh4no3_no3

        if pushed_element == 'nh4no3_nh4':
            self.nh4no3_no3 = self.nh4no3_nh4

        if pushed_element == 'mgso4_mg':
            self.mgso4_s = (self.mgso4_mg * m.S) / m.Mg

        if pushed_element == 'mgso4_s':
            self.mgso4_mg = (self.mgso4_s * m.Mg) / m.S

        if pushed_element == 'kh2po4_k':
            self.kh2po4_p = (self.kh2po4_k * m.P) / m.K

        if pushed_element == 'kh2po4_p':
            self.kh2po4_k = (self.kh2po4_p * m.K) / m.P

        if pushed_element == 'k2so4_k':
            self.k2so4_s = (self.k2so4_k * m.S) / (2 * m.K)

        if pushed_element == 'k2so4_s':
            self.k2so4_k = (self.k2so4_s * 2 * m.K) / (m.S)

        if pushed_element == 'mgno3_mg':
            self.mgno3_no3 = (2 * self.mgno3_mg * m.N) / (m.Mg)

        if pushed_element == 'mgno3_no3':
            self.mgno3_mg = ((1 / 2) * (self.mgno3_no3 / m.N) * m.Mg)

        if pushed_element == 'cacl2_cl':
            self.cacl2_ca = (0.5 * (self.cacl2_cl / m.Cl)) * (m.Ca)

        if pushed_element == 'cacl2_ca':
            self.cacl2_cl = (2 * self.cacl2_ca / m.Ca) * (m.Cl)

        if pushed_element == 'cano3_nh4':
            self.cano3_no3 = (2 * self.cano3_ca * m.N + self.cano3_nh4 * m.Ca) / m.Ca
            self.cano3_ca = -m.Ca * (self.cano3_nh4 - self.cano3_no3) / (2 * m.N)

        if pushed_element == 'cano3_no3':
            self.cano3_ca = -m.Ca * (self.cano3_nh4 - self.cano3_no3) / (2 * m.N)

        if pushed_element == 'litres':
            for k, i in self.salt_gramms.items():
                setattr(self, k , getattr(self, i))

    @float_exception
    def recalc(self, pushed_element=None, val=None):
        try:
            val = float(val)
        except Exception:
            pass
        self.calc_macro(pushed_element=pushed_element, val=val)
        self.calc_micro(pushed_element=pushed_element, val=val)
        self.calc_concentrates(pushed_element=pushed_element, val=val)
        
        self.calc_correction(pushed_element=pushed_element, val=val)
        self.calc_uncorrection(pushed_element=pushed_element, val=val)
        self.calc_prices(pushed_element=pushed_element, val=val)
      
        self.captions = self.calc_captions()
        if pushed_element  and not 'matrix' in pushed_element:
            self.ec = self.calc_ec()
        
        self.ppm = self.calc_ppm()
        self.npk = self.get_npk()
        self.npk_formula = self.calc_npk_formula()
        self.npk_magazine = self.get_npk_magazine()
        self.salt_grams = self.sum_salt_grams()
    
    def to_json(self):
        
        
        data = {'pk': self.pk,
                'ec': "{:.3f}".format(self.ec),
                'ppm': "{:.2f}".format(self.ppm),
                'litres': self.litres,
                'get_profile_str': self.get_profile_str(),
                'mixer_system_number': self.mixer_system_number,
                'mixer_btn_link': self.get_mixer_link(),
                
                'weight_micro': "{:.2f}".format(self.weight_micro()),
                'npk': self.npk,
                'npk_formula': self.npk_formula,
                'npk_magazine': self.npk_magazine,
                'captions': self.captions,
                'micro_calc_mode': self.micro_calc_mode,
                'calc_mode': self.calc_mode,
                'salt_grams': "{:.2f}".format(self.salt_grams),
                'micro_text': self.micro_text,
                'micro_sostav': self.micro_sostav,
                'errors': self.errors,
                'suma': self.suma,
                'lvola': self.lvola,
                'sumb': self.sumb,
                'lvolb': self.lvolb,
                'v_1':self.v_1,
                'v_2': self.v_2,
                'v_k': self.v_k,
                'cmplx': "{:.2f}".format(self.weight_micro()),
                'mkorr': format_html(self.mkorr),
                
                
                
                
                }
        
        for s in self.captions:
            data[f"name-{s}"] = self.captions[s]
        
        for s in self.macro:
            data[s] = "{:.2f}".format(getattr(self, s))
        
        for s in self.micro:
            data[s] = "{:.0f}".format(getattr(self, s))
        
        for s in self.salt_micro_gramm:
            data[s] = "{:.3f}".format(getattr(self, s))

        for s in self.salt_micro_persent:
            data[s] = "{:.4f}".format(getattr(self, s))
        
        for s in self.concentrate_fields:
            t = getattr(self, s)
            if t:
                data[s] = "{:.2f}".format(t)

        for k, i in self.salt_gramms.items():
            a = getattr(self, i)()
            setattr(self, k, a)

        for s, d in self.salt_dict.items():
    
            data[s] = "{:.2f}".format(getattr(self, s))
            for i in d.get('salt'):
                data[i] = "{:.2f}".format(getattr(self, i))

        for i in self.price_fields:
            t = 'calc_' + i
            a = getattr(self, t)()
            setattr(self, i, a)
            data[t] = "{:.3f}".format(a)
        
        for k, ii in self.correction_fields.items():
            for i in ii:
                data[i] = "{:.2f}".format(getattr(self, i))

        
        
        
        matrix = self.get_matrix(as_dict=True)
        for k, i in matrix.items():
            if i:
                data[f'matrix-{k}'] = "{:.2f}".format(i)
            else:
                data[f'matrix-{k}'] = 0
        
        return data

    @float_exception
    def calc_ppm(self):
        ppm = round((self.n + self.p + self.k + self.ca + self.mg + self.s + self.cl) * 100) / 100
        return ppm
    
    @float_exception
    def get_salt_dict(self):
        return self.salt_dict
    
    @float_exception
    def calc_kh2po4(self):
        a = self.p / self.kh2po4_p
        return a * self.litres / 10

    @float_exception
    def calc_ec(self):
        
        if self.pk:
            m = MM()
            a = self.nh4 * m.Ca * m.Mg * m.K
            b = self.ca * m.N * m.Mg * m.K
            c = self.mg * m.N * m.Ca * m.K
            d = self.k * m.N * m.Ca * m.Mg
            e = m.N * m.Ca * m.Mg * m.K
            f = m.N * m.Ca * m.Mg * m.K
            ec = 0.095 * (a + 2 * b + 2 * c + d + 2 * e) / f
            return ec

    @float_exception
    def calc_ca(self):
        m = MM()
        b = self.nh4 * m.P * m.Mg * m.K * m.S * m.Cl
        c = self.p * m.N * m.Mg * m.K * m.S * m.Cl
        d = self.mg * m.N * m.P * m.K * m.S * m.Cl
        e = self.k * m.N * m.P * m.Mg * m.S * m.Cl
        f = self.no3 * m.P * m.Mg * m.K * m.S * m.Cl
        g = self.s * m.N * m.P * m.Mg * m.K * m.Cl
        h = self.cl * m.N * m.P * m.Mg * m.K * m.S
        i = m.N * m.P * m.Mg * m.K * m.S * m.Cl
        ans = (-m.Ca * (b - c + 2 * d + e - f - 2 * g - h)) / (2 * i)
        
        return ans
    
    @float_exception
    def calc_kno3(self):
        if self.calc_mode == self.CalcMode.K:
            a = self.k * self.kh2po4_p * self.k2so4_s * self.mgso4_mg
            b = self.p * self.kh2po4_k * self.k2so4_s * self.mgso4_mg
            c = self.k2so4_k * self.kh2po4_p * self.s * self.mgso4_mg
            d = self.k2so4_k * self.kh2po4_p * self.mg * self.mgso4_s
            e = self.kno3_k * self.kh2po4_p * self.k2so4_s * self.mgso4_mg
            f = -(-a + b + c - d) / e
            return f * self.litres / 10
        else:
            a = self.k * self.kh2po4_p - self.p * self.kh2po4_k
            b = self.kno3_k * self.kh2po4_p
            return (a / b) * self.litres / 10
        return 0
    
    @float_exception
    def calc_cano3(self):
        a = self.ca * self.cacl2_cl - self.cl * self.cacl2_ca
        b = self.cano3_ca * self.cacl2_cl
        c = a / b
        return c * self.litres / 10
    
    @float_exception
    def calc_mgso4(self):
        if self.calc_mode == self.CalcMode.K:
            a = self.mg
            b = self.mgso4_mg
            c = a / b
            return c * self.litres / 10
        else:
            a = self.s
            b = self.mgso4_s
            c = a / b
            return c * self.litres / 10
        return 0
    
    @float_exception
    def calc_k2so4(self):
        if self.calc_mode == self.CalcMode.K:
            a = self.s * self.mgso4_mg - self.mg * self.mgso4_s
            b = self.k2so4_s * self.mgso4_mg
            c = a / b
            return c * self.litres / 10
        return 0
    
    @float_exception
    def calc_nh4no3(self):
        a = self.nh4 * self.cano3_ca * self.cacl2_cl
        b = self.cano3_nh4 * self.ca * self.cacl2_cl
        c = self.cano3_nh4 * self.cl * self.cacl2_ca
        d = self.nh4no3_nh4 * self.cano3_ca * self.cacl2_cl
        e = -(-a + b - c) / d
        return e * self.litres / 10
    
    @float_exception
    def calc_cacl2(self):
        a = self.cl
        b = self.cacl2_cl
        c = a / b
        return c * self.litres / 10
    
    @float_exception
    def calc_mgno3(self):
        if self.calc_mode == self.CalcMode.Mg:
            a = self.mg * self.mgso4_s - self.mgso4_mg * self.s
            b = self.mgno3_mg * self.mgso4_s
            c = a / b
            return c * self.litres / 10
        return 0
    
    @float_exception
    def calc_s(self):
        m = MM
       

        a = self.nh4 * m.Ca * m.Mg * m.K * m.P * m.Cl
        b = 2 * self.ca * m.N * m.Mg * m.K * m.P * m.Cl
        c = 2 * self.mg * m.N * m.Ca * m.K * m.P * m.Cl
        d = self.k * m.N * m.Ca * m.Mg * m.P * m.Cl
        e = self.no3 * m.Ca * m.Mg * m.K * m.P * m.Cl
        f = self.p * m.N * m.Ca * m.Mg * m.K * m.Cl
        g = self.cl * m.N * m.Ca * m.Mg * m.K * m.P
        h = 2 * m.N * m.Ca * m.Mg * m.K * m.P * m.Cl
        total = -m.S * (-a - b - c - d + e + f + g) / (h)
        return total
    
    def calc_captions(self):
        captions = {'fe': 'Железо Fe', 'mn': 'Марганец Mn', 'b': "Бор B", 'zn': "Цинк Zn", 'cu': "Медь Cu",
                    'mo': "Молибден Mo", 'co': "Кобальт Co", 'si': "Силениум Si", 'cmplx': "Комплексное удобрение",
                    'cano3': f'Селитра кальциевая CaO-{round((self.cano3_ca / 0.714691) * 10) / 10}%' \
                             f'N-{round((self.cano3_nh4 + self.cano3_no3) * 10) / 10}'}

        if self.cano3_nh4 == 0:
            if math.ceil(self.cano3_ca * 10) / 10 == 17:
                captions['cano3'] = 'Кальций азотнокислый Са(NО3)2*4H2O'
            if math.ceil(self.cano3_ca * 10) / 10 == 20:
                captions['cano3'] = 'Кальций азотнокислый Са(NО3)2*2H2O'
            if math.ceil(self.cano3_ca * 10) / 10 == 20:
                captions['cano3'] = 'Кальций азотнокислый Ca(NO3)2'
        
        captions[
            'kno3'] = f'Селитра калиевая K2O-{(math.ceil((self.kno3_k / 0.830148) * 10) / 10)} %  N-{math.ceil((self.kno3_no3) * 10) / 10}%'
        if round(self.kno3_k * 10) / 10 == 38.7:
            captions['kno3'] = 'Калий азотнокислый KNO3'
        
        captions['nh4no3'] = f'Селитра аммиачная N- {(math.ceil((self.nh4no3_nh4 + self.nh4no3_no3) * 10) / 10)}%'
        if round(self.nh4no3_no3 * 10) / 10 == 17.5:
            captions['nh4no3'] = f'Аммоний азотнокислый NH4NO3'
        
        captions[
            'mgso4'] = f'Сульфат магния MgO-{(math.ceil((self.mgso4_mg / 0.603036) * 10) / 10)}% SO3-{(math.ceil((self.mgso4_s / 0.400496) * 10) / 10)}%';
        
        if math.ceil(self.mgso4_mg * 10) / 10 == 9.9:
            captions['mgso4'] = f'Магний сернокислый MgSO4*7H2O'
        
        if math.ceil(self.mgso4_mg * 10) / 10 == 20.2:
            captions['mgso4'] = f'Магний сернокислый MgSO4'
        
        captions[
            'kh2po4'] = f'Монофосфат калия K2O-{(math.ceil((self.kh2po4_k / 0.830148) * 10) / 10)}% P2O5-{(math.ceil((self.kh2po4_p / 0.436421) * 10) / 10)}%';
        if math.ceil(self.kh2po4_k * 10) / 10:
            captions['kh2po4'] = 'Калий фосфорнокислый KH2PO4'
        
        captions[
            'k2so4'] = f'Сульфат калия K2O-{(math.ceil((self.k2so4_k / 0.830148) * 10) / 10)}% SO3-{(math.ceil((self.k2so4_s / 0.400496) * 10) / 10)}%'
        if math.ceil(self.k2so4_k * 10) / 10 == 44.9:
            captions['k2so4'] = 'Калий сернокислый K2SO4'
        
        captions[
            'mgno3'] = f'Селитра магниевая MgO-{math.ceil((self.mgno3_mg / 0.603036) * 10) / 10}% N-{math.ceil((self.mgno3_no3) * 10) / 10}%'
        if math.ceil(self.mgno3_mg * 10) / 10 == 9.5:
            captions['mgno3'] = 'Магний азотнокислый Mg(NO3)2*6H2O'
        if math.ceil(self.mgno3_mg * 10) / 10 == 16.4:
            captions['mgno3'] = 'Магний азотнокислый Mg(NO3)2'
        
        captions[
            'cacl2'] = f'Кальций хлористый CaO-{math.ceil((self.cacl2_ca / 0.714691) * 10) / 10}% Cl-{math.ceil((self.cacl2_cl) * 10) / 10}%'
        if math.ceil(self.cacl2_ca * 10) / 10 == 18.3:
            captions['cacl2'] = 'Хлорид кальция 6-водный CaCl2*6H2O'
        if math.ceil(self.cacl2_ca * 10) / 10 == 36.1:
            captions['cacl2'] = 'Хлорид кальция безводный CaCl2'
        
        if self.nh4 > 0:
            captions['nh4_nh3_ratio'] = f'NH4:NO3 1:{math.ceil((self.no3 / self.nh4))}'
        else:
            captions['nh4_nh3_ratio'] = f'NO3=100%'
        self.captions = captions
        return captions
    
    def sum_salt_grams(self):
        s = 0
        for k, i in self.salt_gramms.items():
            i = getattr(self, i)
            if callable(i):
                i = i()
            s += i
        return s

    @float_exception
    def calc_tbml(self):
        self.calc_concentrates()

    @float_exception
    def calc_taml(self):
        self.calc_concentrates()

    @float_exception
    def calc_gml_cano3(self):
        kmol = self.gl_cano3 / (24.4247 / self.cano3_ca)
        self.gml_cano3 = 0.999 + 0.000732 * kmol - 0.000000113 * kmol ** 2

    @float_exception
    def calc_gml_kno3(self):
        kmol = self.gl_kno3 / (38.6717 / self.kno3_k);
        self.gml_kno3 = 0.998 + 0.00062 * kmol - 0.000000114 * kmol ** 2
        
    @float_exception
    def calc_gml_nh4no3(self):
        kmol =  self.gl_nh4no3 / ((34.9978 / 2) / self.nh4no3_no3 )
        self.gml_nh4no3 = 0.999 + 0.000397 * kmol - 0.0000000422 * kmol**2

    @float_exception
    def calc_gml_mgno3(self):
        kmol = self.gl_mgno3  / ((16.3874) / self.mgno3_mg)
        self.gml_mgno3 = 0.998 + 0.000736 * kmol - 0.000000121 * kmol**2

    @float_exception
    def calc_gml_cacl2(self):
        kmol = self.gl_cacl2 / (36.1115 / self.cacl2_ca)
        self.gml_cacl2 = 0.999 + 0.000794 * kmol - 0.000000151 * kmol**2

    @float_exception
    def calc_gml_mgso4(self):
        kmol = self.gl_mgso4 / ((20.1923) / self.mgso4_mg)
        self.gml_mgso4 = 0.999 + 0.00097 * kmol - 0.000000268 * kmol**2

    @float_exception
    def calc_gml_kh2po4(self):
        kmol = self.gl_kh2po4 / ((28.7307) / self.kh2po4_k)
        self.gml_kh2po4 = 0.998 + 0.000716 * kmol - 0.000000399 * kmol**2

    @float_exception
    def calc_gml_k2so4(self):
        kmol = self.gl_k2so4 / ((44.8737) / self.k2so4_k)
        self.gml_k2so4 = 0.998 + 0.000814 * kmol - 0.00000039 * kmol

    @float_exception
    def calc_conc_micro(self):
        self.calc_concentrates()

    @float_exception
    def conc_errors(self):
        errors = {}
        if self.gml_cano3 > 1.4212:
            errors['gml_cano3'] = True
        else:
            errors['gml_cano3'] = False
        if self.gml_kno3 > 1.1627:
            errors['gml_kno3'] = True
        else:
            errors['gml_kno3'] = False
        if self.gml_nh4no3 > 1.2528:
            errors['gml_nh4no3'] = True
        else:
            errors['gml_nh4no3'] = False
        if self.gml_mgno3 > 1.2013:
            errors['gml_mgno3'] = True
        else:
            errors['gml_mgno3'] = False
        if self.gml_mgso4 > 1.2978:
            errors['gml_mgso4'] = True
        else:
            errors['gml_mgso4'] = False
        if self.gml_kh2po4 > 1.128:
            errors['gml_kh2po4'] = True
        else:
            errors['gml_kh2po4'] = False
        if self.gml_k2so4 > 1.0825:
            errors['gml_k2so4'] = True
        else:
            errors['gml_k2so4'] = False
        if self.gml_cacl2 > 1.3963:
            errors['gml_cacl2'] = True
        else:
            errors['gml_cacl2'] = False
        self.errors = errors

    @float_exception
    def calc_prices(self, pushed_element=None, val=None):
        if pushed_element in PlantProfile.price_fields:
            pass
            # t = getattr(self, pushed_element)
            # setattr(self, t, 'calc')

    @float_exception
    def calc_concentrates(self, pushed_element=None, val=None):
        
        self.calc_gml_cano3()
        self.calc_gml_kno3()
        self.calc_gml_nh4no3()
        self.calc_gml_mgno3()
        self.calc_gml_mgso4()
        self.calc_gml_kh2po4()
        self.calc_gml_k2so4()
        self.calc_gml_cacl2()
            
        if pushed_element in self.concentrate_fields:
            if hasattr(self, "calc_"+pushed_element):
                a = getattr(self, "calc_"+pushed_element )
                if callable(a):
                    a()
                    
            
                
        self.ml_cano3 = self.calc_cano3() / self.gl_cano3 * 1000
        self.ml_kno3 = self.calc_kno3() / self.gl_kno3 * 1000
        self.ml_nh4no3 = self.calc_nh4no3() / self.gl_nh4no3 * 1000
        self.ml_mgno3 = self.calc_mgno3() / self.gl_mgno3 * 1000
        self.ml_mgso4 = self.calc_mgso4() / self.gl_mgso4 * 1000
        self.ml_kh2po4 = self.calc_kh2po4() / self.gl_kh2po4 * 1000
        self.ml_k2so4 = self.calc_k2so4() / self.gl_k2so4 * 1000
        self.ml_cacl2 = self.calc_cacl2() / self.gl_cacl2 * 1000
    
        
        if self.dfe != 0: self.ml_fe=(self.fe / self.dfe * self.litres / 10) / self.gl_fe
        if self.dmn != 0: self.ml_mn=(self.mn / self.dmn * self.litres / 10) / self.gl_mn
        
        if self.db != 0:
            self.ml_b= (self.b / self.db *   self.litres / 10) / self.gl_b
            self.ml_cmplx = (self.b / self.db * self.litres / 10) / self.gl_cmplx
        if self.dzn != 0: self.ml_zn=(self.zn / self.dzn * self.litres / 10) / self.gl_zn
        if self.dcu != 0: self.ml_cu=(self.cu / self.dcu * self.litres / 10) / self.gl_cu
        if self.dmo != 0: self.ml_mo=(self.mo / self.dmo * self.litres / 10) / self.gl_mo
        if self.dco != 0: self.ml_co=(self.co / self.dco * self.litres / 10) / self.gl_co
        if self.dsi != 0: self.ml_si=(self.si / self.dsi * self.litres / 10) / self.gl_si
    
        self.gg_cano3 =  self.gml_cano3 *  self.ml_cano3
        self.gg_kno3 =   self.gml_kno3 *   self.ml_kno3
        self.gg_nh4no3 = self.gml_nh4no3 * self.ml_nh4no3
        self.gg_mgno3 =  self.gml_mgno3 *  self.ml_mgno3
        self.gg_mgso4 =  self.gml_mgso4 *  self.ml_mgso4
        self.gg_kh2po4 = self.gml_kh2po4 * self.ml_kh2po4
        self.gg_k2so4 =  self.gml_k2so4 *  self.ml_k2so4
        self.gg_cacl2 =  self.gml_cacl2 *  self.ml_cacl2
    
        self.gg_cmplx   = self.gml_cmplx * self.ml_cmplx if self.ml_cmplx else 0
        self.gg_fe      = self.gml_fe * self.ml_fe if self.ml_fe else 0
        self.gg_b       = self.gml_b * self.ml_b if self.ml_b else 0
        self.gg_mn      = self.gml_mn * self.ml_mn if self.ml_mn else 0
        self.gg_zn      = self.gml_zn * self.ml_zn if self.ml_zn else 0
        self.gg_cu      = self.gml_cu * self.ml_cu if self.ml_cu else 0
        self.gg_mo      = self.gml_mo * self.ml_mo if self.ml_mo else 0
        self.gg_co      = self.gml_co * self.ml_co if self.ml_co else 0
        self.gg_si      = self.gml_si * self.ml_si if self.ml_si else 0

    
        av = round((self.ml_cano3 + self.ml_kno3 + self.ml_nh4no3 + self.ml_mgno3 + self.ml_cacl2) * 10000) / 10000
        am = round((self.gg_cano3 + self.gg_kno3 + self.gg_nh4no3 + self.gg_mgno3 + self.gg_cacl2) * 10000) / 10000
        ak = round(am / av * 100) / 100
        if self.taml != 0:
            ac  = round(self.litres / self.taml * 1000)
            aw  = round(self.taml - av)
            aml = round(self.taml / self.litres * 1000) / 1000
        
            self.suma = f'объем: {av} мл, вес: {am} гр, плотность: {ak} г/мл. '
            self.lvola = f'концентрат А ({ac}:1) . долить воды: {aw} мл. по {aml} мл на 1л.'
    
        vmlmgso4 = self.ml_mgso4 or 0
        vmlkh2po4 = self.ml_kh2po4 or 0
        vmlk2so4 = self.ml_k2so4 or 0
        vmlfe = self.ml_fe or 0
        vmlmn = self.ml_mn or 0
        vmlb = self.ml_b or 0
        vmlzn = self.ml_zn or 0
        vmlcu = self.ml_cu or 0
        vmlmo = self.ml_mo or 0
        vmlco = self.ml_co or 0
        vmlsi = self.ml_si or 0
    
        if self.micro_calc_mode==self.CalcMicroMode.B:
            bv = round((self.ml_mgso4 + self.ml_kh2po4 + self.ml_k2so4 + self.ml_cmplx) * 10000) / 10000
            bm = round((self.gg_mgso4 + self.gg_kh2po4 + self.gg_k2so4 + self.gg_cmplx) * 10000) / 10000
            bk = round(bm / bv * 1000) / 1000
        else:
         
            bv = vmlmgso4 + vmlkh2po4 + vmlk2so4 + vmlfe + vmlmn + vmlb + vmlzn + vmlmo + vmlcu + vmlco + vmlsi
            bm = round((self.gg_mgso4 + self.gg_kh2po4 + self.gg_k2so4 + self.gg_fe + self.gg_mn + self.gg_b +
                        self.gg_zn + self.gg_mo + self.gg_co + self.gg_si) * 100) / 100
            bk = round(bm / bv * 100) / 100
        
        if self.tbml != 0:
            bc = round(self.litres / self.tbml * 1000)
            bw = round(self.tbml - bv)
            bml= round(self.tbml / self.litres * 1000) / 1000
            self.sumb = f'объем: {round(bv * 10) / 10} мл, вес: {bm} гр, плотность: {bk} г/мл'
            self.lvolb = f'концентрат Б ({bc}:1) . долить воды: {bw} мл. по {bml} мл на 1л.'
        self.conc_errors()
    
    
    
    ca_0 = None
    ca_1 = None
    ca_2 = None
    ca_k = None
    cl_0 = None
    cl_1 = None
    cl_2 = None
    cl_k = None
    ec_0 = None
    ec_1 = None
    k_0 = None
    k_1 = None
    k_2 = None
    k_k = None
    mg_0 = None
    mg_1 = None
    mg_2 = None
    mg_k = None
    n_0 = None
    n_1 = None
    nh4_0 = None
    nh4_1 = None
    nh4_2 = None
    nh4_k = None
    no3_0 = None
    no3_1 = None
    no3_2 = None
    no3_k = None
    p_0 = None
    p_1 = None
    p_2 = None
    p_k = None
    s_0 = None
    s_1 = None
    v_k = None
    v_2 = None
    v_1 = None

    def profile_npk_data(self):
        out = "<table class='table'><tr>"
        for i in PlantProfile.macro:
            out += f"<td>{i}</td>"
        out += '</tr>'
        out += '<tr>'
        for i in PlantProfile.macro:
            out += f"<td>{int(getattr(self,i))}</td>"
        out += '</tr>'
        out += "</table>"
    
        out += "<table class='table'><tr>"
    
        for i in PlantProfile.micro:
            out += f"<td>{i}</td>"
        out += '</tr>'
        out += '<tr>'
        for i in PlantProfile.micro:
            out += f"<td>{int(getattr(self,i))}</td>"
        out += '</tr>'
    
        out += "</table>"
        return out


class PlantTemplate(models.Model):
    def __str__(self):
        return f'{self.name} by {self.profile_owner}'
    
    class Meta:
        ordering = ['name', 'profile_owner']
    
    name = models.CharField(max_length=1024, verbose_name='Имя профиля')
    description = models.TextField(null=True, blank=True)
    profile_owner = models.CharField(max_length=1024, verbose_name='Автор', null=True, blank=True)
    
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.name = self.name.capitalize()
        super(PlantTemplate, self).save()


class PlantProfileHistory(models.Model):
    class Meta:
        ordering = ['pk', 'date']
    
    date = models.DateTimeField(auto_now_add=True)
    profile = models.ForeignKey(PlantProfile, on_delete=models.CASCADE)
    profile_data = models.JSONField(default=dict, null=True, blank=True)
    changed_data = models.JSONField(default=dict, null=True, blank=True)
    history_text = models.TextField(null=True, blank=True)
    history_image =  models.ForeignKey('wagtailimages.Image', on_delete=models.CASCADE, related_name='+', null=True, blank=True,)
    history_image2 = models.ForeignKey(
                            'wagtailimages.Image', on_delete=models.CASCADE, related_name='+', null=True, blank=True,
                        )
    history_image3 = models.ForeignKey(
                            'wagtailimages.Image', on_delete=models.CASCADE, related_name='+', null=True, blank=True,
                        )
    history_image4 = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+', null=True, blank=True,
    )
    
    def profile_npk_data(self):
        d = simplejson.loads(self.profile_data)
        out = "<table class='table'><tr>"
        
        for i in PlantProfile.macro:
            out += f"<td>{i}</td>"
        out += '</tr>'
        out += '<tr>'
        for i in PlantProfile.macro:
            out += f"<td>{int(d.get(i))}</td>"
        out += '</tr>'
        out += "</table>"
        
        out += "<table class='table'><tr>"
        
        for i in PlantProfile.micro:
            out += f"<td>{i}</td>"
        out += '</tr>'
        out += '<tr>'
        for i in PlantProfile.micro:
            out += f"<td>{int(d.get(i))}</td>"
        out += '</tr>'
        
        out += "</table>"
        return out

class PlantProfileShares(models.Model):
    profile = models.ForeignKey(PlantProfile, on_delete=models.CASCADE, verbose_name="Профиль")
    link_name = models.CharField(max_length=100, default=uuid.uuid4, unique=True, verbose_name='Имя ссылки')
    enabled = models.BooleanField(default=True, verbose_name="Включен/активен")
    
# class PlantProfileDesc(models.Model):
#     class Meta:
#         ordering = ['pk', 'date']
#
#     class PSystem(models.TextChoices):
#         nft = 'nft', _('NFT')
#         dwt = 'dwt', _('DWT')
#         cocos = 'cocos', _('Кокосовый субстрат')
#
#     profile = models.ForeignKey(PlantProfile, on_delete=models.CASCADE)
#     system =  models.CharField(max_length=2, choices=PSystem.choices, default=PSystem.cocos, verbose_name='Микро метод расчета')
#     """кококс/двт/гидропоника место:гроубокс, подоконник, улица, балкон  свет:досветка, естественное температура: подогрев, комнатная, уличная комментарий: тут че в фильтры не поместилось писать"""
#
    
    



class Price(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=1024)

 