# coding=utf-8
# Create your views here.
import json
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.http.response import HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.template.context import RequestContext
from app.utils import require_in_POST
from excursions.models import ExcursionCategory, Excursion, ExcursionImage
from excursions.utils import get_price_list
from excursions.views import ajax
from excursions.views.base import _excursion_save, _excursion_context


def index(request):
    context = _excursion_context(request)
    context['title'] = 'Иргид - экскурсионное агентство'
    return render(request, "excursions/main-page/index.html", context)


def category(request, id):
    context = _excursion_context(request)
    c = ExcursionCategory.objects.get(pk=id)
    context['current_category'] = c
    context['excursions'] = c.excursions(request).order_by("title")
    context['title'] = c.title
    context['meta'] = {
        'description': u"Категория: %s; Описание: %s"
                       % (c.title, c.description.strip())
    }
    return render(request, "excursions/category/index.html", context)


@login_required
@permission_required("excursions.delete_excursioncategory")
def category_remove(request, id):
    try:
        ExcursionCategory.objects.get(pk=id).delete()
    except Exception as e:
        messages.warning(request, e.message)

    return redirect(request.META['HTTP_REFERER'])


def excursion(request, id):
    context = _excursion_context(request)
    e = Excursion.objects.get(pk=id)
    context['current_excursion'] = e
    category = e.category
    context['current_category'] = category
    context['excursions'] = category.excursions(request).order_by("title")
    context['gallery'] = ExcursionImage.objects.filter(excursion_id=id).order_by("order")
    context['title'] = e.title
    context['meta'] = {
        'description': u"Экскурсия: %s; Описание: %s" % (e.title, e.short_description)
    }
    context['price_list'] = json.dumps(get_price_list(e.priceList))

    return render(request, "excursions/excursion/index.html", context)


@login_required
@permission_required("excursions.delete_excursion")
def excursion_remove(request, id):
    try:
        Excursion.objects.get(pk=id).delete()
    except Exception as e:
        messages.warning(request, e.message)

    return redirect(request.META['HTTP_REFERER'])


@login_required
@permission_required("excursions.change_excursion")
@require_in_POST("category_id")
def excursion_save(request):
    _excursion_save(request)
    return redirect(request.META['HTTP_REFERER'])


@login_required
@require_in_POST("title")
@permission_required("excursions.change_excursioncategory")
def category_save(request):
    ajax.category_save(request)
    return redirect(request.META['HTTP_REFERER'])


def excursion_gallery_index(request):
    context = {}
    c = ExcursionCategory.objects.filter(is_gallery=True).last()

    context['excursions'] = c.excursions(request).order_by("title") if c else []
    context['current_category'] = c
    context['title'] = u'Галерея'
    return render(request, "excursions/gallery/index.html", context)


def excursion_gallery_item(request, id):
    context = _excursion_context(request)
    e = Excursion.objects.get(pk=id)
    context['current_excursion'] = e
    category = e.category
    context['current_category'] = category
    context['excursions'] = category.excursions(request).order_by("title")
    context['gallery'] = ExcursionImage.objects.filter(excursion_id=id).order_by("order")
    context['title'] = e.title
    context['meta'] = {
        'description': u"Экскурсия: %s; Описание: %s" % (e.title, e.short_description)
    }
    context['price_list'] = json.dumps(get_price_list(e.priceList))

    return render(request, "excursions/gallery/excursion/index.html", context)