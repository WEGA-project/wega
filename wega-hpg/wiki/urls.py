import os

from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from wiki.views import wiki_page, wiki_pages

urlpatterns = [
    path('<str:slug>/', wiki_page, name='wiki_page'),
    path('',  wiki_pages, name='wiki_pages'),

]


