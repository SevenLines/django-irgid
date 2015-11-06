from django import template
from django.conf import settings

from custom_settings.models import Setting

register = template.Library()


@register.simple_tag
def custom_setting(key):
    setting = Setting.objects.filter(key=key).first()
    result = None
    if setting:
        result = setting.get_value()
    return result


@register.filter
def custom_setting_value(key):
    setting = Setting.objects.filter(key=key).first()
    result = None
    if setting:
        result = setting.get_value()
    return result
