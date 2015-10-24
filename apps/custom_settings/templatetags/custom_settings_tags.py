from django import template

from custom_settings.models import TextSetting

register = template.Library()

@register.simple_tag
def custom_setting(key):
    return TextSetting.objects.get(key=key).value

@register.filter
def custom_setting_value(key):
    return TextSetting.objects.get(key=key).value