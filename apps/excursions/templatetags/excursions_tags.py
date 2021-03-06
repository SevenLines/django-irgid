# coding=utf-8
from __future__ import division

import re

import math
from django import template
from django.conf import settings
from django.core.urlresolvers import reverse
from django.template.defaultfilters import stringfilter
from django.template.loader import render_to_string
from django.utils.translation import get_language
from django.utils.translation import ugettext_lazy as _

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
            1: _(u'день'),
            2: _(u'дня'),
            3: _(u'дня'),
            4: _(u'дня'),
        }.get(days, _(u'дней'))
        out += "{} {}".format(days, day_verb)

    if hours:
        hrs = str(hours).split('.')[0]
        if hrs[-2:] in ('11', '12', '13', '14'):
            hour_verb = _(u'часов')
        elif hrs[-1] == '1':
            hour_verb = _(u'час')
        elif hrs[-1] in ('2', '3', '4'):
            hour_verb = _(u'часа')
        else:
            hour_verb = _(u'часов')
        out += " {} {}".format(str(hours).rstrip('0').rstrip('.'), hour_verb)

    return out.strip()

@register.filter
@stringfilter
def week_day_verbose(value):
    value = int(value)
    return {
        0: 'Понедельник',
        1: 'Вторник',
        2: 'Среда',
        3: 'Четверг',
        4: 'Пятница',
        5: 'Суббота',
        6: 'Воскресенье',
    }.get(value)

@register.filter
@stringfilter
def week_day_verb(value):
    value = int(value)
    return {
        0: 'Пн',
        1: 'Вт',
        2: 'Ср',
        3: 'Чт',
        4: 'Пт',
        5: 'Сб',
        6: 'Вс',
    }.get(value)

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.simple_tag(takes_context=True)
def menu(context):
    special_categories = ExcursionCategory.objects.get_special_categories_info()
    path = context['request'].path

    menu_dict = []
    selected_item = None

    lang = get_language()

    for item in settings.MENU:
        if item[5] and lang not in item[5]:
            continue

        if item[0] == 'travel:index' and 'travel_id' not in special_categories:
            continue
        if item[0] == 'gallery:index' and 'gallery_id' not in special_categories:
            continue

        if item[4](context):
            selected = re.search(item[2], path)
            menu_item = {
                'url': reverse(item[0]),
                'title': item[1],
                'selected': selected,
                'class': item[3],
            }
            if selected:
                selected_item = menu_item
            menu_dict.append(menu_item)

    return render_to_string("_/elements/menu.html", {
        'menu': menu_dict,
        'menu_current_item': selected_item
    }, context.request)


@register.filter
@stringfilter
def lazy_load(text):
    """
    :type text: str
    """
    import re
    exp = re.compile(r'(<img.*?)src="(.*?)"(.*?>)', re.IGNORECASE)
    return exp.sub(r'\1 class="lazy fadein" data-original="\2" \3', text)
