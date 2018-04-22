from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import translation

from custom_settings.models import TextSetting, IntegerSetting


class Command(BaseCommand):
    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument("lang", nargs='?', default="ru")

    def handle(self, *args, **options):
        with translation.override(options['lang']):
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
