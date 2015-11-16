# coding=utf-8
from __future__ import division

import re

import math
from django import template
from django.conf import settings
from django.core.urlresolvers import reverse
from django.template.defaultfilters import stringfilter
from django.template.loader import render_to_string

from excursions.models import ExcursionCategory

register = template.Library()


@register.filter
@stringfilter
def min_to_hours(value):
    value = round(int(value) / 60, 1)
    return u"%g" % value


@register.filter
@stringfilter
def time_verbose(value):
    hours = round(int(value) / 60, 1)
    days = int(math.floor(hours / 24))
    hours -= days * 24

    out = ""

    if days:
        day_verb = {
            1: 'день',
            2: 'дня',
            3: 'дня',
            4: 'дня',
        }.get(days, 'дней')
        out += "{} {}".format(days, day_verb)

    if hours:
        hour_verb = 'часа' if hours <= 4 else 'часов'
        out += " {} {}".format(str(hours).rstrip('0').rstrip('.'), hour_verb)

    return out.strip()


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.simple_tag(takes_context=True)
def menu(context):
    special_categories = ExcursionCategory.objects.get_special_categories_info()
    path = context['request'].path

    menu_dict = []
    for item in settings.MENU:
        if item[0] == 'travel:index' and 'travel_id' not in special_categories:
            continue
        if item[0] == 'gallery:index' and 'gallery_id' not in special_categories:
            continue

        if item[4](context):
            menu_dict.append({
                'url': reverse(item[0]),
                'title': item[1],
                'selected': re.match(item[2], path),
                'class': item[3],
            })

    return render_to_string("_/elements/menu.html", {
        'menu': menu_dict
    }, context)
