# coding=utf-8
import cms.api
from django.core.management.base import BaseCommand
from excursions.models import ExcursionCategory

__author__ = 'm'

class Command(BaseCommand):
    args = ''
    help = 'test'

    def handle(self, *args, **options):
        try:
            page = cms.api.create_page(title="Экскурсии",
                                       template="_/base.html",
                                       apphook="ExcursionsHook",
                                       in_navigation=True,
                                       published=True,
                                       language="ru")
        except BaseException as e:
            self.stderr.write(e.message)

        c = ExcursionCategory(
            title="В музеи"
        )
        c.save()

        c = ExcursionCategory(
            title="На Байкал"
        )
        c.save()

        c = ExcursionCategory(
            title="По городу"
        )
        c.save()

        c = ExcursionCategory(
            title="Пешие"
        )
        c.save()

        c = ExcursionCategory(
            title="Для школьников"
        )
        c.save()
