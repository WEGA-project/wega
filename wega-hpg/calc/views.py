import json
import logging
from decimal import Decimal

import django_tables2
from django.contrib.auth.decorators import login_required

from django.db.models import F
from django.shortcuts import redirect, render, HttpResponse
from django.http import JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django_tables2 import RequestConfig
from calc.forms import DelForm, FilterForm, PlantProfileAddForm, PlantProfileEditForm, \
    PlantProfileUploadForm
from calc.models import PlantProfile, PlantProfileHistory
from calc.tables import HistoryColumn, ModalBtn, PlatProfileMatrixTable, PlatProfileTable
from project.utils import DataMixin
import simplejson


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


@login_required
def plant_profiles(request):
    context = DataMixin.get_user_context(title="Профили питания", btn_name="Добавить")
    context['form'] = PlantProfileAddForm
    context['upload_form'] = PlantProfileUploadForm
    context['filter'] = FilterForm(request.GET)
    extra_columns = []
    extra_columns.append(('name', django_tables2.Column()))
    columns = ['name']
    filter_form = context['filter']
    if request.GET.get('filter') and filter_form.is_valid():
        request.session['show_macro'] = not filter_form.cleaned_data.get('hide_macro')
        request.session['show_micro'] = not filter_form.cleaned_data.get('hide_micro')
        request.session['show_salt'] = not filter_form.cleaned_data.get('hide_salt')
        request.session['show_gramms'] = not filter_form.cleaned_data.get('show_gramms')

        
    
    if request.session.get('show_macro'):
        columns += PlantProfile.macro
        for item in PlantProfile.macro:
            extra_columns.append((item, django_tables2.Column()))
    else:
        filter_form.fields['hide_macro'].widget.attrs['checked'] = ''
    
    if request.session.get('show_micro'):
        columns += PlantProfile.micro
        for item in PlantProfile.micro:
            extra_columns.append((item, django_tables2.Column()))
    else:
        filter_form.fields['hide_micro'].widget.attrs['checked'] = ''
    
    if request.session.get('show_salt'):
        columns += PlantProfile.salt
        for item in PlantProfile.salt:
            extra_columns.append((item, django_tables2.Column()))
    else:
        filter_form.fields['hide_salt'].widget.attrs['checked'] = ''

    if request.session.get('show_gramms'):
        columns += PlantProfile.salt_gramms
        for item in PlantProfile.salt_gramms:
            extra_columns.append((item,  django_tables2.Column()))

    else:
        filter_form.fields['show_gramms'].widget.attrs['checked'] = ''
        
    extra_columns.append(('action', ModalBtn(verbose_name='', )))
    data = []
    query = PlantProfile.objects.filter(user=request.user, template=None)
    for pp in query:
        cols = {}
        cols['action'] = pp.pk
        pp.recalc()
        for col in columns:
            
            cols[col] = getattr(pp, col)
        data.append(cols)
        
    my_table = PlatProfileTable(data, extra_columns=extra_columns)
    RequestConfig(request, paginate={'per_page': 10}).configure(my_table)
    context['table'] = my_table
    return render(request, 'calc/index.html', context=context)


from django.forms.models import model_to_dict


@login_required
def plant_profile_history(request, pk):
    context = DataMixin.get_user_context(title="История изменений профиля питания", btn_name="Вернуть")
    context['form'] = None
    context['upload_form'] = None
    context['filter'] = FilterForm(request.GET)
    extra_columns = []
    history_column = HistoryColumn()
    extra_columns.append(('pk', django_tables2.Column()))
    extra_columns.append(('date', django_tables2.Column()))
    extra_columns.append(('name', history_column))

    
    columns = ['pk,''name',]
    
    filter_form = context['filter']
    if request.GET.get('filter') and filter_form.is_valid():
        request.session['show_macro'] = not filter_form.cleaned_data.get('hide_macro')
        request.session['show_micro'] = not filter_form.cleaned_data.get('hide_micro')
        request.session['show_salt'] = not filter_form.cleaned_data.get('hide_salt')
        request.session['show_gramms'] = not filter_form.cleaned_data.get('show_gramms')
    
    if request.session.get('show_macro'):
        columns += PlantProfile.macro
        for item in PlantProfile.macro:
            extra_columns.append((item, history_column))
    
    else:
        filter_form.fields['hide_macro'].widget.attrs['checked'] = ''
    
    if request.session.get('show_micro'):
        columns += PlantProfile.micro
        for item in PlantProfile.micro:
            extra_columns.append((item, history_column))
    else:
        filter_form.fields['hide_micro'].widget.attrs['checked'] = ''
    
    if request.session.get('show_salt'):
        columns += PlantProfile.salt
        for item in PlantProfile.salt:
            extra_columns.append((item, history_column))
    else:
        filter_form.fields['hide_salt'].widget.attrs['checked'] = ''
    
    if request.session.get('show_gramms'):
        columns += PlantProfile.salt_gramms
        for item in PlantProfile.salt_gramms:
            extra_columns.append((item, history_column))
    
    else:
        filter_form.fields['show_gramms'].widget.attrs['checked'] = ''
 
    extra_columns.append(('action', ModalBtn(verbose_name='', )))
    history_data = PlantProfileHistory.objects.filter(profile_id=pk)
    data = []
   
    for history in history_data:
        p = simplejson.loads(history.profile_data)
        p['user_id'] = p['user']
        del p['user']
        pp = PlantProfile(**p)
        changes = simplejson.loads(history.changed_data)
        
        for salt_gramm_name in PlantProfile.salt_gramms:
            p[salt_gramm_name] = "{:.3f}".format(getattr(pp, salt_gramm_name)())
        
        vals = {}
        
        for col in PlantProfile.macro + PlantProfile.micro + PlantProfile.salt + PlantProfile.salt_gramms:
            mark_danger = col in changes
            vals[col] = {'mark-danger': mark_danger, 'val': p.get(col)}
        for col in extra_columns:
            mark_danger = col[0] in changes
            vals[col[0]] = {'mark-danger': mark_danger, 'val': p.get(col[0])}
        
        vals['action'] = p.get('id')
        vals['pk'] = p.get('id')
        vals['date'] = history.date

        
        
        data.append(vals)
    my_table = PlatProfileTable(data, extra_columns=extra_columns)
    RequestConfig(request, paginate={'per_page': 10}).configure(my_table)
    context['table'] = my_table
    return render(request, 'calc/index.html', context=context)


@login_required
def upload_plant_profile(request):
    context = DataMixin.get_user_context(title="Загрузить с файла профиль", btn_name="Загрузить")
    form = PlantProfileUploadForm(request.POST, files=request.FILES)
    if form.is_valid():
        files = request.FILES.getlist('file')
        for f in files:
            data = f.read().decode('utf-8')
            create_kw = {'name': str(f)}
            
            for item in data.splitlines():
                key, value = item.split('=')
                
                if key.lower() in PlantProfile.micro or key.lower() in PlantProfile.macro or key.lower() in PlantProfile.salt:
                    create_kw[key.lower()] = "{:.3f}".format(float(value))
            
            try:
                pp = PlantProfile(**create_kw)
                pp.ec = 0
                pp.ppm = 0
                pp.user = request.user
                pp.save()
            except Exception as e:
                logging.exception(e)
                return HttpResponse(str(e))
        
        return redirect('profile_index')
    else:
        return render(request, 'calc/index.html', context=context)


@login_required
def create_plant_profile(request):
    context = DataMixin.get_user_context(title="Новый профиль", btn_name="Добавить")
    form = PlantProfileAddForm(request.POST)
    if form.is_valid():
        new = PlantProfile.objects.get(template=form.cleaned_data['template'])
        new.pk = None
        new.name = form.cleaned_data['name']
        new.from_template = form.cleaned_data['template']
        new.user = request.user
        new.template = None
        new.save()
        return redirect('profile_index')
    else:
        return render(request, 'calc/index.html', context=context)


@login_required
@csrf_exempt
def plant_profile_precalc(request, pk):
    calc_mode = 'salt'
    try:
        pp = PlantProfile.objects.get(pk=pk, user=request.user)
        if is_ajax(request):
            if request.method == 'POST':
                data = json.loads(request.body)
                pushed_element = data.get('pushed_element')
                
                for param_list in [['ppm', 'ec', ], PlantProfile.macro, PlantProfile.micro, PlantProfile.salt]:
                    for i in param_list:
                        t = data.get(i, None)
                        if t:
                            setattr(pp, i, t)
                if pushed_element:
                    if 'matrix' in pushed_element:
                        t, a, b, = pushed_element.split('-')
                        val = data.get(pushed_element)
                        
                        old = Decimal(getattr(pp, b))
                        new = Decimal(getattr(pp, a)) / Decimal(val)
                        
                        if b == 'n':
                            m_delta = Decimal(new / old)
                            if pp.nh4 and pp.no3:
                                
                                pp.nh4 = Decimal(pp.nh4) * m_delta
                                pp.no3 = Decimal(pp.no3) * m_delta
                            
                            elif pp.nh4 and not pp.no3:
                                pp.nh4 = Decimal(pp.nh4) * Decimal(m_delta)
                            
                            elif not pp.nh4 and pp.no3:
                                pp.no3 = Decimal(pp.no3) * Decimal(m_delta)
                        
                        setattr(pp, b, "{:.3f}".format(new))
                
                data = {}
                pp.recalc()
                data['pp'] = pp.to_json()
    
    
    
    
    except PlantProfile.DoesNotExist:
        raise Http404
    
    # print(data)
    return JsonResponse(data)


@login_required
def edit_plant_profile(request, pk):
    context = DataMixin.get_user_context(title="Редактируем профиль", btn_name="Сохранить")
    instance = PlantProfile.objects.get(user=request.user, pk=pk)
    old_instance = PlantProfile.objects.get(user=request.user, pk=pk)
    form = PlantProfileEditForm(instance=instance)
    context['form'] = form
    context['instance'] = instance
    if request.method == 'POST':
        form = PlantProfileEditForm(instance=instance, data=request.POST)
        if form.is_valid():
            new = form.save(commit=False)
            new.user = request.user
            new.ec = 0
            new.ppm = 0
            
            changes = form.changed_data
            for item in PlantProfile.salt_gramms:
                
                if getattr(new, item)() != getattr(old_instance, item)():
                    print(
                        f'item {item} getattr(new,item)() {getattr(new, item)()} getattr(instance,item)() {getattr(old_instance, item)()}')
                    changes.append(item)
            
            new.save()
            ph = PlantProfileHistory(profile=new,
                                     # profile_data=simplejson.dumps(model_to_dict(new)),
                                     # changed_data=simplejson.dumps(form.cleaned_data)
                                     profile_data=simplejson.dumps(model_to_dict(new)),
                                     changed_data=simplejson.dumps(changes)
                                     )
            ph.save()
        else:
            context['form'] = form
        
        return redirect('profile_index')
    
    return render(request, 'calc/edit.html', context=context)


@login_required
def plant_profile_del(request, pk):
    context = DataMixin.get_user_context(title="Удаляем профиль", btn_name="Подтвердить")
    object = PlantProfile.objects.get(user=request.user, pk=pk)
    form = DelForm()
    context['instance'] = object
    if request.method == 'POST':
        form = DelForm(data=request.POST)
        if form.is_valid():
            object.delete()
            return redirect('profile_index')
    context['form'] = form
    return render(request, 'calc/del.html', context=context)


@login_required
def settings(request):
    context = DataMixin.get_user_context(title="Настройки", btn_name="Сохранить")
    context['form'] = PlantProfileAddForm
    
    return render(request, 'calc/index.html', context=context)
