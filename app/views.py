# coding=utf-8
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http.response import HttpResponseBadRequest, HttpResponse
from django.shortcuts import redirect
from app.utils import require_in_POST

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