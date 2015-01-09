# coding=utf-8
# Create your views here.
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.template.context import RequestContext
from app.utils import require_in_POST
from excursions.forms import ExcursionForm
from excursions.models import ExcursionCategory, Excursion
from excursions.views import ajax
from excursions.views.__base import _excursion_save, _excursion_context


def index(request):
    context = _excursion_context(request)
    return render(request, "excursions/preview.html", context)


def category(request, id):
    context = _excursion_context(request)
    category = ExcursionCategory.objects.get(pk=id)
    context['current_category'] = category
    context['excursions'] = category.excursions(request).order_by("title")
    return render(request, "excursions/preview-category.html", context)


@login_required
def category_remove(request, id):
    try:
        ExcursionCategory.objects.get(pk=id).delete()
    except Exception as e:
        messages.warning(request, e.message)

    return redirect(request.META['HTTP_REFERER'])


@login_required
@require_in_POST("title", "description")
def category_save(request):
    if len(request.POST['title']) == 0:
        return HttpResponseBadRequest("title should not be empty")

    if 'id' in request.POST and request.POST['id'] != '':
        e = ExcursionCategory.objects.get(id=request.POST['id'])
    else:
        e = ExcursionCategory()

    e.title = request.POST['title']
    e.description = request.POST['description']
    e.save()

    return redirect(request.META['HTTP_REFERER'])


def excursion(request, id):
    context = _excursion_context(request)
    context['current_excursion'] = Excursion.objects.get(pk=id)
    category = context['current_excursion'].category
    context['current_category'] = category
    context['excursions'] = category.excursions(request).order_by("title")
    # context['form'] = ExcursionForm()

    return render(request, "excursions/preview-excursion.html", context)


@login_required
def excursion_remove(request, id):
    try:
        Excursion.objects.get(pk=id).delete()
    except Exception as e:
        messages.warning(request, e.message)

    return redirect(request.META['HTTP_REFERER'])


@login_required
@require_in_POST("category_id")
def excursion_save(request):

    _excursion_save(request)

    return redirect(request.META['HTTP_REFERER'])