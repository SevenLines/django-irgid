from uuid import uuid4
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.http.response import HttpResponseBadRequest
from django.shortcuts import render
from app.utils import require_in_POST
from excursions.models import Excursion, ExcursionCategory, ExcursionImage


def _excursion_context(request):
    categories = ExcursionCategory.objects.all()

    if not request.user.is_authenticated():
        categories = filter(lambda c: Excursion.objects.filter(category=c, published=True).count() > 0, categories)

    return {
        'categories': categories
    }


def _excursion_save(request):
    if 'id' in request.POST:
        e = Excursion.objects.get(pk=int(request.POST['id']))
    else:
        if 'category_id' in request.POST:
            e = Excursion()
        else:
            return HttpResponseBadRequest("category_id is not defined")

    if 'small_image' in request.FILES:
        f = request.FILES['small_image']
        ext = f.name.split('.')[-1]
        e.img_preview.delete()
        e.img_preview.save('%s.%s' % (uuid4(), ext), ContentFile(f.read()))
        e.save()

    if 'big_image' in request.FILES:
        f = request.FILES['big_image']
        ext = f.name.split('.')[-1]
        e.image.delete()
        e.image.save('%s.%s' % (uuid4(), ext), ContentFile(f.read()))
        e.save()

    if 'gallery[]' in request.FILES:
        for f in request.FILES.getlist('gallery[]'):
            ext = f.name.split('.')[-1]
            image = ExcursionImage()
            image.excursion = e
            image.image.save('%s.%s' % (uuid4(), ext), ContentFile(f.read()))
            image.save()



    if 'category_id' in request.POST and e.category_id != int(request.POST['category_id']):
        e.category_id = int(request.POST['category_id'])

    if 'title' in request.POST:
        e.title = request.POST['title']

    if 'price_list' in request.POST:
        e.priceList = request.POST['price_list']

    if 'description' in request.POST:
        e.description = request.POST['description']

    if 'short_description' in request.POST:
        e.short_description = request.POST['short_description']

    if 'published' in request.POST:
        e.published = request.POST['published'] == 'True'

    e.save()