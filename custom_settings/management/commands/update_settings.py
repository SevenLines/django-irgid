from django.core.management.base import BaseCommand

from custom_settings.models import TextSetting
from custom_settings.settings_list import settings

class Command(BaseCommand):
    def handle(self, *args, **options):
        for s in settings:
            key = s[0]
            title = s[1]
            value = s[2]
            setting, created = TextSetting.objects.get_or_create(key=key)
            if created:
                setting.title = title
                setting.value = value
            else:
                setting.title = title
            setting.save()
