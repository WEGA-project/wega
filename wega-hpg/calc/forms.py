from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import CheckboxInput

from calc.models import PlantProfile, PlantProfileHistory


class PlantProfileAddForm(forms.ModelForm):
    class Meta:
        model = PlantProfile
        fields = ['name', 'template']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control d-inline-block'
            if visible.name != 'name':
                visible.field.initial = 0
                visible.field.widget.attrs['required'] = True


class PlantProfileEditForm(forms.ModelForm):
    class Meta:
        model = PlantProfile
        exclude = ['user', 'ec', 'ppm']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.calc_mode ==  PlantProfile.CalcMode.K:
            del self.fields['mgno3_mg']
            del self.fields['mgno3_no3']
        
        

        for visible in self.visible_fields():
            if visible.name != 'name':
                visible.field.widget.attrs['step'] = 1
                visible.field.widget.attrs['class'] = 'form-control d-inline-block precalc'
                # visible.field.widget.attrs['class'] = 'd-inline-block precalc'
                visible.field.widget.attrs['inputmode'] = "decimal"
                visible.field.initial = 0
                visible.field.required = False
            if visible.name == 'name':
                visible.field.widget.attrs['class'] = 'form-control d-inline-block col'
            if visible.name == 'calc_mode':
                visible.label= 'Метод расчета'

        
                
                
class DelForm(forms.Form):
    pass



class FilterForm(forms.Form):
    hide_macro = forms.BooleanField(required=False, label='Спрятать макро')
    hide_micro = forms.BooleanField(required=False, label='Спрятать микро')
    hide_salt   = forms.BooleanField(required=False, label='Спрятать проценты')
    show_gramms = forms.BooleanField(required=False, label='Спрятать соли')
    

class PlantProfileUploadForm(forms.Form):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
 