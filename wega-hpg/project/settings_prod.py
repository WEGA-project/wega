from .settings import *
DEBUG=False
def get_pwd(fn='/var/WEGA/db.php'):
    with open(fn, 'r') as f:
        lines = f.readlines()
        for i  in lines:
            try:
                k, v = i.split('=')
                if k=='$password':
                    return v[1:-3]
            except Exception as e:
                pass
                

SECRET_KEY = '&9+%$$-s6g4@3y1%00x-4bg&i6=e(gupn27f0$e@*p&_y#n*u'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'wegacalc',
        'USER': 'root',
        'PASSWORD': get_pwd(),
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}

