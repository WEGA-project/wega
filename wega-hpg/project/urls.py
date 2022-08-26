import os

from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/',include('wega_auth.urls')),
    path('calc/', include('calc.urls')),
    path('', include('home.urls')),
]




if settings.DEBUG or True:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns() # tell gunicorn where static files are in dev mode
    urlpatterns += static(settings.MEDIA_URL + 'images/', document_root=os.path.join(settings.MEDIA_ROOT, 'images'))
    urlpatterns += static(settings.MEDIA_URL, document_root=os.path.join(settings.MEDIA_ROOT))