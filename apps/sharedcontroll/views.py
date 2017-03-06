from django.http.response import HttpResponse
from django.shortcuts import render

# Create your views here.
from sharedcontroll.models import SharedURL


def share(request):
    url = SharedURL()
    url.url = request.META.get('HTTP_REFERER')

    if 'service' in request.GET:
        url.service = request.GET['service']

    url.save()
    return HttpResponse()