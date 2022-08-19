from .settings import *
DEBUG=False
pwd = os.system("""$(echo "<?php include '/var/WEGA/db.php'; echo \$password;" | /usr/bin/php)""")
SECRET_KEY = '&9+%$$-s6g4@3y1%00x-4bg&i6=e(gupn27f0$e@*p&_y#n*u'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'wegacalc',
        'USER': 'root',
        'PASSWORD': pwd,
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
