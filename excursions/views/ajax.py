import json
from uuid import uuid4
from django.contrib.auth.decorators import login_required, permission_required
from django.core.files.base import ContentFile
from django.db.transaction import atomic
from django.http.response import HttpResponse
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
    return render(request, "excursions/category-excursion-item.html", context)


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
@require_in_POST("id")
@permission_required("excursions.change_excursion")
def set_category_image(request):
    c = ExcursionCategory.objects.get(pk=request.POST['id'])
    if c and 'image' in request.FILES:
        f = request.FILES['image']
        ext = f.name.split('.')[-1]
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