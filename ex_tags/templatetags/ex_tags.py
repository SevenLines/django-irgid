# coding=utf-8
from django.template.defaultfilters import stringfilter
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

def obfuscate_string(value):
    return ''.join(['&#{};'.format(str(ord(char))) for char in value])

# @register.simple_tag
# def theme(css_path=''):
#     """
#     Рендерит дополнительный css с темой
#     :param css_path:
#     :return:
#     """
#     if css_path == '':
#         css_path = MainPage.solo().current_theme_css
#     if css_path == '':
#         return ""
#
#     return render_to_string("ex_tags/link_css.html", {
#         'css_path': css_path
#     })


@register.filter
@stringfilter
def obfuscate(value):
    return mark_safe(obfuscate_string(value))


@register.filter
@stringfilter
def obfuscate_mailto(value, text=False):
    mail = obfuscate_string(value)

    if text:
        link_text = text
    else:
        link_text = mail
    address = obfuscate_string(value)
    return mark_safe('<a href="mailto:%s">%s</a>' % (address, address))

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)