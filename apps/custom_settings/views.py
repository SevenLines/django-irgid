# coding=utf-8
# Create your views here.
from itertools import chain

from django.http.response import HttpResponse
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView

from custom_settings.models import TextSetting, IntegerSetting, Setting




class SettingsListView(ListView):
    model = Setting
    template_name = 'custom_settings/setting_list.html'

    def get_queryset(self):
        return chain(TextSetting.objects.all(), IntegerSetting.objects.all())

    def get_context_data(self, **kwargs):
        context = super(SettingsListView, self).get_context_data(**kwargs)
        context.update({
            'title': u'Настройки'
        })
        return context


class SettingEditView(UpdateView):
    model = Setting
    slug_field = 'key'
    fields = ['value', ]

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.value = request.POST['value'] if request.POST['value'] != '-' else None
        obj.save()

        if request.is_ajax():
            return HttpResponse()
        else:
            return redirect(self.get_success_url())

    def get_success_url(self):
        return self.request.META['HTTP_REFERER']