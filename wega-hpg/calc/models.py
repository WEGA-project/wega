import math

from django.contrib.auth.models import User
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
    
    macro = ['n', 'no3', 'nh4', 'p', 'k', 'ca', 'mg', 's', 'cl', ]
    macro_matrix = ['n', 'p', 'k', 'ca', 'mg', 's', ]
    micro = ['fe', 'mn', 'b', 'zn', 'cu', 'mo', 'co', 'si', ]
    salt = ['cano3_ca', 'cano3_no3', 'cano3_nh4', 'kno3_k', 'kno3_no3', 'nh4no3_nh4', 'nh4no3_no3', 'mgso4_mg',
            'mgso4_s', 'kh2po4_k', 'kh2po4_p', 'k2so4_k', 'k2so4_s', 'mgno3_mg', 'mgno3_no3', 'cacl2_ca', 'cacl2_cl', ]
    
  
    salt_gramms = ['cano3', 'kno3', 'nh4no3', 'mgso4', 'kh2po4', 'k2so4', 'mgno3', 'cacl2', ]
    
    salt_dict = {
        'cano3': {'salt': ['cano3_ca', 'cano3_no3', 'cano3_nh4', ], 'name': 'Кальций азотнокислый',
                  'formula': 'Са(NО3)2*4H2O'},
        'kno3': {'salt': ['kno3_k', 'kno3_no3', ], 'name': 'Калий азотнокислый', 'formula': 'KNO3'},
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
    mn = models.FloatField(default=0, verbose_name='Mn')
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
    
    nh4_nh3_ratio = models.FloatField(default=0.1, verbose_name='NH4:NH3')

    def k_mg(self):
        return round(self.k / self.mg, 3)

    def k_ca(self):
        return round(self.k / self.ca, 3)
    
    def k_n(self):
        return round(self.k/self.n,3 )
    def get_npk(self):
        t = self.get_matrix()[0]


    @float_exception
    def calc_npk_formula(self):
        a = f"{math.ceil(self.n / self.n * 100 ) / 100} : " \
            f"{math.ceil(self.p / self.n * 100 ) / 100} : " \
            f"{math.ceil(self.k / self.n * 100 ) / 100} : " \
            f"{math.ceil(self.ca / self.n * 100 ) / 100} : " \
            f"{math.ceil(self.mg / self.n * 100 ) / 100} : " \
            f"{math.ceil(self.s / self.n * 100 ) / 100} : " \
            f"{math.ceil(self.cl / self.n * 100 ) / 100} sPPM={ self.calc_ppm()}"
        return a
    
    def get_npk_magazine(self):
        a = f"NPK: {math.ceil(self.n/10)}-{math.ceil(self.p / 0.436421 / 10)}-{math.ceil(self.k / 0.830148 / 10)} " \
            f"CaO={(math.ceil(self.ca / 0.714691 / 10) * 10 / 10)}% MgO={math.ceil(self.mg / 0.603036 / 10 * 10) / 10 }%" \
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
                    self.nh4 =  t
        
                elif not self.nh4 and self.no3:
                    t = self.no3 * m_delta
                    self.no3 = t
    
            setattr(self, b, new)
        
        if pushed_element=='ec':
            # сделал раунд до 3х знаков, чтобы соотвествовало старой версии
            # серу считает с учетом хлора - в старой бага
            r_n =(self.k_mg() *self.k_ca())/\
                 (self.k_ca()*self.k_n() + self.k_mg()*self.k_n() + self.k_mg()*self.k_ca() + self.k_mg()*self.k_ca()*self.k_n())
            r_k= (self.k_n() * self.k_mg() * self.k_ca()) / (
                        self.k_ca() * self.k_n() + self.k_mg() * self.k_n() + self.k_mg() * self.k_ca() + self.k_mg() * self.k_ca() * self.k_n())
            r_ca = (self.k_mg() * self.k_n()) / (
                        self.k_ca() * self.k_n() + self.k_mg() * self.k_n() + self.k_mg() * self.k_ca() + self.k_mg() * self.k_ca() * self.k_n())
            r_mg = (self.k_ca() * self.k_n()) / (
                        self.k_ca() * self.k_n() + self.k_mg() * self.k_n() + self.k_mg() * self.k_ca() + self.k_mg() * self.k_ca() * self.k_n())
            r_nh4 = (r_n * self.nh4_nh3_ratio ) / (1 + self.nh4_nh3_ratio )
            self.ec = float(val)

            r = (0.10526315789473684211 * m.N *m.Ca * m.Mg * m.K * (100 * self.ec - 19)) / \
                (
                   r_nh4  * m.Ca * m.Mg * m.K +
                   2 * r_ca  * m.N * m.Mg * m.K +
                   2 * r_mg * m.N  * m.Ca * m.K +
                   r_k * m.N * m.Ca * m.Mg)
            
            self.n = r_n * r
            self.k = r_k * r
            self.ca = r_ca * r
            self.mg = r_mg * r
            self.nh4 = r_nh4 * r
            self.no4 = self.n -self.nh4
            self.s = self.calc_s()
            
        if pushed_element in self.salt_gramms:
            self.no3 = (self.cano3() * self.cano3_no3+ self.nh4_nh3_ratio * self.nh4no3_no3  +
                        self.kno3()*self.kno3_no3 + self.mgno3()*self.mgno3_no3)/(0.1*self.litres)
            self.nh4 = 1

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
            self.nh4 = self.nh4_nh3_ratio* self.n/ (self.nh4_nh3_ratio+1)
            
            
        if pushed_element != 's':
            self.s = self.calc_s()
            
        if pushed_element != 'ca':
            self.ca = self.calc_ca()
        
        if pushed_element=='cano3_ca':
            self.cano3_no3 =  (2 * self.cano3_ca * m.N +  self.cano3_nh4  * m.Ca) / m.Ca

        if pushed_element == 'kno3_k':
            self.kno3_no3 = (self.kno3_k * m.N) / m.K
            
        if pushed_element=='kno3_no3':
            self.kno3_k = ( self.kno3_no3 * m.K ) / m.N

        if pushed_element == 'nh4no3_no3':
            self.nh4no3_nh4 = self.nh4no3_no3
        
        if pushed_element=='nh4no3_nh4':
            self.nh4no3_no3 = self.nh4no3_nh4

        if pushed_element == 'mgso4_mg':
            self.mgso4_s = (self.mgso4_mg * m.S) / m.Mg
            
        if pushed_element=='mgso4_s':
            self.mgso4_mg = (self.mgso4_s*m.Mg)/m.S

        if pushed_element == 'kh2po4_k':
            self.kh2po4_p = (self.kh2po4_k * m.P) / m.K
        
        if pushed_element=='kh2po4_p':
            self.kh2po4_k =  (self.kh2po4_p*m.K)/m.P

        if pushed_element == 'k2so4_k':
            self.k2so4_s = (self.k2so4_k * m.S) / (2 * m.K)
        
        if pushed_element=='k2so4_s':
            self.k2so4_k = (self.k2so4_s*2*m.K)/(m.S)

        if pushed_element == 'mgno3_mg':
            self.mgno3_no3 = (2 * self.mgno3_mg * m.N) / (m.Mg)

        if pushed_element == 'mgno3_no3':
            self.mgno3_mg = ((1 / 2) * (self.mgno3_no3 / m.N) * m.Mg)

        if pushed_element == 'cacl2_cl':
            self.cacl2_ca = (0.5 * (self.cacl2_cl / m.Cl)) * (m.Ca)

        if pushed_element == 'cacl2_ca':
            self.cacl2_cl = (2*self.cacl2_ca/m.Ca)*(m.Cl)
            
        
        if pushed_element == 'cano3_nh4':
            self.cano3_no3 = (2 * self.cano3_ca  * m.N + self.cano3_nh4 * m.Ca) / m.Ca
            self.cano3_ca  = -m.Ca * ( self.cano3_nh4 -self.cano3_no3 ) / (2*m.N)
    
        
        if pushed_element == 'cano3_no3':
            self.cano3_ca = -m.Ca * (self.cano3_nh4 - self.cano3_no3) / (2 * m.N)

        
    
            
            
            
        self.captions = self.calc_captions()
        
        
        for i in self.salt_gramms:
            a = getattr(self, i)()
            setattr(self, i,  a / 10)
        
        self.ec =  self.calc_ec()
        self.ppm = self.calc_ppm()
        self.npk = self.get_npk()
        self.npk_formula = self.calc_npk_formula()
        self.npk_magazine = self.get_npk_magazine()
        self.salt_grams = self.sum_salt_grams()
        
    
    def to_json(self):
        
        data = {'pk': self.pk,
                'ec': "{:.2f}".format(self.ec),
                'ppm': "{:.2f}".format(self.ppm),
                'npk': self.npk,
                'npk_formula':self.npk_formula,
                'npk_magazine':self.npk_magazine,
                'captions': self.captions,
                'salt_grams': "{:.2f}".self.salt_grams,
                }

        for s in self.captions:
            data[f"name-{ s }"] = self.captions[s]
            
        for s in self.macro:
            data[s] = "{:.2f}".format(getattr(self, s))
        
        for s in self.micro:
            data[s] = "{:.2f}".format(getattr(self, s) )
        
        for s, d in self.salt_dict.items():
            data[s] = "{:.2f}".format(getattr(self, s) )
            for i in d.get('salt'):
                data[i] = "{:.2f}".format(getattr(self, i) )
        
        matrix = self.get_matrix(as_dict=True)
        for k, i in matrix.items():
            data[f'matrix-{k}'] = "{:.2f}".format(i)
        
        return data
    
    
    def calc_ppm(self):
        ppm = round((self.n+ self.p + self.k + self.ca + self.mg + self.s + self.cl) * 100  ) / 100
        return ppm
    
    
    @float_exception
    def get_salt_dict(self):
        return self.salt_dict
    
    @float_exception
    def kh2po4(self):
        a = self.p / self.kh2po4_p
        return a * self.litres
    
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
            return f * self.litres
        else:
            a = self.k * self.kh2po4_p - self.p * self.kh2po4_k
            b = self.kno3_k * self.kh2po4_p
            return (a / b) * self.litres
        return 0
    
    @float_exception
    def cano3(self):
        a = self.ca * self.cacl2_cl - self.cl * self.cacl2_ca
        b = self.cano3_ca * self.cacl2_cl
        c = a / b
        return c * self.litres
    
    @float_exception
    def mgso4(self):
        if self.calc_mode == self.CalcMode.K:
            a = self.mg
            b = self.mgso4_mg
            c = a / b
            return c * self.litres
        else:
            a = self.s
            b = self.mgso4_s
            c = a / b
            return c * self.litres
        return 0
    
    @float_exception
    def k2so4(self):
        if self.calc_mode == self.CalcMode.K:
            a = self.s * self.mgso4_mg - self.mg * self.mgso4_s
            b = self.k2so4_s * self.mgso4_mg
            c = a / b
            return c * self.litres
        return 0
    
    @float_exception
    def nh4no3(self):
        a = self.nh4 * self.cano3_ca * self.cacl2_cl
        b = self.cano3_nh4 * self.ca * self.cacl2_cl
        c = self.cano3_nh4 * self.cl * self.cacl2_ca
        d = self.nh4no3_nh4 * self.cano3_ca * self.cacl2_cl
        e = -(-a + b - c) / d
        return e * self.litres
    
    @float_exception
    def cacl2(self):
        a = self.cl
        b = self.cacl2_cl
        c = a / b
        return c * self.litres
    
    @float_exception
    def mgno3(self):
        if self.calc_mode == self.CalcMode.Mg:
            a = self.mg * self.mgso4_s - self.mgso4_mg * self.s
            b = self.mgno3_mg * self.mgso4_s
            c = a / b
            return c * self.litres
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
        g = self.cl * m.N * m.Ca  * m.Mg * m.K * m.P
        h = 2 * m.N * m.Ca * m.Mg * m.K * m.P * m.Cl
        total = -m.S * (-a - b - c - d + e + f + g) / (h)
        return total
    
 
        
    def calc_captions(self):
        captions = {}

        captions['cano3'] = f'Селитра кальциевая CaO-{round((self.cano3_ca / 0.714691) * 10) / 10}%' \
                            f'N-{round((self.cano3_nh4 + self.cano3_no3 ) * 10) / 10}'
        if self.cano3_nh4==0:
            if math.ceil(self.cano3_ca * 10) / 10 == 17:
                captions['cano3'] = 'Кальций азотнокислый Са(NО3)2*4H2O'
            if math.ceil(self.cano3_ca * 10) / 10 == 20:
                captions['cano3'] = 'Кальций азотнокислый Са(NО3)2*2H2O'
            if math.ceil(self.cano3_ca * 10) / 10 == 20:
                captions['cano3'] = 'Кальций азотнокислый Ca(NO3)2'
        
        captions['kno3'] = f'Селитра калиевая K2O-{(math.ceil((self.kno3_k / 0.830148) * 10) / 10)} %  N-{math.ceil((self.kno3_no3) * 10) / 10}%'
        if round(self.kno3_k*10)/10 == 38.7:
            captions['kno3'] = 'Калий азотнокислый KNO3'

        captions['nh4no3'] = f'Селитра аммиачная N- {(math.ceil((self.nh4no3_nh4+self.nh4no3_no3)*10)/10)}%'
        if round(self.nh4no3_no3*10)/10 == 17.5:
            captions['nh4no3'] = f'Аммоний азотнокислый NH4NO3'
        
        captions['mgso4'] = f'Сульфат магния MgO-{(math.ceil((self.mgso4_mg/0.603036)*10)/10)}% SO3-{(math.ceil((self.mgso4_s/0.400496)*10)/10)}%';

        if  math.ceil(self.mgso4_mg * 10) / 10 == 9.9:
            captions['mgso4'] = f'Магний сернокислый MgSO4*7H2O'
    
        if math.ceil(self.mgso4_mg * 10) / 10 == 20.2:
            captions['mgso4'] = f'Магний сернокислый MgSO4'
        
        captions['kh2po4'] =  f'Монофосфат калия K2O-{(math.ceil((self.kh2po4_k / 0.830148) * 10) / 10)}% P2O5-{(math.ceil((self.kh2po4_p / 0.436421) * 10) / 10)}%';
        if math.ceil(self.kh2po4_k*10)/10:
            captions['kh2po4'] = 'Калий фосфорнокислый KH2PO4'

        captions['k2so4'] =f'Сульфат калия K2O-{(math.ceil((self.k2so4_k / 0.830148) * 10) / 10)}% SO3-{(math.ceil((self.k2so4_s / 0.400496) * 10) / 10)}%'
        if math.ceil(self.k2so4_k*10)/10 == 44.9:
            captions['k2so4'] = 'Калий сернокислый K2SO4'
            
        
        
        captions['mgno3'] = f'Селитра магниевая MgO-{math.ceil((self.mgno3_mg / 0.603036) * 10) / 10}% N-{math.ceil((self.mgno3_no3)*10)/10}%'
        if math.ceil(self.mgno3_mg*10)/10==9.5:
            captions['mgno3']='Магний азотнокислый Mg(NO3)2*6H2O'
        if math.ceil(self.mgno3_mg * 10) / 10 == 16.4:
            captions['mgno3']= 'Магний азотнокислый Mg(NO3)2'

  
        captions['cacl2'] =f'Кальций хлористый CaO-{math.ceil((self.cacl2_ca/0.714691)*10)/10}% Cl-{math.ceil((self.cacl2_cl)*10)/10}%'
        if math.ceil(self.cacl2_ca*10)/10 == 18.3:
             captions['cacl2'] = 'Хлорид кальция 6-водный CaCl2*6H2O'
        if math.ceil(self.cacl2_ca * 10) / 10 == 36.1:
            captions['cacl2'] = 'Хлорид кальция безводный CaCl2'

        if self.nh4 > 0:
            captions['nh4_nh3_ratio'] = f'NH4:NO3 1:{math.ceil((self.no3 / self.nh4))}'
        else:
            captions['nh4_nh3_ratio'] = f'NO3=100%'
            
        return captions
    
    def sum_salt_grams(self):
        s=0
        for i in self.salt_gramms:
            i = getattr(self,i)()
            s+=i
        return s/10
        
 


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
