from __future__ import division
from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def min_to_hours(value):
    value = round(int(value) / 60, 1)
    return u"%g" % value