# coding=utf-8
# Create your views here.
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.template.context import RequestContext
from app.utils import require_in_POST
from excursions.models import ExcursionCategory, Excursion


def e_context():
    categories = ExcursionCategory.objects.all()

    return {
        'categories': categories,
    }


def index(request):
    return render(request, "excursions/preview.html", RequestContext(request, e_context()))


def category(request, id):
    return render(request, "excursions/preview-category.html", RequestContext(request, e_context()))


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
    return render(request, "excursions/preview-excursion.html", RequestContext(request, e_context()))


@login_required
def excursion_remove(request, id):
    try:
        Excursion.objects.get(pk=id).delete()
    except Exception as e:
        messages.warning(request, e.message)

    return redirect(request.META['HTTP_REFERER'])


@login_required
@require_in_POST("title", "description", "category_id")
def excursion_save(request):
    e = Excursion()
    e.title = request.POST['title']
    e.category_id = request.POST['category_id']
    e.description = request.POST['description']
    e.save()
    return HttpResponse(e.pk)