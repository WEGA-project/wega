from django.shortcuts import render

from project.utils import DataMixin
from wiki.models import Wiki


def wiki_pages(request):
    context = DataMixin.get_user_context(title="Загрузить с файла профиль", btn_name="Загрузить")
    q = Wiki.objects.all()
    context['pages'] = q
    return render(request, 'wiki/index.html', context=context)


def wiki_page(request, slug):
    context = DataMixin.get_user_context(title="Загрузить с файла профиль", btn_name="Загрузить")
    q = Wiki.objects.get(slug = slug)
    context['page'] = q
    return render(request, 'wiki/page.html', context=context)