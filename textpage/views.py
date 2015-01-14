from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.shortcuts import render


# Create your views here.
from app.utils import require_in_POST
from textpage.models import TextPage


def index(request):
    return render(request, "textpage/page.html", {})


@login_required
@require_in_POST("id")
def save(request):
    p = TextPage.objects.get(id=request.POST['id'])
    if 'text' in request.POST:
        p.text = request.POST['text']
    p.save()
    return HttpResponse()