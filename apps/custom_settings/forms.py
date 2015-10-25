from django.forms.forms import Form
from django.forms.models import ModelForm

from custom_settings.models import TextSetting


class TextSettingForm(ModelForm):
    class Meta:
        model = TextSetting
