import math
import os
import subprocess

from django import template
from django.conf import settings

register = template.Library()


@register.filter
def getattribute(obj, attribute):
    a = getattr(obj, attribute)
    if callable(a):
        return a()
    return a


@register.filter
def get(obj, key):
    a = obj.get(key)
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


@register.simple_tag
def git_ver():
    '''
    Retrieve and return the latest git commit hash ID and tag as a dict.
    '''
    
    git_dir = os.path.dirname(settings.BASE_DIR)
    
    try:
        # Date and hash ID
        head = subprocess.Popen(
            "git -C {dir} log -1 --pretty=format:\"%h on %cd\" --date=short".format(dir=git_dir),
            shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        version = head.stdout.readline().strip().decode('utf-8')
        
        # Latest tag
 
        
        git_string = "ver. {v}".format(v=version)
        if 'not a git repo' in git_string:
            return ''
    except:
        git_string = ''
    
    return git_string

@register.filter
def hpg_float_format(num, n=2):
    if num:
        return f"{num:.{n}f}"
    else:
        return "0"