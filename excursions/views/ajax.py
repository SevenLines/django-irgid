from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from app.utils import require_in_POST
from excursions.models import Excursion
from excursions.views.__base import _excursion_save, _excursion_context


@login_required
def excursion_save(request):
    _excursion_save(request)
    context = _excursion_context(request)
    context['e'] = Excursion.objects.get(pk=request.POST['id'])
    return render(request, "excursions/category-excursion-item.html", context)