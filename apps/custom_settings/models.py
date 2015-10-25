from django.conf import settings
from django.db import models
from django.db.models.loading import get_model
from polymorphic import PolymorphicModel


class Setting(PolymorphicModel):
    key = models.CharField(max_length=128, null=False, blank=True, unique=True)
    title = models.CharField(max_length=128, null=False, blank=True)

    def get_value(self):
        return self.value

    @property
    def type(self):
        return settings.CUSTOM_SETTINGS[self.key][2]


class TextSetting(Setting):
    value = models.TextField(null=True, default=True)


class IntegerSetting(Setting):
    value = models.IntegerField(null=True, default=True)

    @property
    def options(self):
        model_name_title = settings.CUSTOM_SETTINGS.get(self.key)[3]

        result = []
        model_name, title = model_name_title.split(':', 1)
        if model_name:
            model = get_model(*model_name.split('.', 1))
            result = [{'pk': item['pk'], 'title': item[title]} for item in model.objects.values('pk', title)]

        return result


