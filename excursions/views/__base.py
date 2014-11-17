from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from app.utils import require_in_POST
from excursions.models import Excursion, ExcursionCategory


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
        e = Excursion()

    if e.category_id != int(request.POST['category_id']):
        e.category_id = int(request.POST['category_id'])

    if 'title' in request.POST:
        e.title = request.POST['title']

    if 'description' in request.POST:
        e.description = request.POST['description']

    if 'published' in request.POST:
        e.published = request.POST['published'] == 'True'

    e.save()