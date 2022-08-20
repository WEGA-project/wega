from decimal import Decimal

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

from calc.decorators import decimal_exception


class MM:
    mN  = Decimal(14.0067)
    mP  = Decimal(30.973762)
    mK  = Decimal(39.0983)
    mCa = Decimal(40.078)
    mMg = Decimal(24.305)
    mS  = Decimal(32.065)
    mCl = Decimal(35.453)


# Create your models here.
class PlantProfile(models.Model):
    class CalcMode(models.TextChoices):
        K = 'K', _('K2SO4')
        Mg = 'Mg', _('MgNO3')
    
    macro = ['n', 'no3', 'nh4', 'p', 'k', 'ca', 'mg', 's', 'cl', ]
    macro_matrix = ['n', 'p', 'k', 'ca', 'mg', 's', ]
    micro = ['fe', 'mn', 'b', 'zn', 'cu', 'mo', 'co', 'si', ]
    salt = ['cano3_ca', 'cano3_no3', 'cano3_nh4', 'kno3_k', 'kno3_no3', 'nh4no3_nh4', 'nh4no3_no3', 'mgso4_mg',
            'mgso4_s', 'kh2po4_k', 'kh2po4_p', 'k2so4_k', 'k2so4_s', 'mgno3_mg', 'mgno3_no3', 'cacl2_ca', 'cacl2_cl', ]
    
    salt_gramms=['cano3','kno3','nh4no3','mgso4','kh2po4','k2so4','mgno3','cacl2',]
    
    salt_dict = {
        'cano3': {'salt': ['cano3_ca', 'cano3_no3', 'cano3_nh4', ], 'name': 'Кальций азотнокислый', 'formula': 'CaNO3'},
        'kno3': {'salt': ['kno3_k', 'kno3_no3', ], 'name': 'Селитра калиевая', 'formula': 'KNO3'},
        'nh4no3': {'salt': ['nh4no3_nh4', 'nh4no3_no3', ], 'name': 'Селитра аммиачная', 'formula': 'NH4NO3'},
        'mgso4': {'salt': ['mgso4_mg', 'mgso4_s', ], 'name': 'Сульфат магния', 'formula': 'MgSO4'},
        'kh2po4': {'salt': ['kh2po4_k', 'kh2po4_p', ], 'name': 'Монофосфат калия', 'formula': 'KPO4'},
        'k2so4': {'salt': ['k2so4_k', 'k2so4_s', ], 'name': 'Сульфат калия', 'formula': 'KSO4'},
        'mgno3': {'salt': ['mgno3_mg', 'mgno3_no3', ], 'name': 'Селитра магниевая', 'formula': 'MgNO3'},
        'cacl2': {'salt': ['cacl2_ca', 'cacl2_cl', ], 'name': 'Хлорид кальция 6водный', 'formula': 'CaCl2'},
    }
    
    name = models.CharField(max_length=1024, verbose_name='Имя профиля')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ec = models.DecimalField(max_digits=9, decimal_places=3, verbose_name='Ec')
    ppm = models.DecimalField(max_digits=9, decimal_places=3, verbose_name='PPM')
    
    calc_mode = models.CharField(max_length=2, choices=CalcMode.choices, default=CalcMode.K, )
    
    n = models.DecimalField(max_digits=9,   default=0, decimal_places=3,   verbose_name='N')
    no3 = models.DecimalField(max_digits=9, default=0, decimal_places=3, verbose_name='NO3')
    nh4 = models.DecimalField(max_digits=9, default=0, decimal_places=3, verbose_name='NH4')
    
    p = models.DecimalField(max_digits=9, default=0, decimal_places=3, verbose_name='P')
    k = models.DecimalField(max_digits=9, default=0, decimal_places=3, verbose_name='K')
    ca = models.DecimalField(max_digits=9, default=0, decimal_places=3, verbose_name='Ca')
    mg = models.DecimalField(max_digits=9, default=0, decimal_places=3, verbose_name='Mg')
    s = models.DecimalField(max_digits=9, default=0, decimal_places=3, verbose_name='S')
    cl = models.DecimalField(max_digits=9, default=0, decimal_places=3, verbose_name='Cl')
    
    fe = models.DecimalField(max_digits=9, default=0, decimal_places=3, verbose_name='Fe')
    mn = models.DecimalField(max_digits=9, default=0, decimal_places=3, verbose_name='Mn')
    b = models.DecimalField(max_digits=9, default=0, decimal_places=3, verbose_name='B')
    zn = models.DecimalField(max_digits=9, default=0, decimal_places=3, verbose_name='Zn')
    cu = models.DecimalField(max_digits=9, default=0, decimal_places=3, verbose_name='Cu')
    mo = models.DecimalField(max_digits=9, default=0, decimal_places=3, verbose_name='Mo')
    co = models.DecimalField(max_digits=9, default=0, decimal_places=3, verbose_name='Co')
    si = models.DecimalField(max_digits=9, default=0, decimal_places=3, verbose_name='Si')
    
    cano3_ca = models.DecimalField(max_digits=9, default=0, decimal_places=3, verbose_name='CaNO3_Ca')
    cano3_no3 = models.DecimalField(max_digits=9, default=0, decimal_places=3, verbose_name='CaNO3_NO3')
    cano3_nh4 = models.DecimalField(max_digits=9, default=0, decimal_places=3, verbose_name='CaNO3_NH4')
    
    kno3_k = models.DecimalField(max_digits=9, default=0, decimal_places=3, verbose_name='KNO3_K')
    kno3_no3 = models.DecimalField(max_digits=9, default=0, decimal_places=3, verbose_name='KNO3_NO3')
    nh4no3_nh4 = models.DecimalField(max_digits=9, default=0, decimal_places=3, verbose_name='NH4NO3_NH4')
    nh4no3_no3 = models.DecimalField(max_digits=9, default=0, decimal_places=3, verbose_name='NH4NO3_NO3')
    mgso4_mg = models.DecimalField(max_digits=9, default=0, decimal_places=3, verbose_name='MgSO4_Mg')
    mgso4_s = models.DecimalField(max_digits=9, default=0, decimal_places=3, verbose_name='MgSO4_S')
    kh2po4_k = models.DecimalField(max_digits=9, default=0, decimal_places=3, verbose_name='KH2PO4_K')
    kh2po4_p = models.DecimalField(max_digits=9, default=0, decimal_places=3, verbose_name='KH2PO4_P')
    k2so4_k = models.DecimalField(max_digits=9, default=0, decimal_places=3, verbose_name='K2SO4_K')
    k2so4_s = models.DecimalField(max_digits=9, default=0, decimal_places=3, verbose_name='K2SO4_S')
    mgno3_mg = models.DecimalField(max_digits=9, default=0, decimal_places=3, verbose_name='MgNO3_Mg')
    mgno3_no3 = models.DecimalField(max_digits=9, default=0, decimal_places=3, verbose_name='MgNO3_NO3')
    cacl2_ca = models.DecimalField(max_digits=9, default=0, decimal_places=3, verbose_name='CaCl2_Ca')
    cacl2_cl = models.DecimalField(max_digits=9, default=0, decimal_places=3, verbose_name='CaCl2_Cl')

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
            cur_cal = getattr(pp, cur_element.lower()) or Decimal(0)
            for i in self.macro_matrix:
                val = getattr(pp, i.lower()) or Decimal(0)
                if cur_cal == 0:
                    row[i] = None
                    matrix_dict[f"{i}-{cur_element}"] = None
                else:
                    t = round(Decimal(val) / Decimal(cur_cal), 3)
                    row[i] = t
                    matrix_dict[f"{i}-{cur_element}"] = t
        
            del element_row[0]
            element_row.append(cur_element)
            matrix.append(row)
            ii += 1
        if as_dict:
            return matrix_dict
        return matrix


    def recalc(self ):
        self.s = "{:.3f}".format(self.calc_s())
        self.n = "{:.3f}".format(Decimal(self.no3) + Decimal(self.nh4))
        
        for i in self.salt_gramms:
            a = getattr(self, i)()
            setattr(self, i, "{:.3f}".format(a/10))
        
    def to_json(self):
        data = {'pk':self.pk, 'ec':self.ec, 'ppm':self.ppm}
        for s in self.macro:
            # data[s] = "{:.3f}".format(getattr(self, s))
            data[s] = getattr(self, s)
        
        for s in self.micro:
            # data[s]= "{:.3f}".format(getattr(self, s))
            data[s] = getattr(self, s)
            
        for s, d in self.salt_dict.items():
            # data[s] = "{:.3f}".format(getattr(self, s))
            data[s] = getattr(self, s)
            for i in d.get('salt'):
                data[i] = getattr(self, i)
                # data[i] = "{:.3f}".format(getattr(self, i))
        
        matrix = self.get_matrix(as_dict=True)
        for k, i in matrix.items():
            data[f'matrix-{k}'] = i
            
            
        return data
    
    @decimal_exception
    def get_salt_dict(self):
        if self.calc_mode == self.CalcMode.K:
            if 'mgno3' in self.salt_dict:
                del self.salt_dict['mgno3']
    
        if self.calc_mode == self.CalcMode.Mg:
            if 'k2so4' in self.salt_dict:
                del self.salt_dict['k2so4']
    
        return self.salt_dict

    @decimal_exception
    def kh2po4(self):
        a = Decimal(self.p) / Decimal(self.kh2po4_p)
        return a

    @decimal_exception
    def kno3(self):
        if self.calc_mode == self.CalcMode.K:
            a = Decimal(self.k) * Decimal(self.kh2po4_p) * Decimal(self.k2so4_s) * Decimal(self.mgso4_mg)
            b = Decimal(self.p) * Decimal(self.kh2po4_k) * Decimal(self.k2so4_s) * Decimal(self.mgso4_mg)
            c = Decimal(self.k2so4_k) * Decimal(self.kh2po4_p) * Decimal(self.s) * Decimal(self.mgso4_mg)
            d = Decimal(self.k2so4_k) * Decimal(self.kh2po4_p) * Decimal(self.mg) * Decimal(self.mgso4_s)
            e = Decimal(self.kno3_k) * Decimal(self.kh2po4_p) * Decimal(self.k2so4_s) * Decimal(self.mgso4_mg)
            f = -(-a + b + c - d) / e
            return f
        else:
            a = Decimal(self.k) * Decimal(self.kh2po4_p) - Decimal(self.p) * Decimal(self.kh2po4_k)
            b = Decimal(self.kno3_k) * Decimal(self.kh2po4_p)
            return a / b
        return 0

    @decimal_exception
    def cano3(self):
        a = Decimal(self.ca) * Decimal(self.cacl2_cl) - Decimal(self.cl) * Decimal(self.cacl2_ca)
        b = Decimal(self.cano3_ca) * Decimal(self.cacl2_cl)
        c = a / b
        return c
    
    def mgso4(self):
        if self.calc_mode == self.CalcMode.K:
            a = Decimal(self.mg)
            b = Decimal(self.mgso4_mg)
            c = a / b
            return c
        else:
            a = Decimal(self.s)
            b = Decimal(self.mgso4_s)
            c = a / b
            return c
        return 0

    @decimal_exception
    def k2so4(self):
        if self.calc_mode == self.CalcMode.K:
            a = Decimal(self.s) * Decimal(self.mgso4_mg) - Decimal(self.mg) * Decimal(self.mgso4_s)
            b = Decimal(self.k2so4_s) * Decimal(self.mgso4_mg)
            c = a / b
            return c
        return 0

    @decimal_exception
    def nh4no3(self):
        a = Decimal(self.nh4) * Decimal(self.cano3_ca) * Decimal(self.cacl2_cl)
        b = Decimal(self.cano3_nh4) * Decimal(self.ca) * Decimal(self.cacl2_cl)
        c = Decimal(self.cano3_nh4) * Decimal(self.ca) * Decimal(self.cacl2_ca)
        d = Decimal(self.nh4no3_nh4) * Decimal(self.cano3_ca) * Decimal(self.cacl2_cl)
        e = -(-a + b - c) / d
        return e

    @decimal_exception
    def cacl2(self):
        a = Decimal(self.cl)
        b = Decimal(self.cacl2_cl)
        c = a / b
        return c

    @decimal_exception
    def mgno3(self):
        if self.calc_mode == self.CalcMode.Mg:
            a = Decimal(self.mg) * Decimal(self.mgso4_s) - Decimal(self.mgso4_mg) * Decimal(self.s)
            b = Decimal(self.mgno3_mg) * Decimal(self.mgso4_s)
            c = a / b
            return c
        return 0

    @decimal_exception
    def calc_s(self):
        m=MM
        a = Decimal(self.nh4) * m.mCa * m.mMg * m.mK * m.mP * m.mCl
        b = 2 * Decimal(self.ca) * m.mN * m.mMg * m.mK * m.mP * m.mCl
        c = 2 * Decimal(self.mg) * m.mN * m.mCa * m.mK * m.mP * m.mCl
        d = Decimal(self.k) * m.mN * m.mCa * m.mMg * m.mP * m.mCl
        e = Decimal(self.no3) * m.mCa * m.mMg* m.mK * m.mP * m.mCl
        f = Decimal(self.p) * m.mN * m.mCa * m.mMg * m.mK * m.mCl
        g = Decimal(self.cl) * m.mN * m.mCa * m.mK * m.mMg * m.mP
        h = 2 * m.mN * m.mCa * m.mMg * m.mK * m.mP * m.mCl
        total = -m.mS * (-a - b - c - d + e + f + g) /  (h)
        return total


class Price(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=1024)
