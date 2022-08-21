from django.template.loader import render_to_string
from django.utils.html import format_html
import django_tables2 as tables
from django.utils.safestring import mark_safe

from calc.models import PlantProfile

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
    

class HistoryColumn(tables.Column):
    def render(self, value, record):
        if isinstance(value, str):
            return mark_safe(value)
        elif value['mark-danger']:
            return mark_safe(f'<span class="text-danger">{value["val"]}</span>')
        else:
            return mark_safe(f'<span class="text">{value["val"]}</span>')
        return value