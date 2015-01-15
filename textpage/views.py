from uuid import uuid4
from django.contrib.auth.decorators import login_required, permission_required
from django.core.files.base import ContentFile
from django.http.response import HttpResponse
from django.shortcuts import render
import json


# Create your views here.
from app.utils import require_in_POST, require_in_GET
from textpage.models import TextPage, TextPageImage


@login_required
@permission_required("textpage.change_textpage")
@require_in_POST("id")
def save(request):
    p = TextPage.objects.get(id=request.POST['id'])
    if 'text' in request.POST:
        p.text = request.POST['text']
    p.save()
    return HttpResponse()

@login_required
def upload_image(request):
    f = request.FILES['image']
    im = TextPageImage()
    ext = f.name.split('.')[-1]
    im.image.save('%s.%s' % (uuid4(), ext), ContentFile(f.read()))
    im.save()
    return HttpResponse(json.dumps({
        "url": im.image.url,
        "id": im.id
    }), content_type="json")

@login_required
@require_in_GET("id")
def remove_image(request):
    im = TextPageImage.objects.get(pk=request.GET['id'])
    im.image.delete()
    im.delete()
    return HttpResponse()


def index(request):
    return render(request, "textpage/page.html", {})
