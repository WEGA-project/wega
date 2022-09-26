from django.core.cache import cache
from django.db.models import Sum
from django.shortcuts import render
from django.utils import timezone

from project.utils import DataMixin
from wiki.models import Wiki, WikiStatistic


def wiki_pages(request):
    context = DataMixin.get_user_context(title="Загрузить с файла профиль", btn_name="Загрузить")
    q = Wiki.objects.all()
    context['pages'] = q
    return render(request, 'wiki/index.html', context=context)


def wiki_page(request, slug):
    context = DataMixin.get_user_context(title="Загрузить с файла профиль", btn_name="Загрузить")
    q = Wiki.objects.get(slug = slug)
    context['page'] = q

  
    try:
        # Далее забираем объект сегодняшней статистики или создаём новый, если требуется
        obj, created = WikiStatistic.objects.get_or_create(defaults={"page": q, "date": timezone.now()},
                                                           date=timezone.now(), page=q)
    except WikiStatistic.MultipleObjectsReturned as e:
        a = WikiStatistic.objects.filter(page=q, date=timezone.now())
        a.first().delete()
        obj, created = WikiStatistic.objects.get_or_create(defaults={"page": q, "date": timezone.now()},
                                                           date=timezone.now(), page=q)

    obj.views += 1  # инкрементируем счётчик просмотров и обновляем поле в базе данных
    obj.save(update_fields=['views'], )
    context['views'] = obj.views
    
    return render(request, 'wiki/page.html', context=context)