from django import template
from django.conf import settings

from custom_settings.models import Setting

register = template.Library()


@register.simple_tag
def custom_setting(key):
    return Setting.objects.get_value(key)


@register.filter
def custom_setting_value(key):
    return Setting.objects.get_value(key)
