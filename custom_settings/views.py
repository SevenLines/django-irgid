# coding=utf-8
# Create your views here.
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView

from custom_settings.models import TextSetting


class SettingsListView(ListView):
    model = TextSetting

    def get_context_data(self, **kwargs):
        context = super(SettingsListView, self).get_context_data(**kwargs)
        context.update({
            'title': u'Настройки'
        })
        return context


class SettingEditView(UpdateView):
    model = TextSetting
    fields = ['value', ]

    def get_success_url(self):
        return self.request.META['HTTP_REFERER']