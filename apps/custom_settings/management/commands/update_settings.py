from django.conf import settings
from django.core.management.base import BaseCommand

from custom_settings.models import TextSetting, IntegerSetting


class Command(BaseCommand):
    def handle(self, *args, **options):
        for key, s in settings.CUSTOM_SETTINGS.items():
            title = s[0]
            value = s[1]
            type = s[2]

            model = None
            if type == 'String':
                model = TextSetting
            elif type in ('Integer', 'ForeignKey'):
                model = IntegerSetting

            setting, created = model.objects.get_or_create(key=key)

            if created:
                setting.title = title
                setting.value = value
            else:
                setting.title = title

            setting.save()
