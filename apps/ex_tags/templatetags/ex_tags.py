# coding=utf-8
from django.template.defaultfilters import stringfilter
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

def obfuscate_string(value):
    return ''.join(['&#{};'.format(str(ord(char))) for char in value])

@register.filter
@stringfilter
def obfuscate(value):
    return mark_safe(obfuscate_string(value))


@register.filter
@stringfilter
def obfuscate_mailto(value, text=False):
    address = obfuscate_string(value)
    return mark_safe('<a href="mailto:%s">%s</a>' % (address, address))

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)