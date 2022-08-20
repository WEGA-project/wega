
from django import template
register = template.Library()

@register.filter
def getattribute (obj, attribute):
    a = getattr(obj, attribute)
    if callable(a):
        return a()
    return a
    

@register.filter
def get_field_from_form(obj, attribute):
    # return obj.fields.get(attribute)
    return obj.fields[attribute].get_bound_field(obj, attribute)

@register.filter
def second_part(obj):
    # return obj.fields.get(attribute)
    return obj.split('_')[1]

@register.filter
def divide(a, b):
    # return obj.fields.get(attribute)
    if not a or not b:
        return  0
    return a/b

@register.filter
def index(indexable, i):
    return indexable[i]