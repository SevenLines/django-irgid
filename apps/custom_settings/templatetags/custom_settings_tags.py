from django import template
from django.conf import settings
from django.template.defaultfilters import safe
from django.utils.safestring import mark_safe

from custom_settings.models import Setting

register = template.Library()


@register.simple_tag
def custom_setting(key):
    return mark_safe(Setting.objects.get_value(key))


@register.filter
def custom_setting_value(key):
    return mark_safe(Setting.objects.get_value(key))
