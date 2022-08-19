from django.template.loader import render_to_string
from django.utils.html import format_html
import django_tables2 as tables

from calc.models import PlantProfile

class ModalBtn(tables.Column):
    def render(self, value):
        t = render_to_string('calc/modal_button.html', {'pk':value} )

        return format_html( t )


class PlatProfileTable(tables.Table):
    class Meta:
        model = PlantProfile
        template_name = 'django_tables2/bootstrap.html'
        fields = ['name']

class PlatProfileMatrixTable(tables.Table):
    class Meta:
        model = PlantProfile
        template_name = 'django_tables2/bootstrap.html'
        fields = []
    
    