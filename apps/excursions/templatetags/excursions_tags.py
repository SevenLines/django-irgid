from __future__ import division

import re
from django import template
from django.conf import settings
from django.core.urlresolvers import reverse
from django.template.defaultfilters import stringfilter
from django.template.loader import render_to_string

register = template.Library()

@register.filter
@stringfilter
def min_to_hours(value):
    value = round(int(value) / 60, 1)
    return u"%g" % value


@register.simple_tag(takes_context=True)
def menu(context):
    path = context['request'].path
    menu_dict = map(lambda x: {
        'url': reverse(x[0]),
        'title': x[1],
        'selected': re.match(x[2], path),
        'class': x[3],
        'login_required': x[4],
    }, settings.MENU)
    return render_to_string("_/elements/menu.html", {
        'menu': menu_dict
    }, context)
