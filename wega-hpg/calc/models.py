import math

from django.contrib.auth.models import User
from django.core.cache import cache
from django.db import models
from django.utils.translation import gettext_lazy as _

from calc.decorators import float_exception


class MM:
    N = 14.0067
    P = 30.973762
    K = 39.0983
    Ca = 40.078
    Mg = 24.305
    S = 32.065
    Cl = 35.453


# Create your models here.
class PlantProfile(models.Model):
    class CalcMode(models.TextChoices):
        K = 'K', _('Калий сернокислый K2SO4 ')
        Mg = 'Mg', _('Магний азотнокислый Mg(NO3)2*6H2O')
    
    class CalcMicroMode(models.TextChoices):
        U = 'u', _('Все микро соли')
        B = 'b', _('Комплекс по бору')
    
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
    
    salt_gramms = ['cano3', 'kno3', 'nh4no3', 'mgso4', 'kh2po4', 'k2so4', 'mgno3', 'cacl2', ]

    

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
    
    
    
    def concentrate_dict_b(self):
        if self.micro_calc_mode=='u':
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
            }
            return concentrate_dict_b
        else:
            concentrate_dict_b = {
                'mgso4': {'name': 'mgso4', 'data': ['gl_mgso4', 'gml_mgso4', ], 'calc_data': ['ml_mgso4', 'gg_mgso4']},
                'kh2po4': {'name': 'kh2po4', 'data': ['gl_kh2po4', 'gml_kh2po4', ],
                           'calc_data': ['ml_kh2po4', 'gg_kh2po4']},
                'k2so4': {'name': 'k2so4', 'data': ['gl_k2so4', 'gml_k2so4', ], 'calc_data': ['ml_k2so4', 'gg_k2so4']},
                'cmplx': {'name': 'cmplx', 'data': ['gl_cmplx', 'gml_cmplx', ], 'calc_data': ['ml_cmplx', 'gg_cmplx']},
            }
            return concentrate_dict_b
            
    
    salt_dict = {
        'cano3':  {'salt': ['cano3_ca', 'cano3_no3', 'cano3_nh4', ], 'name': 'Кальций азотнокислый',
                  'formula': 'Са(NО3)2*4H2O'},
        'kno3':    {'salt': ['kno3_k', 'kno3_no3', ], 'name': 'Калий азотнокислый', 'formula': 'KNO3'},
        'nh4no3': {'salt': ['nh4no3_nh4', 'nh4no3_no3', ], 'name': 'Аммоний азотнокислый', 'formula': 'NH4NO3'},
        'mgso4':  {'salt': ['mgso4_mg', 'mgso4_s', ], 'name': 'Магний сернокислый', 'formula': 'MgSO4*7H2O'},
        'kh2po4': {'salt': ['kh2po4_k', 'kh2po4_p', ], 'name': 'Калий фосфорнокислый', 'formula': 'KH2PO4'},
        'k2so4':  {'salt': ['k2so4_k', 'k2so4_s', ], 'name': 'Калий сернокислый ', 'formula': 'K2SO4'},
        'mgno3':  {'salt': ['mgno3_mg', 'mgno3_no3', ], 'name': 'Магний азотнокислый', 'formula': 'Mg(NO3)2*6H2O'},
        'cacl2':  {'salt': ['cacl2_ca', 'cacl2_cl', ], 'name': 'Хлорид кальция 6-водный', 'formula': 'CaCl2*6H2O'},
    }
    
    name = models.CharField(max_length=1024, verbose_name='Имя профиля')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ec = models.FloatField(default=0, verbose_name='Ec')
    ppm = models.FloatField(default=0, verbose_name='PPM')
    litres = models.FloatField(default=10)
    
    template = models.ForeignKey('PlantTemplate', on_delete=models.CASCADE, null=True, blank=True)
    from_template = models.ForeignKey('PlantTemplate', on_delete=models.CASCADE, null=True, blank=True,
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
                                       verbose_name='Способ расчета')
    
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
    def calc_micro_vars(self):
        self.agfe =  (self.fe * self.litres) / (self.gmsum * 10000)   if self.fe > 0 else 0
        self.agmn =  (self.mn * self.litres) / (self.gmsum * 10000)   if self.mn > 0 else 0
        self.agb  =  (self.b * self.litres)  / (self.gmsum * 10000)   if self.b  > 0 else 0
        self.agzn =  (self.zn * self.litres) / (self.gmsum * 10000)   if self.zn > 0 else 0
        self.agcu =  (self.cu * self.litres) / (self.gmsum * 10000)   if self.cu > 0 else 0
        self.agmo =  (self.mo * self.litres) / (self.gmsum * 10000)   if self.mo > 0 else 0
        self.agco =  (self.co * self.litres) / (self.gmsum * 10000)   if self.co > 0 else 0
        self.agsi =  (self.si * self.litres) / (self.gmsum * 10000)   if self.si > 0 else 0
    
 
    
    def weight_to_micro(self):
        self.fe = 10000 * self.gfe * (self.dfe / self.litres)
        self.mn = 10000 * self.gmn * (self.dmn / self.litres)
        self.b  = 10000 * self.gb * (self.db /   self.litres)
        self.zn = 10000 * self.gzn * (self.dzn / self.litres)
        self.cu = 10000 * self.gcu * (self.dcu / self.litres)
        self.mo = 10000 * self.gmo * (self.dmo / self.litres)
        self.co = 10000 * self.gco * (self.dco / self.litres)
        self.si = 10000 * self.gsi * (self.dsi / self.litres)

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
            
    
        
    def calc_micro(self, pushed_element=None, val=None):
        # print('calc_micro pushed_element', pushed_element)
        self.bor_complex = None
        recalc_gmsum= True
        
        if not any([self.gfe + self.gmn + self.gb + self.gzn + self.gcu + self.gmo + self.gco + self.gsi]):
            self.micro_to_weight(recalc_gmsum=False)
            
        if pushed_element and pushed_element == 'micro_calc_mode':
            recalc_gmsum = False
            if  val=='b':
                self.gmsum = self.gfe + self.gmn + self.gb + self.gzn + self.gcu + self.gmo + self.gco + self.gsi
            else:
                self.gmsum = self.b / self.db * self.litres / 10000
        else:
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
            self.micro_to_weight(recalc_gmsum=recalc_gmsum)
            
        if self.micro_calc_mode==self.CalcMicroMode.U:
            
            self.micro_sostav = f'Состав: Fe={round(self.agfe * 1000) / 1000}%' \
                                f' Mn={(round(self.agmn * 1000) / 1000)}%' \
                                f' B={round(self.agb * 1000) / 1000}%' \
                                f' Zn={round(self.agzn * 1000) / 1000}%' \
                                f' Cu={round(self.agcu * 1000) / 1000}%' \
                                f' Mo={round(self.agmo * 1000) / 1000}%' \
                                f' Co={round(self.agco * 1000) / 1000}%' \
                                f' Si={round(self.agsi * 1000) / 1000}%'
            
     
        
        if pushed_element == 'weight_micro':
            self.gmsum = float(val)
            self.b = 10000 * self.gmsum * (self.db / self.litres)
      
        if self.v_micro > 0:
            self.micro_text = f'Концентрация: {round(self.gmsum * 1000 / self.v_micro * 100) / 100} г/л,' \
                              f'Кратность: {round(self.litres / self.v_micro * 1000)}:1,' \
                              f'Расход: {round(self.v_micro / self.litres * 10) / 10} мл/л раствора'
                        
      
    
    def weight_micro(self):
        if self.micro_calc_mode == self.CalcMicroMode.B:
            return self.calc_bor_complex()
        else:
            return self.gfe + self.gmn + self.gzn + self.gcu + self.gmo + self.gco + self.gsi
    
    def calc_bor_complex(self):
        
        if self.b > 0:
            bor_complex = self.b / self.db * self.litres / 10000
        else:
            bor_complex = 0
        return bor_complex
    
    def k_mg(self):
        return round(self.k / self.mg, 3)
    
    def k_ca(self):
        return round(self.k / self.ca, 3)
    
    def k_n(self):
        return round(self.k / self.n, 3)
    
    def get_npk(self):
        t = self.get_matrix()[0]
    
    
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
    
    def get_npk_magazine(self):
        a = f"NPK: {math.ceil(self.n / 10)}-{math.ceil(self.p / 0.436421 / 10)}-{math.ceil(self.k / 0.830148 / 10)} " \
            f"CaO={(math.ceil(self.ca / 0.714691 / 10) * 10 / 10)}% MgO={math.ceil(self.mg / 0.603036 / 10 * 10) / 10}%" \
            f"SO3={math.ceil(self.s / 0.400496 / 10 * 10) / 10}"
        return a
    
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
    
    def recalc(self, pushed_element=None, val=None):
        m = MM()
        
        if pushed_element == 'nh4_nh3_ratio':
            self.nh4 = self.n * (self.nh4_nh3_ratio / (self.nh4_nh3_ratio + 1))
            self.no3 = self.n / (self.nh4_nh3_ratio + 1)
        
        if pushed_element and 'matrix' in pushed_element:
            t, a, b, = pushed_element.split('-')
            
            old = getattr(self, b)
            new = getattr(self, a) / float(val)
            
            if b == 'n':
                m_delta = new / old
                if self.nh4 and self.no3:
                    t1 = self.nh4 * m_delta
                    t2 = self.no3 * m_delta
                    
                    self.nh4 = t1
                    self.no3 = t2
                
                elif self.nh4 and not self.no3:
                    t = self.nh4 * m_delta
                    self.nh4 = t
                
                elif not self.nh4 and self.no3:
                    t = self.no3 * m_delta
                    self.no3 = t
            
            setattr(self, b, new)
        
        if pushed_element == 'ec':
            # сделал раунд до 3х знаков, чтобы соотвествовало старой версии
            # серу считает с учетом хлора - в старой бага
            r_n = (self.k_mg() * self.k_ca()) / \
                  (
                          self.k_ca() * self.k_n() + self.k_mg() * self.k_n() + self.k_mg() * self.k_ca() + self.k_mg() * self.k_ca() * self.k_n())
            r_k = (self.k_n() * self.k_mg() * self.k_ca()) / (
                    self.k_ca() * self.k_n() + self.k_mg() * self.k_n() + self.k_mg() * self.k_ca() + self.k_mg() * self.k_ca() * self.k_n())
            r_ca = (self.k_mg() * self.k_n()) / (
                    self.k_ca() * self.k_n() + self.k_mg() * self.k_n() + self.k_mg() * self.k_ca() + self.k_mg() * self.k_ca() * self.k_n())
            r_mg = (self.k_ca() * self.k_n()) / (
                    self.k_ca() * self.k_n() + self.k_mg() * self.k_n() + self.k_mg() * self.k_ca() + self.k_mg() * self.k_ca() * self.k_n())
            r_nh4 = (r_n * self.nh4_nh3_ratio) / (1 + self.nh4_nh3_ratio)
            self.ec = float(val)
            
            r = (0.10526315789473684211 * m.N * m.Ca * m.Mg * m.K * (100 * self.ec - 19)) / \
                (
                        r_nh4 * m.Ca * m.Mg * m.K +
                        2 * r_ca * m.N * m.Mg * m.K +
                        2 * r_mg * m.N * m.Ca * m.K +
                        r_k * m.N * m.Ca * m.Mg)
            
            self.n = r_n * r
            self.k = r_k * r
            self.ca = r_ca * r
            self.mg = r_mg * r
            self.nh4 = r_nh4 * r
            self.no4 = self.n - self.nh4
            self.s = self.calc_s()
        
        if pushed_element in self.salt_gramms:
            val = float(val)
            if pushed_element == 'cano3':
                n_no3 = (val * self.cano3_no3 + self.nh4no3_no3 * self.nh4no3() + self.kno3() * self.kno3_no3 +
                         self.mgno3() * self.mgno3_no3)
                n_nh4 = (val * self.cano3_nh4 + self.nh4no3() * self.nh4no3_nh4)
                n_n = n_no3 + n_nh4
                n_p = (self.kh2po4() * self.kh2po4_p)
                n_k = (self.kno3() * self.kno3_k + self.kh2po4() * self.kh2po4_k + self.k2so4() * self.k2so4_k)
                n_ca = (val * self.cano3_ca + self.cacl2() * self.cacl2_ca)
                n_mg = (self.mgso4() * self.mgso4_mg + self.mgno3() * self.mgno3_mg)
                n_nhno3 = n_nh4 / n_no3
                n_cl = (self.cacl2() * self.cacl2_cl)
                self.nh4_nh3_ratio = n_nhno3
                self.n = n_n
                self.p = n_p
                self.k = n_k
                self.ca = n_ca
                self.mg = n_mg
                self.cl = n_cl
            
            if pushed_element == 'kno3':
                n_no3 = (self.cano3() * self.cano3_no3 + self.nh4no3_no3 * self.nh4no3() + val * self.kno3_no3 +
                         self.mgno3() * self.mgno3_no3)
                n_nh4 = (self.cano3() * self.cano3_nh4 + self.nh4no3() * self.nh4no3_nh4)
                n_n = n_no3 + n_nh4
                n_p = (self.kh2po4() * self.kh2po4_p)
                n_k = (val * self.kno3_k + self.kh2po4() * self.kh2po4_k + self.k2so4() * self.k2so4_k)
                n_ca = (self.cano3() * self.cano3_ca + self.cacl2() * self.cacl2_ca)
                n_mg = (self.mgso4() * self.mgso4_mg + self.mgno3() * self.mgno3_mg)
                n_nhno3 = n_nh4 / n_no3
                n_cl = (self.cacl2() * self.cacl2_cl)
                self.nh4_nh3_ratio = n_nhno3
                self.n = n_n
                self.p = n_p
                self.k = n_k
                self.ca = n_ca
                self.mg = n_mg
                self.cl = n_cl
            
            if pushed_element == 'nh4no3':
                n_no3 = (self.cano3() * self.cano3_no3 + self.nh4no3_no3 * val + self.kno3() * self.kno3_no3 +
                         self.mgno3() * self.mgno3_no3)
                n_nh4 = (self.cano3() * self.cano3_nh4 + val * self.nh4no3_nh4)
                n_n = n_no3 + n_nh4
                n_p = (self.kh2po4() * self.kh2po4_p)
                n_k = (self.kno3() * self.kno3_k + self.kh2po4() * self.kh2po4_k + self.k2so4() * self.k2so4_k)
                n_ca = (self.cano3() * self.cano3_ca + self.cacl2() * self.cacl2_ca)
                n_mg = (self.mgso4() * self.mgso4_mg + self.mgno3() * self.mgno3_mg)
                n_nhno3 = n_nh4 / n_no3
                n_cl = (self.cacl2() * self.cacl2_cl)
                self.nh4_nh3_ratio = n_nhno3
                self.n = n_n
                self.p = n_p
                self.k = n_k
                self.ca = n_ca
                self.mg = n_mg
                self.cl = n_cl
            
            if pushed_element == 'mgso4':
                n_no3 = (self.cano3() * self.cano3_no3 + self.nh4no3_no3 * self.nh4no3() + self.kno3() * self.kno3_no3 +
                         self.mgno3() * self.mgno3_no3)
                n_nh4 = (self.cano3() * self.cano3_nh4 + self.nh4no3() * self.nh4no3_nh4)
                n_n = n_no3 + n_nh4
                n_p = (self.kh2po4() * self.kh2po4_p)
                n_k = (self.kno3() * self.kno3_k + self.kh2po4() * self.kh2po4_k + self.k2so4() * self.k2so4_k)
                n_ca = (self.cano3() * self.cano3_ca + self.cacl2() * self.cacl2_ca)
                n_mg = (val * self.mgso4_mg + self.mgno3() * self.mgno3_mg)
                n_nhno3 = n_nh4 / n_no3
                n_cl = (self.cacl2() * self.cacl2_cl)
                self.nh4_nh3_ratio = n_nhno3
                self.n = n_n
                self.p = n_p
                self.k = n_k
                self.ca = n_ca
                self.mg = n_mg
                self.cl = n_cl
            
            if pushed_element == 'kh2po4':
                n_no3 = (self.cano3() * self.cano3_no3 + self.nh4no3_no3 * self.nh4no3() + self.kno3() * self.kno3_no3 +
                         self.mgno3() * self.mgno3_no3)
                n_nh4 = (self.cano3() * self.cano3_nh4 + self.nh4no3() * self.nh4no3_nh4)
                n_n = n_no3 + n_nh4
                n_p = (val * self.kh2po4_p)
                n_k = (self.kno3() * self.kno3_k + val * self.kh2po4_k + self.k2so4() * self.k2so4_k)
                n_ca = (self.cano3() * self.cano3_ca + self.cacl2() * self.cacl2_ca)
                n_mg = (self.mgso4() * self.mgso4_mg + self.mgno3() * self.mgno3_mg)
                n_nhno3 = n_nh4 / n_no3
                n_cl = (self.cacl2() * self.cacl2_cl)
                self.nh4_nh3_ratio = n_nhno3
                self.n = n_n
                self.p = n_p
                self.k = n_k
                self.ca = n_ca
                self.mg = n_mg
                self.cl = n_cl
            
            if pushed_element == 'k2so4':
                n_no3 = (self.cano3() * self.cano3_no3 + self.nh4no3_no3 * self.nh4no3() + self.kno3() * self.kno3_no3 +
                         self.mgno3() * self.mgno3_no3)
                n_nh4 = (self.cano3() * self.cano3_nh4 + self.nh4no3() * self.nh4no3_nh4)
                n_n = n_no3 + n_nh4
                n_p = (self.kh2po4() * self.kh2po4_p)
                n_k = (self.kno3() * self.kno3_k + self.kh2po4() * self.kh2po4_k + val * self.k2so4_k)
                n_ca = (self.cano3() * self.cano3_ca + self.cacl2() * self.cacl2_ca)
                n_mg = (self.mgso4() * self.mgso4_mg + self.mgno3() * self.mgno3_mg)
                n_nhno3 = n_nh4 / n_no3
                n_cl = (self.cacl2() * self.cacl2_cl)
                self.nh4_nh3_ratio = n_nhno3
                self.n = n_n
                self.p = n_p
                self.k = n_k
                self.ca = n_ca
                self.mg = n_mg
                self.cl = n_cl
            
            if pushed_element == 'mgno3':
                n_no3 = (self.cano3() * self.cano3_no3 + self.nh4no3_no3 * self.nh4no3() + self.kno3() * self.kno3_no3 +
                         val * self.mgno3_no3)
                n_nh4 = (self.cano3() * self.cano3_nh4 + self.nh4no3() * self.nh4no3_nh4)
                n_n = n_no3 + n_nh4
                n_p = (self.kh2po4() * self.kh2po4_p)
                n_k = (self.kno3() * self.kno3_k + self.kh2po4() * self.kh2po4_k + self.k2so4() * self.k2so4_k)
                n_ca = (self.cano3() * self.cano3_ca + self.cacl2() * self.cacl2_ca)
                n_mg = (self.mgso4() * self.mgso4_mg + val * self.mgno3_mg)
                n_nhno3 = n_nh4 / n_no3
                n_cl = (self.cacl2() * self.cacl2_cl)
                self.nh4_nh3_ratio = n_nhno3
                self.n = n_n
                self.p = n_p
                self.k = n_k
                self.ca = n_ca
                self.mg = n_mg
                self.cl = n_cl
            
            if pushed_element == 'cacl2':
                n_no3 = (self.cano3() * self.cano3_no3 + self.nh4no3_no3 * self.nh4no3() + self.kno3() * self.kno3_no3 +
                         self.mgno3() * self.mgno3_no3)
                n_nh4 = (self.cano3() * self.cano3_nh4 + self.nh4no3() * self.nh4no3_nh4)
                n_n = n_no3 + n_nh4
                n_p = (self.kh2po4() * self.kh2po4_p)
                n_k = (self.kno3() * self.kno3_k + self.kh2po4() * self.kh2po4_k + self.k2so4() * self.k2so4_k)
                n_ca = (self.cano3() * self.cano3_ca + val * self.cacl2_ca)
                n_mg = (self.mgso4() * self.mgso4_mg + self.mgno3() * self.mgno3_mg)
                n_nhno3 = n_nh4 / n_no3
                n_cl = (val * self.cacl2_cl)
                
                self.nh4_nh3_ratio = n_nhno3
                self.n = n_n
                self.p = n_p
                self.k = n_k
                self.ca = n_ca
                self.mg = n_mg
                self.cl = n_cl
            setattr(self, pushed_element, float(val))
        
        if pushed_element == 'nh4':
            t = self.n - self.nh4
            self.no3 = t
            self.n = self.no3 + self.nh4
        
        elif pushed_element == 'no3':
            t = self.n - self.no3
            self.nh4 = t
            self.n = self.no3 + self.nh4
        
        if pushed_element == 'n':
            self.no3 = self.n / (self.nh4_nh3_ratio + 1)
            self.nh4 = self.nh4_nh3_ratio * self.n / (self.nh4_nh3_ratio + 1)
        
        if pushed_element not in ['s', 'litres']:
            self.s = self.calc_s()
        
        if pushed_element not in ['ca', 'litres']:
            self.ca = self.calc_ca()
        
        if pushed_element == 'cano3_ca':
            self.cano3_no3 = (2 * self.cano3_ca * m.N + self.cano3_nh4 * m.Ca) / m.Ca
        
        if pushed_element == 'kno3_k':
            self.kno3_no3 = (self.kno3_k * m.N) / m.K
        
        if pushed_element == 'kno3_no3':
            self.kno3_k = (self.kno3_no3 * m.K) / m.N
        
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
        
        if pushed_element in self.micro or pushed_element in self.salt_micro_gramm \
                or pushed_element in self.salt_micro_persent or val in ['b', 'B', 'u', 'U'] \
                or pushed_element in ['weight_micro', 'v_micro']:
            self.calc_micro(pushed_element=pushed_element, val=val)
        
        self.captions = self.calc_captions()
        if pushed_element in self.concentrate_fields:
            a = getattr(self, "calc_"+pushed_element)
            if callable(a):
                a()
        for i in self.salt_gramms:
            a = getattr(self, i)
            if callable(a):
                a = a()
            setattr(self, i, a)
        
        
        
            
            
        
        self.ec = self.calc_ec()
        self.ppm = self.calc_ppm()
        self.npk = self.get_npk()
        self.npk_formula = self.calc_npk_formula()
        self.npk_magazine = self.get_npk_magazine()
        self.salt_grams = self.sum_salt_grams()
    
    def to_json(self):
        
        data = {'pk': self.pk,
                'ec': "{:.2f}".format(self.ec),
                'ppm': "{:.2f}".format(self.ppm),
                'litres': self.litres,
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
            data[s] = "{:.3f}".format(getattr(self, s))
        
        for s in self.concentrate_fields:
            t = getattr(self, s)
            if t:
                data[s] = "{:.2f}".format(t)
        
        for s, d in self.salt_dict.items():
            data[s] = "{:.2f}".format(getattr(self, s))
            for i in d.get('salt'):
                data[i] = "{:.2f}".format(getattr(self, i))
        
        matrix = self.get_matrix(as_dict=True)
        for k, i in matrix.items():
            if i:
                data[f'matrix-{k}'] = "{:.2f}".format(i)
            else:
                data[f'matrix-{k}'] = 0
        
        return data
    
    def calc_ppm(self):
        ppm = round((self.n + self.p + self.k + self.ca + self.mg + self.s + self.cl) * 100) / 100
        return ppm
    
    @float_exception
    def get_salt_dict(self):
        return self.salt_dict
    
    @float_exception
    def kh2po4(self):
        a = self.p / self.kh2po4_p
        return a * self.litres / 10
    
    def calc_ec(self):
        
        m = MM()
        a = self.nh4 * m.Ca * m.Mg * m.K
        b = self.ca * m.N * m.Mg * m.K
        c = self.mg * m.N * m.Ca * m.K
        d = self.k * m.N * m.Ca * m.Mg
        e = m.N * m.Ca * m.Mg * m.K
        f = m.N * m.Ca * m.Mg * m.K
        ec = 0.095 * (a + 2 * b + 2 * c + d + 2 * e) / f
        return ec
    
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
    def kno3(self):
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
    def cano3(self):
        a = self.ca * self.cacl2_cl - self.cl * self.cacl2_ca
        b = self.cano3_ca * self.cacl2_cl
        c = a / b
        return c * self.litres / 10
    
    @float_exception
    def mgso4(self):
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
    def k2so4(self):
        if self.calc_mode == self.CalcMode.K:
            a = self.s * self.mgso4_mg - self.mg * self.mgso4_s
            b = self.k2so4_s * self.mgso4_mg
            c = a / b
            return c * self.litres / 10
        return 0
    
    @float_exception
    def nh4no3(self):
        a = self.nh4 * self.cano3_ca * self.cacl2_cl
        b = self.cano3_nh4 * self.ca * self.cacl2_cl
        c = self.cano3_nh4 * self.cl * self.cacl2_ca
        d = self.nh4no3_nh4 * self.cano3_ca * self.cacl2_cl
        e = -(-a + b - c) / d
        return e * self.litres / 10
    
    @float_exception
    def cacl2(self):
        a = self.cl
        b = self.cacl2_cl
        c = a / b
        return c * self.litres / 10
    
    @float_exception
    def mgno3(self):
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
        for i in self.salt_gramms:
            i = getattr(self, i)
            if callable(i):
                i = i()
            s += i
        return s

  
    def calc_tbml(self):
        self.calc_concentrates()
        
        
    def calc_taml(self):
        self.calc_concentrates()
    def calc_gml_cano3(self):
        self.calc_concentrates()
    def calc_gml_kno3(self):
        self.calc_concentrates()
    def calc_gml_nh4no3(self):
        self.calc_concentrates()
    def calc_gml_mgno3(self):
        self.calc_concentrates()
    def calc_gml_mgso4(self):
        self.calc_concentrates()
    def calc_gml_kh2po4(self):
        self.calc_concentrates()
    def calc_gml_k2so4(self):
        self.calc_concentrates()
    def calc_gml_cacl2(self):
        self.calc_concentrates()
        
    def calc_gl_cano3(self):
        kmol = self.gl_cano3 / (24.4247 / self.cano3_ca)
        self.gml_cano3 = 0.999 + 0.000732 * kmol - 0.000000113 * kmol**2
        self.calc_concentrates()
    def calc_gl_kno3(self):
        kmol = self.gl_kno3/ (38.6717 / self.kno3_k);
        self.gml_kno3 = 0.998 + 0.00062 * kmol - 0.000000114 * kmol**2
        self.calc_concentrates()
        
    def calc_gl_nh4no3(self):
        kmol =  self.gl_nh4no3 / ((34.9978 / 2) / self.nh4no3_no3 )
        self.gml_nh4no3 = 0.999 + 0.000397 * kmol - 0.0000000422 * kmol**2
        self.calc_concentrates()
    
    def calc_gl_mgno3(self):
        kmol = self.gl_mgno3  / ((16.3874) / self.mgno3_mg)
        self.gml_mgno3 = 0.998 + 0.000736 * kmol - 0.000000121 * kmol**2
        self.calc_concentrates()
    def calc_gl_cacl2(self):
        kmol = self.gl_cacl2 / (36.1115 / self.cacl2_ca)
        self.gml_cacl2 = 0.999 + 0.000794 * kmol - 0.000000151 * kmol**2
        self.calc_concentrates()
    
    def calc_gl_mgso4(self):
        kmol = self.gl_mgso4 / ((20.1923) / self.mgso4_mg)
        self.gml_mgso4 = 0.999 + 0.00097 * kmol - 0.000000268 * kmol**2
        self.calc_concentrates()
    
    def calc_gl_kh2po4(self):
        kmol = self.gl_kh2po4 / ((28.7307) / self.kh2po4_k)
        self.gml_kh2po4 = 0.998 + 0.000716 * kmol - 0.000000399 * kmol**2
        self.calc_concentrates()
        
    def calc_gl_k2so4(self):
        kmol = self.gl_k2so4 / ((44.8737) / self.k2so4_k)
        self.gml_k2so4 = 0.998 + 0.000814 * kmol - 0.00000039 * kmol
        self.calc_concentrates()
    
    def calc_conc_micro(self):
        self.calc_concentrates()
        
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

    def calc_concentrates(self):
    
        self.ml_cano3 = self.cano3() / self.gl_cano3 * 1000
        self.ml_kno3 = self.kno3() / self.gl_kno3 * 1000
        self.ml_nh4no3 = self.nh4no3() / self.gl_nh4no3 * 1000
        self.ml_mgno3 = self.mgno3() / self.gl_mgno3 * 1000
        self.ml_mgso4 = self.mgso4() / self.gl_mgso4 * 1000
        self.ml_kh2po4 = self.kh2po4() / self.gl_kh2po4 * 1000
        self.ml_k2so4 = self.k2so4() / self.gl_k2so4 * 1000
        self.ml_cacl2 = self.cacl2() / self.gl_cacl2 * 1000
    

        if self.db != 0:  self.ml_cmplx=(self.b / self.db * self.litres / 10)/ self.gl_cmplx
        if self.dfe != 0: self.ml_fe=(self.fe / self.dfe * self.litres / 10) / self.gl_fe
        if self.dmn != 0: self.ml_mn=(self.mn / self.dmn * self.litres / 10) / self.gl_mn
        if self.db != 0:  self.ml_b= (self.b / self.db *   self.litres / 10) / self.gl_b
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


class Price(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=1024)
