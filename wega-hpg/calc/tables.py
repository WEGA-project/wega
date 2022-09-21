import decimal

from django.template.loader import render_to_string
from django.utils.html import format_html
import django_tables2 as tables
from django.utils.safestring import mark_safe
from django_tables2 import TemplateColumn

from calc.models import PlantProfile
from wagtail.images.models import Image, Rendition
class ModalBtn(tables.Column):
    def render(self, value):
        t = render_to_string('calc/modal_button.html', {'pk':value} )

        return format_html( t )


class PlatProfileTable(tables.Table):
    class Meta:
        model = PlantProfile
        template_name = 'django_tables2/bootstrap4.html'
        fields = []

class PlatProfileMatrixTable(tables.Table):
    class Meta:
        model = PlantProfile
        template_name = 'django_tables2/bootstrap-responcive.html'
        fields = []
    
import datetime


class CalcColumn(tables.Column):
    def render(self, value, record):
        if isinstance(value, str):
            return mark_safe(value)
        
        if isinstance(value, datetime.datetime):
            return value.strftime("%d.%m.%Y %H:%M:%S")
        
        if isinstance(value, float):
            return "{:.1f}".format(value)
        
        return value


class PColumn(tables.Column):
    def render(self, value, record):
     
        return mark_safe(value())
        
   
        
  
        
     





class ImageColumn(tables.Column):
    def render(self, value, record):
        t = ''
        # record
        # Image, Rendition
        val = '-'
        if value:
            val = render_to_string('project/carousel.html', context={'images':value})
        # for i in value:
        #     thumb_url = i.get_rendition('fill-100x100|jpegquality-60').url
        #     t += f'<a class="fancybox" ' \
        #          f'href="/media/{i}">' \
        #          f'<img src="/media/{thumb_url}" style="height:100px;width:100px;" class="img-thumbnail"></a>'
        return mark_safe(val)
    
class HistoryColumn(tables.Column):
    def render(self, value, record):
        if isinstance(value, str):
            return mark_safe(value)
        
        if isinstance(value, datetime.datetime):
            return value.strftime("%d.%m.%Y")
        
        if value['mark-danger']:
            return mark_safe(f'<span class="text-danger">{value["val"]}</span>')
        else:
            return mark_safe(f'<span class="text">{value["val"]}</span>')
        return value

 