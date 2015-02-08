import json
from uuid import uuid4
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.files.base import ContentFile
from django.db.transaction import atomic
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from app.utils import require_in_POST, require_in_GET
from excursions.models import Excursion, ExcursionImage, ExcursionCategory
from excursions.views.base import _excursion_save, _excursion_context


@login_required
@permission_required("excursions.change_excursion")
def excursion_save(request):
    _excursion_save(request)
    context = _excursion_context(request)
    context['e'] = Excursion.objects.get(pk=request.POST['id'])
    return render(request, "excursions/category/category-excursion-item.html", context)


@login_required
@require_in_POST("excursion_id")
@permission_required("excursions.change_excursion")
def excursion_image_add(request):
    e = Excursion.objects.get(id=request.POST['excursion_id'])
    if e and 'image' in request.FILES:
        f = request.FILES['image']
        ext = f.name.split('.')[-1]
        image = ExcursionImage()
        image.excursion = e
        image.image.save('%s.%s' % (uuid4(), ext), ContentFile(f.read()))
        image.save()
    return HttpResponse()


@login_required
@require_in_POST("order")
@permission_required("excursions.change_excursion")
@atomic
def set_categories_order(request):
    order = request.POST['order']
    order = json.loads(order)
    for ec in ExcursionCategory.objects.filter(id__in=order.keys()):
        ec.order = order[unicode(ec.id)]
        ec.save()
    return HttpResponse()


@login_required
@permission_required("excursions.change_excursion")
@require_in_GET("visible", "id")
def toggle_category(request):
    c = ExcursionCategory.objects.get(pk=request.GET['id'])
    c.visible = request.GET['visible'] == "true"
    c.save()
    return HttpResponse(c.visible)


@login_required
@require_in_POST("title")
@permission_required("excursions.change_excursioncategory")
def category_save(request):
    # if len(request.POST['title']) == 0:
    # return HttpResponseBadRequest("title should not be empty")

    if 'id' in request.POST and request.POST['id'] != '':
        e = ExcursionCategory.objects.get(id=request.POST['id'])
    else:
        e = ExcursionCategory()

    if 'title' in request.POST:
        e.title = request.POST['title']

    if 'description' in request.POST:
        e.description = request.POST['description']

    if 'visible' in request.POST:
        e.visible = request.POST['visible'] == "true"

    if 'image' in request.FILES:
        f = request.FILES['image']
        ext = f.name.split('.')[-1]
        e.image.delete()
        e.image.save('%s.%s' % (uuid4(), ext), ContentFile(f.read()))

    e.save()

    return HttpResponse()

@login_required
@permission_required("excursions.delete_excursioncategory")
def category_remove(request):
    id = request.GET["id"]
    try:
        ExcursionCategory.objects.get(pk=id).delete()
    except Exception as e:
        messages.warning(request, e.message)

    return HttpResponse()

@login_required
@require_in_POST("id")
@permission_required("excursions.change_excursion")
def set_category_image(request):
    c = ExcursionCategory.objects.get(pk=request.POST['id'])
    if c and 'image' in request.FILES:
        f = request.FILES['image']
        ext = f.name.split('.')[-1]
        c.image.delete()
        c.image.save('%s.%s' % (uuid4(), ext), ContentFile(f.read()))
        c.save()
    return HttpResponse(c.image.url)


@login_required
@require_in_GET("id")
@permission_required("excursions.change_excursion")
def remove_category_image(request):
    c = ExcursionCategory.objects.get(pk=request.GET['id'])
    if c:
        assert isinstance(c, ExcursionCategory)
        c.image.delete()
    return HttpResponse()


@login_required
@permission_required("excursions.change_excursion")
def excursion_image_remove(request, id):
    ei = ExcursionImage.objects.get(id=id)
    ei.image.delete()
    ei.delete()
    return HttpResponse()
