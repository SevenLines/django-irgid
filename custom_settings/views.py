# Create your views here.
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView

from custom_settings.models import TextSetting


class SettingsListView(ListView):
    model = TextSetting


class SettingEditView(UpdateView):
    model = TextSetting
    fields = ['value', ]

    def get_success_url(self):
        return self.request.META['HTTP_REFERER']