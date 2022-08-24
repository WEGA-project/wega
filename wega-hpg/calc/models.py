import math

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

from calc.decorators import float_exception


class MM:
    N = float(14.0067)
    P = float(30.973762)
    K = float(39.0983)
    Ca = float(40.078)
    Mg = float(24.305)
    S = float(32.065)
    Cl = float(35.453)


# Create your models here.
class PlantProfile(models.Model):
    class CalcMode(models.TextChoices):
        K = 'K', _('Калий сернокислый K2SO4 ')
        Mg = 'Mg', _('Магний азотнокислый Mg(NO3)2*6H2O')
    
    macro = ['n', 'no3', 'nh4', 'p', 'k', 'ca', 'mg', 's', 'cl', ]
    macro_matrix = ['n', 'p', 'k', 'ca', 'mg', 's', ]
    micro = ['fe', 'N', 'b', 'zn', 'cu', 'mo', 'co', 'si', ]
    salt = ['cano3_ca', 'cano3_no3', 'cano3_nh4', 'kno3_k', 'kno3_no3', 'nh4no3_nh4', 'nh4no3_no3', 'mgso4_mg',
            'mgso4_s', 'kh2po4_k', 'kh2po4_p', 'k2so4_k', 'k2so4_s', 'mgno3_mg', 'mgno3_no3', 'cacl2_ca', 'cacl2_cl', ]
    
    # salt_gramms=['cano3','kno3','nh4no3','mgso4','kh2po4','k2so4','mgno3','cacl2',]
    salt_gramms = ['cano3', 'kno3', 'nh4no3', 'mgso4', 'kh2po4', 'k2so4', 'mgno3', 'cacl2', ]
    
    salt_dict = {
        'cano3': {'salt': ['cano3_ca', 'cano3_no3', 'cano3_nh4', ], 'name': 'Кальций азотнокислый',
                  'formula': 'Са(NО3)2*4H2O'},
        'kno3': {'salt': ['kno3_k', 'kno3_no3', ], 'name': 'Калий азотнокислый', 'formula': 'Ca(NO3)2'},
        'nh4no3': {'salt': ['nh4no3_nh4', 'nh4no3_no3', ], 'name': 'Аммоний азотнокислый', 'formula': 'NH4NO3'},
        'mgso4': {'salt': ['mgso4_mg', 'mgso4_s', ], 'name': 'Магний сернокислый', 'formula': 'MgSO4*7H2O'},
        'kh2po4': {'salt': ['kh2po4_k', 'kh2po4_p', ], 'name': 'Калий фосфорнокислый', 'formula': 'KH2PO4'},
        'k2so4': {'salt': ['k2so4_k', 'k2so4_s', ], 'name': 'Калий сернокислый ', 'formula': 'K2SO4'},
        'mgno3': {'salt': ['mgno3_mg', 'mgno3_no3', ], 'name': 'Магний азотнокислый', 'formula': 'Mg(NO3)2*6H2O'},
        'cacl2': {'salt': ['cacl2_ca', 'cacl2_cl', ], 'name': 'Хлорид кальция 6-водный', 'formula': 'CaCl2*6H2O'},
    }
    
    name = models.CharField(max_length=1024, verbose_name='Имя профиля')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ec = models.FloatField(default=0, verbose_name='Ec')
    ppm = models.FloatField(default=0, verbose_name='PPM')
    litres = models.PositiveIntegerField(default=10)
    
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
    N = models.FloatField(default=0, verbose_name='N')
    b = models.FloatField(default=0, verbose_name='B')
    zn = models.FloatField(default=0, verbose_name='Zn')
    cu = models.FloatField(default=0, verbose_name='Cu')
    mo = models.FloatField(default=0, verbose_name='Mo')
    co = models.FloatField(default=0, verbose_name='Co')
    si = models.FloatField(default=0, verbose_name='Si')
    
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
    
    def get_npk(self):
        t = self.get_matrix()[0]


    @float_exception
    def calc_npk_formula(self):
        a = f"{math.ceil(float(self.n) / float(self.n) * 100) / 100} : {math.ceil(float(self.p) / float(self.n) * 100) / 100} : " \
            f"{math.ceil(float(self.k) / float(self.n) * 100) / 100} : " \
            f"{math.ceil(float(self.ca) / float(self.n) * 100) / 100} : {math.ceil(float(self.mg) / float(self.n) * 100) / 100} : " \
            f"{math.ceil(float(self.s) / float(self.n) * 100) / 100} : " \
            f"{math.ceil(float(self.cl) / float(self.n) * 100) / 100} sPPM={ self.calc_ppm()}"
        return a
    
    def get_npk_magazine(self):
        a = f"NPK: {math.ceil(float(self.n)/10)}-{math.ceil(float(self.p) / 0.436421 / 10)}-{math.ceil(float(self.k) / 0.830148 / 10)} " \
            f"CaO={(math.ceil(float(self.ca) / 0.714691 / 10) * 10 / 10)}% MgO={math.ceil(float(self.mg) / 0.603036 / 10 * 10) / 10 }%" \
            f"SO3={math.ceil(float(self.s) / 0.400496 / 10 * 10) / 10}"
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
            cur_cal = getattr(pp, cur_element.lower()) or float(0)
            for i in self.macro_matrix:
                val = getattr(pp, i.lower()) or float(0)
                if val is None or cur_cal is None or cur_cal == 0:
                    row[i] = None
                    matrix_dict[f"{i}-{cur_element}"] = None
                else:
                    
                    try:
                        t = round(float(val) / float(cur_cal), 2)
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
    
    def recalc(self, pushed_element=None):
        if not pushed_element == 's':
            self.s = "{:.2f}".format(self.calc_s())
        if pushed_element != 'ca':
            self.ca = "{:.2f}".format(self.calc_ca())
        
        if pushed_element in ['nh4', 'no3']:
            self.n = "{:.2f}".format(float(self.no3) + float(self.nh4))
    
        for i in self.salt_gramms:
            a = getattr(self, i)()
            setattr(self, i, "{:.2f}".format(a / 10))
        
        self.ec =  "{:.2f}".format(self.calc_ec() )
        self.ppm = "{:.2f}".format(0 )
        self.npk = self.get_npk()
        self.npk_formula = self.calc_npk_formula()
        self.npk_magazine = self.get_npk_magazine()
    
    def to_json(self):
        
        
        
        data = {'pk': self.pk, 'ec': self.ec, 'ppm': self.ppm, 'npk': self.npk,
                'npk_formula':self.npk_formula, 'npk_magazine':self.npk_magazine }
        for s in self.macro:
            data[s] = getattr(self, s)
        
        for s in self.micro:
            data[s] = getattr(self, s)
        
        for s, d in self.salt_dict.items():
            data[s] = getattr(self, s)
            for i in d.get('salt'):
                data[i] = getattr(self, i)
        
        matrix = self.get_matrix(as_dict=True)
        for k, i in matrix.items():
            data[f'matrix-{k}'] = "{:.2f}".format(i)
        
        return data
    
    
    def calc_ppm(self):
        ppm = round((float(self.n)+ float(self.p) + float(self.k) + float(self.ca) + float(self.mg) + float(self.s) + float(self.cl)) * 100  ) / 100
        return ppm
    
    
    @float_exception
    def get_salt_dict(self):
        return self.salt_dict
    
    @float_exception
    def kh2po4(self):
        a = float(self.p) / float(self.kh2po4_p)
        return a * self.litres
    
    def calc_ec(self):
        
        m = MM()
        a = float(self.nh4) * m.Ca * m.Mg * m.K
        b = float(self.ca) * m.N * m.Mg * m.K
        c = float(self.mg) * m.N * m.Ca * m.K
        d = float(self.k) * m.N * m.Ca * m.Mg
        e = m.N * m.Ca * m.Mg * m.K
        f = m.N * m.Ca * m.Mg * m.K
        ec = 0.095 * (a + 2 * b + 2 * c + d + 2 * e) / f
        return ec
    
    def calc_ca(self):
        m = MM()
        b = float(self.nh4) * m.P * m.Mg * m.K * m.S * m.Cl
        c = float(self.p) * m.N * m.Mg * m.K * m.S * m.Cl
        d = float(self.mg) * m.N * m.P * m.K * m.S * m.Cl
        e = float(self.k) * m.N * m.P * m.Mg * m.S * m.Cl
        f = float(self.no3) * m.P * m.Mg * m.K * m.S * m.Cl
        g = float(self.s) * m.N * m.P * m.Mg * m.K * m.Cl
        h = float(self.cl) * m.N * m.P * m.Mg * m.K * m.S
        i = m.N * m.P * m.Mg * m.K * m.S * m.Cl
        ans = (-m.Ca * (b - c + 2 * d + e - f - 2 * g - h)) / (2 * i)
        
        return ans
    
    @float_exception
    def kno3(self):
        if self.calc_mode == self.CalcMode.K:
            a = float(self.k) * float(self.kh2po4_p) * float(self.k2so4_s) * float(self.mgso4_mg)
            b = float(self.p) * float(self.kh2po4_k) * float(self.k2so4_s) * float(self.mgso4_mg)
            c = float(self.k2so4_k) * float(self.kh2po4_p) * float(self.s) * float(self.mgso4_mg)
            d = float(self.k2so4_k) * float(self.kh2po4_p) * float(self.mg) * float(self.mgso4_s)
            e = float(self.kno3_k) * float(self.kh2po4_p) * float(self.k2so4_s) * float(self.mgso4_mg)
            f = -(-a + b + c - d) / e
            return f * self.litres
        else:
            a = float(self.k) * float(self.kh2po4_p) - float(self.p) * float(self.kh2po4_k)
            b = float(self.kno3_k) * float(self.kh2po4_p)
            return (a / b) * self.litres
        return 0
    
    @float_exception
    def cano3(self):
        a = float(self.ca) * float(self.cacl2_cl) - float(self.cl) * float(self.cacl2_ca)
        b = float(self.cano3_ca) * float(self.cacl2_cl)
        c = a / b
        return c * self.litres
    
    @float_exception
    def mgso4(self):
        if self.calc_mode == self.CalcMode.K:
            a = float(self.mg)
            b = float(self.mgso4_mg)
            c = a / b
            return c * self.litres
        else:
            a = float(self.s)
            b = float(self.mgso4_s)
            c = a / b
            return c * self.litres
        return 0
    
    @float_exception
    def k2so4(self):
        if self.calc_mode == self.CalcMode.K:
            a = float(self.s) * float(self.mgso4_mg) - float(self.mg) * float(self.mgso4_s)
            b = float(self.k2so4_s) * float(self.mgso4_mg)
            c = a / b
            return c * self.litres
        return 0
    
    @float_exception
    def nh4no3(self):
        a = float(self.nh4) * float(self.cano3_ca) * float(self.cacl2_cl)
        b = float(self.cano3_nh4) * float(self.ca) * float(self.cacl2_cl)
        c = float(self.cano3_nh4) * float(self.ca) * float(self.cacl2_ca)
        d = float(self.nh4no3_nh4) * float(self.cano3_ca) * float(self.cacl2_cl)
        e = -(-a + b - c) / d
        return e * self.litres
    
    @float_exception
    def cacl2(self):
        a = float(self.cl)
        b = float(self.cacl2_cl)
        c = a / b
        return c * self.litres
    
    @float_exception
    def mgno3(self):
        if self.calc_mode == self.CalcMode.Mg:
            a = float(self.mg) * float(self.mgso4_s) - float(self.mgso4_mg) * float(self.s)
            b = float(self.mgno3_mg) * float(self.mgso4_s)
            c = a / b
            return c * self.litres
        return 0
    
    @float_exception
    def calc_s(self):
        m = MM
        a = float(self.nh4) * m.Ca * m.Mg * m.K * m.P * m.Cl
        b = 2 * float(self.ca) * m.N * m.Mg * m.K * m.P * m.Cl
        c = 2 * float(self.mg) * m.N * m.Ca * m.K * m.P * m.Cl
        d = float(self.k) * m.N * m.Ca * m.Mg * m.P * m.Cl
        e = float(self.no3) * m.Ca * m.Mg * m.K * m.P * m.Cl
        f = float(self.p) * m.N * m.Ca * m.Mg * m.K * m.Cl
        g = float(self.cl) * m.N * m.Ca * m.K * m.Mg * m.P
        h = 2 * m.N * m.Ca * m.Mg * m.K * m.P * m.Cl
        total = -m.S * (-a - b - c - d + e + f + g) / (h)
        return total


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
