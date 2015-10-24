# coding=utf-8
import os

from braces.views import LoginRequiredMixin
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.core.files.storage import FileSystemStorage
from django.http.response import HttpResponseBadRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.views.generic.base import TemplateView, View

from irgid.forms import UploadFileForm
from irgid.utils import require_in_POST

__author__ = 'm'

@require_in_POST("username", "password")
def login_user(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
        else:
            messages.error(request, u"Пользователь %s не активен" % username)
    else:
        messages.error(request, u"Неверная комбинация пользователь / пароль")
    return redirect(request.META['HTTP_REFERER'])


def handle_uploaded_file(f):
    with open('some/file/name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


class UploadFile(LoginRequiredMixin, View):
    storage = FileSystemStorage(os.path.join(settings.MEDIA_ROOT, 'common'),
                                base_url=os.path.join(settings.MEDIA_URL, 'common'))

    def post(self, request):
        form = UploadFileForm(request.POST, request.FILES)

        result = HttpResponseRedirect(request.META['HTTP_REFERER'])

        if form.is_valid():
            file = request.FILES['file']
            name = self.storage.save(name=None, content=file)
            result = self.storage.url(name)
            result = HttpResponse(result)

        return result


class TemplateViewEx(TemplateView):
    data = None

    def get_context_data(self, **kwargs):

        data = self.data if self.data else {}

        context = super(TemplateViewEx, self).get_context_data(**kwargs)
        context.update(data)
        return context
